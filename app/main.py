from fastapi import FastAPI, HTTPException, Path, status, Depends
from app import schemas, crud, database
from sqlmodel import Session
from datetime import date

app = FastAPI()

@app.on_event("startup")
def on_startup():
    database.create_db_and_tables()

@app.put("/hello/{username}", status_code=status.HTTP_204_NO_CONTENT)
def put_hello(
    username: str = Path(..., pattern="^[A-Za-z]+$"),
    payload: schemas.UserCreate = ...,
    session: Session = Depends(database.get_session),
):
    if payload.dateOfBirth >= date.today():
        raise HTTPException(status_code=400, detail="dateOfBirth must be before today")
    crud.create_or_update_user(session, username, payload.dateOfBirth)
    return

@app.get("/hello/{username}", response_model=schemas.Message)
def get_hello(
    username: str = Path(..., pattern="^[A-Za-z]+$"),
    session: Session = Depends(database.get_session),
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
    session: Session = Depends(database.get_session),
):
    return {"message": "db connection"}