# Multi-stage build
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app
# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# Use a final image without uv
FROM python:3.14-slim-bookworm

# The runtime only needs the uv-managed virtual environment, so drop the base
# image's pip: nothing uses it, and its vendored copies of urllib3, setuptools
# and msgpack carry fixable CVEs that would otherwise fail the Trivy gate.
RUN python -m pip uninstall -y pip

# Copy the application from the builder. The files stay owned by root and are
# only readable by the unprivileged runtime user below, so the application
# cannot modify its own code or virtual environment.
COPY --from=builder /app /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app
EXPOSE 8000

# Create non-root user
RUN adduser --disabled-password --uid 1000 appuser
USER 1000

# Run the FastAPI application. Hot reloading for local development is enabled
# by compose.yaml, which overrides this command to add `--reload`.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# The slim base image ships no curl, so probe the liveness endpoint with the
# Python standard library. Kubernetes ignores HEALTHCHECK and relies on the
# probes in the Helm chart; this one serves Docker and Compose.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/live', timeout=3)"]
