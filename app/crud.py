from sqlmodel import Session, select
from app.models import User
from datetime import date

def create_or_update_user(session: Session, username: str, dob: date):
    statement = select(User).where(User.username == username)
    user = session.exec(statement).one_or_none()
    if user:
        user.date_of_birth = dob
    else:
        user = User(username=username, date_of_birth=dob)
        session.add(user)
    session.commit()

def get_user(session: Session, username: str):
    statement = select(User).where(User.username == username)
    return session.exec(statement).one_or_none() 