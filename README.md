# Sample app

## Project Overview

This project demonstrates a modern, production-ready FastAPI application with:

- OpenAPI docs endpoints with Swagger UI and ReDoc
- PostgreSQL database
- Containerized for local development
- Cloud-agnostic deployment (Docker, Helm)
- Automated tests and code quality tools

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Python 3.13+](https://www.python.org/downloads/) (for running tests/linters locally)
- [uv](https://github.com/astral-sh/uv) (for Python dependency management)
- [Helm](https://helm.sh/) (for Kubernetes deployment)

## Project Structure

```
app/           # Application code (FastAPI, models, db, tests)
helm/          # Helm chart for Kubernetes deployment
Dockerfile     # Container build
compose.yaml   # Docker Compose for local dev
Makefile       # Common dev/test/build commands
```

## Local Development

1. Clone the repo
2. Run: `make dev` (starts app and db with Docker Compose, hot reload enabled)
3. API docs: [http://localhost:8000/docs](http://localhost:8000/docs) and [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Running Unit Tests

Run `make test` (uses `uv` and `coverage`)

## Common Makefile Commands

- `make dev`           – Start app and db locally (hot reload)
- `make test`          – Run tests with coverage
- `make build`         – Build Docker image
- `make helm-install`  – Install Helm chart to local cluster

## Deployment with Helm

1. Build and push your Docker image to a registry (update `values.yaml` with the image repo/tag)
2. Update Helm dependencies:
   ```sh
   make helm-deps
   ```
3. Install to your cluster:
   ```sh
   make helm-install
   ```

See the `helm/sample-app/values.yaml` for configuration options (ingress, DB, env, etc).
