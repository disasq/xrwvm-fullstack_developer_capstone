# Best Cars — Dealership Review Portal

Full Stack Application Development Capstone Project by **Dias Saqyp**.

Best Cars lets visitors browse 50 dealerships, filter by state, read reviews and their sentiment, register, log in, and post a review. Django Admin manages car makes and models.

## Run the application

```sh
docker compose up --build
```

Open http://localhost:8000. Django accounts and the MongoDB review database use persistent Docker volumes. Register through the Sign up page. Create a local administrator with:

```sh
docker compose exec web python manage.py createsuperuser
```

For an HTTPS proxy, set `DJANGO_CSRF_TRUSTED_ORIGINS` to the exact external origin. Set `DJANGO_SECRET_KEY` and `DJANGO_ALLOWED_HOSTS` for your environment.

## Architecture

- Django authenticates users, serves React and the static About/Contact pages, and proxies the backend services.
- React displays dealerships, state filters, dealer details, registration, login, and the review form.
- Express and MongoDB store dealerships and reviews. The supplied records are seeded only when the collections are empty.
- Flask and VADER analyze review sentiment.
- Django CarMake and CarModel store the car catalog used in the review form.

## Capstone submission

See [SUBMISSION_GUIDE.md](SUBMISSION_GUIDE.md) for the mapping of all 28 tasks. Actual terminal output and cURL responses are in [evidence](evidence). The accompanying submission ZIP contains 12 screenshots.

[Deployment URL](evidence/deploymentURL) · [Successful CI run](https://github.com/disasq/xrwvm-fullstack_developer_capstone/actions/runs/44125992044)

The deployment runs in the Skills Network Kubernetes lab. Its URL is available while the lab and port forwarding remain running. After a new pod is created, restart the port forward:

```sh
kubectl port-forward service/dealership 8003:8000 --address 0.0.0.0
```

The lab manifest contains this session's registry namespace. Update the three image addresses, trusted origin, and allowed hosts for a different environment. Create the `dealership-secret` Kubernetes secret before applying the manifest. The lab's Kubernetes databases are temporary; register a new account after replacing a pod.

## Verification

GitHub Actions runs Python linting, Express syntax validation, a React production build, Django configuration checks, and four Django tests. The application was also checked through live API requests, root admin login/logout, state filtering, and posting reviews in both Compose and Kubernetes.

Test credentials are excluded from the public repository. In `evidence/loginuser`, `DEMO_PASSWORD` replaces the password used during the recorded request; the response is unchanged.
