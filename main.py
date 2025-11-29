from fastapi import FastAPI
from contextlib import asynccontextmanager
from app import api, health
from app import database, telemetry
from prometheus_fastapi_instrumentator import Instrumentator
from loguru import logger
import sys

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
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
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
