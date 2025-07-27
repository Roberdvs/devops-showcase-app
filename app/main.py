from fastapi import FastAPI, HTTPException, Path, Depends
from contextlib import asynccontextmanager
from fastapi.responses import RedirectResponse
from typing import Annotated
from app import schemas, crud, database, telemetry
from sqlmodel import Session
from sqlalchemy import text
from datetime import date
from prometheus_fastapi_instrumentator import Instrumentator

# Initialize OpenTelemetry tracer
tracer = telemetry.setup_opentelemetry()


# FastAPI lifespan to initialize the database and tables on startup
@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Startup logic
    database.create_db_and_tables()
    yield

# Initialize FastAPI app
app = FastAPI(lifespan=lifespan)

# Instrument FastAPI with OpenTelemetry tracing
telemetry.instrument_fastapi(app)

# Instrument FastAPI with Prometheus metrics
Instrumentator().instrument(app).expose(app, include_in_schema=False, should_gzip=True)

# Dependency to get a database session
SessionDep = Annotated[Session, Depends(database.get_session)]

###############
# API Endpoints
###############


@app.get("/")
def root():
    """Redirect to the API documentation."""
    return RedirectResponse(url="/docs")


@app.put(
    "/hello/{username}", summary="Add User's birthday", response_model=schemas.Message
)
def put_hello(
    session: SessionDep,
    username: str = Path(..., pattern="^[A-Za-z]+$"),
    payload: schemas.UserCreate = ...,
):
    """Create or update a user's date of birth.
    - username: must contain only letters
    - dateOfBirth: must be before today
    """
    if payload.dateOfBirth >= date.today():
        raise HTTPException(status_code=400, detail="dateOfBirth must be before today")
    crud.create_or_update_user(session, username, payload.dateOfBirth)
    msg = "Date of Birth added sucessfully"
    return {"message": msg}


@app.get(
    "/hello/{username}", summary="Get User's birthday", response_model=schemas.Message
)
def get_hello(
    session: SessionDep,
    username: str = Path(..., pattern="^[A-Za-z]+$"),
):
    """Return a birthday message for the given user.
    - If today is the user's birthday: 'Happy birthday!'
    - Otherwise: 'Your birthday is in N day(s)'
    """
    user = crud.get_user(session, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    today = date.today()
    bday = user.date_of_birth.replace(year=today.year)
    if bday < today:
        bday = bday.replace(year=today.year + 1)
    days = (bday - today).days
    if days == 0:
        msg = f"Hello, {username}! Happy birthday!"
    else:
        msg = f"Hello, {username}! Your birthday is in {days} day(s)"
    return {"message": msg}


@app.get(
    "/health/live",
    summary="Liveness Health Check",
    response_description="Returns 200 (OK) if application is running",
    response_model=schemas.HealthCheck,
)
def liveness_check():
    """Liveness check endpoint. Returns 200 (OK) if application process is running."""
    return schemas.HealthCheck(status="OK")


@app.get(
    "/health/ready",
    summary="Readiness Health Check",
    response_description="Returns 200 (OK) if application is ready to serve traffic",
    response_model=schemas.HealthCheck,
)
def readiness_check():
    """Readiness check endpoint. Returns 200 (OK) if application can serve traffic."""
    # Test database connectivity
    try:
        with database.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return schemas.HealthCheck(status="OK")
    except Exception as e:
        # Return 503 Service Unavailable if database is not accessible
        raise HTTPException(
            status_code=503, detail=f"Database connection failed: {str(e)}"
        )
