from fastapi import APIRouter, Path, HTTPException, Depends
from typing import Annotated
from datetime import date
from sqlmodel import Session
from app import schemas, crud, database

router = APIRouter(prefix="/hello")

# Dependency to get a database session
SessionDep = Annotated[Session, Depends(database.get_session)]


@router.put(
    "/{username}", summary="Add User's birthday", response_model=schemas.Message
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


@router.get(
    "/{username}", summary="Get User's birthday", response_model=schemas.Message
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
