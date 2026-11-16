"""Capture real HTTP responses from a running local capstone stack."""
import json
import os
from pathlib import Path
import shlex
import subprocess

out = Path('evidence')
out.mkdir(exist_ok=True)
base = os.environ.get('APP_URL', 'http://localhost:8000').rstrip('/')
user = os.environ.get('DEMO_USERNAME', 'demo_reviewer')
password = os.environ['DEMO_PASSWORD']
cookies = '/tmp/capstone-evidence-cookies'


def capture(name, args):
    command = ['curl', '-sS', '--fail-with-body', *args]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    try:
        body = json.dumps(json.loads(result.stdout), indent=2, ensure_ascii=False)
    except json.JSONDecodeError:
        body = result.stdout
    text = '$ ' + shlex.join(command).replace(password, '${DEMO_PASSWORD}') + '\n' + body + '\n'
    (out / name).write_text(text)
    print(f'{name}: captured {len(body)} characters')


registration = {'userName': user, 'firstName': 'Demo', 'lastName': 'Reviewer',
                'email': 'reviewer@example.com', 'password': password}
subprocess.run(['curl', '-sS', '-X', 'POST', base + '/djangoapp/register',
                '-H', 'Content-Type: application/json', '-d', json.dumps(registration)],
               capture_output=True, check=True)
capture('loginuser', ['-c', cookies, '-X', 'POST', base + '/djangoapp/login',
                      '-H', 'Content-Type: application/json',
                      '-d', json.dumps({'userName': user, 'password': password})])
capture('logoutuser', ['-b', cookies, base + '/djangoapp/logout'])
for name, endpoint in [('getdealerreviews', '/djangoapp/reviews/dealer/1'),
                       ('getalldealers', '/djangoapp/get_dealers'),
                       ('getdealerbyid', '/djangoapp/dealer/1'),
                       ('getdealersbyState', '/djangoapp/get_dealers/Kansas'),
                       ('getallcarmakes', '/djangoapp/get_cars')]:
    capture(name, [base + endpoint])
capture('analyzereview', ['http://localhost:5050/analyze/Fantastic%20services'])
run_id = '43806184116'
api_url = f'https://api.github.com/repos/disasq/xrwvm-fullstack_developer_capstone/actions/runs/{run_id}/jobs'
command = ['curl', '-fsSL', api_url]
result = subprocess.run(command, capture_output=True, text=True, check=True)
jobs = json.loads(result.stdout)['jobs']
lines = ['$ ' + shlex.join(command), f'GitHub Actions run: {run_id}']
for job in jobs:
    lines.append(f"Job {job['name']}: {job['conclusion']}")
    for step in job['steps']:
        lines.append(f"  {step['number']}. {step['name']}: {step['conclusion']} ({step['started_at']} - {step['completed_at']})")
(out / 'CICD').write_text('\n'.join(lines) + '\n')
print('CICD: captured executed workflow steps')
