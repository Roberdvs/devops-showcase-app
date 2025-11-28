# Copilot Instructions for AI Coding Agents

## Project Overview
- **FastAPI** backend with SQLModel ORM and PostgreSQL database.
- Containerized with Docker, orchestrated via Docker Compose for local dev and Helm for Kubernetes.
- Observability: OpenTelemetry tracing, Prometheus metrics, structured logging (Loguru).
- CI/CD: GitHub Actions for tests, builds, Helm chart publishing, and e2e tests in ephemeral minikube.

## Key Directories & Files
- `app/`: Main application code (API, models, database, telemetry, health checks)
- `app/tests/unit/`: Unit tests (isolated, in-memory SQLite)
- `app/tests/integration/`: Integration tests (Testcontainers, real PostgreSQL)
- `helm/`: Helm chart for Kubernetes deployment
- `compose.yaml`: Docker Compose for local dev
- `Makefile`: Common dev/test/build commands
- `pyproject.toml`: Python dependencies

## Developer Workflows
- **Local Dev:** `make dev` (Docker Compose, hot reload)
- **Unit Tests:** `make test` (runs with coverage)
- **Integration Tests:** `make integration-tests` (Testcontainers)
- **Build Image:** `make build`
- **Helm Deploy:** `make helm-deps` & `make helm-install`

## Application Patterns
- **Database config:**
  - Uses env vars: `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` or a single `DATABASE_URL` (takes precedence).
  - See `app/database.py` for connection logic.
- **API structure:**
  - All endpoints under `/hello` (see `app/api.py`).
  - Health endpoints: `/health/live`, `/health/ready` (see `app/health.py`).
- **Observability:**
  - Tracing: controlled by `OTEL_TRACES_EXPORTER` env var.
  - Metrics: `/metrics` endpoint, enabled with `ENABLE_METRICS=true`.
- **Logging:**
  - Structured JSON logs via Loguru (see `app/main.py`).

## Testing Patterns
- **Unit tests:**
  - Use in-memory SQLite, override DB session via dependency injection.
  - See `app/tests/unit/test_api.py` for examples.
- **Integration tests:**
  - Use Testcontainers to spin up PostgreSQL.
  - Fixtures in `app/tests/integration/conftest.py`.

## Kubernetes & Helm
- **Helm chart:**
  - Located in `helm/devops-showcase-app/`.
  - `values.yaml`: dev defaults; `values-prod-example.yaml`: production patterns (external DB, ingress, PDB, etc).
- **CI/CD:**
  - Chart published to GitHub Pages on main branch push.
  - See `.github/workflows/chart-releaser.yaml`.

## Conventions & Tips
- Follow 12-factor app principles: all config via env vars.
- Prefer updating `Makefile` for new workflows.
- Use `uv` for Python dependency management (see Dockerfile and CI).
- For new endpoints, add to `app/api.py` and document in OpenAPI.
- For new metrics or tracing, use Prometheus and OpenTelemetry patterns from `app/telemetry.py`.

---

For more details, see `README.md` and referenced files. If any section is unclear or missing, please provide feedback for improvement.
