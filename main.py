import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from prometheus_fastapi_instrumentator import Instrumentator

from app import api, database, health, telemetry

# Remove default loguru handler
logger.remove()
# Initialize loguru handler for structured logging
logger.add(sys.stderr, serialize=True)

# Initialize OpenTelemetry tracer
tracer = telemetry.setup_opentelemetry()


# FastAPI lifespan to initialize the database and tables on startup
@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Startup logic. Fail fast if database is not available
    try:
        logger.info("Attempting to initialize database...")
        database.create_db_and_tables()
        logger.info("Database initialized successfully")
    except Exception:  # noqa: BLE001
        # Deliberately broad: startup must fail fast on any error here.
        # logger.exception records the traceback in the structured log.
        logger.exception("Failed to initialize database")
        sys.exit(1)
    yield


# Initialize FastAPI app
app = FastAPI(lifespan=lifespan)

# Instrument FastAPI with OpenTelemetry tracing
telemetry.instrument_fastapi(app)

# Instrument FastAPI with Prometheus metrics
Instrumentator().instrument(app).expose(app, include_in_schema=False, should_gzip=True)

# Include routers
app.include_router(api.router)
app.include_router(health.router)
