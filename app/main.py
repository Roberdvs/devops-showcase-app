from fastapi import FastAPI, HTTPException, Path, Depends
from contextlib import asynccontextmanager
from fastapi.responses import RedirectResponse
from typing import Annotated
from app import schemas, crud, database
from sqlmodel import Session
from datetime import date

SessionDep = Annotated[Session, Depends(database.get_session)]


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Startup logic
    database.create_db_and_tables()
    yield
    # (Optional) Shutdown logic here


app = FastAPI(lifespan=lifespan)


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
    "/health",
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    response_model=schemas.HealthCheck,
)
def get_health():
    """Health check endpoint. Returns status OK as JSON."""
    return schemas.HealthCheck(status="OK")
