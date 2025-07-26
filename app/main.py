from fastapi import FastAPI, HTTPException, Path, status, Depends
from typing import Annotated
from app import schemas, crud, database
from sqlmodel import Session
from datetime import date

SessionDep = Annotated[Session, Depends(database.get_session)]

app = FastAPI()

@app.on_event("startup")
def on_startup():
    database.create_db_and_tables()

@app.put("/hello/{username}")
def put_hello(
    session: SessionDep,
    username: str = Path(..., pattern="^[A-Za-z]+$"),
    payload: schemas.UserCreate = ...,
):
    if payload.dateOfBirth >= date.today():
        raise HTTPException(status_code=400, detail="dateOfBirth must be before today")
    crud.create_or_update_user(session, username, payload.dateOfBirth)
    return username

@app.get("/hello/{username}", response_model=schemas.Message)
def get_hello(
    session: SessionDep,
    username: str = Path(..., pattern="^[A-Za-z]+$"),
):
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
    status_code=status.HTTP_200_OK,
    response_model=schemas.HealthCheck,
)
def get_health():
    return schemas.HealthCheck(status="OK")

@app.get("/testdb", response_model=schemas.Message)
def get_hello(
    session: SessionDep,
):
    return {"message": "db connection"}