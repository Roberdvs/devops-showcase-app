# Sample app

A sample FastAPI application with PostgreSQL backend.

## Features
- OpenAPI docs
- PostgreSQL database
- Containerized for local development

## Quickstart

### Local Development

1. Clone the repo
2. Run: `docker compose up --watch`. Application will be hot reloaded when performing changes to the source code.
3. API docs: http://localhost:8000/docs

### Running Unit Tests

```
uv run coverage run -m pytest
uv run coverage report
```
