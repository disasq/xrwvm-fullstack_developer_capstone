# fullstack_developer_capstone

Repository: xrwvm-fullstack_developer_capstone

Best Cars is a car dealership review portal built with Django, React, Express, MongoDB, and a Flask sentiment service.

## Run

```sh
docker compose up --build
```

Open http://localhost:8000. Register an account to post reviews. Configure DJANGO_SECRET_KEY and DJANGO_ALLOWED_HOSTS for deployment. Create an administrator with `docker compose exec web python manage.py createsuperuser`.

## Services

- Django serves the React application and authenticates users.
- Express stores dealerships and reviews in MongoDB and seeds the supplied dataset only when empty.
- Flask analyzes review sentiment with VADER.
- CarMake and CarModel are managed through Django Admin.

## Verification

The GitHub Actions workflow runs Django checks and tests, Python linting, JavaScript syntax checks, and the React production build. Evidence is captured from live requests and browser interactions.
