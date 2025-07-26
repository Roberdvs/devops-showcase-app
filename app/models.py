from sqlmodel import SQLModel, Field
from datetime import date


class User(SQLModel, table=True):
    username: str = Field(primary_key=True, index=True)
    date_of_birth: date
