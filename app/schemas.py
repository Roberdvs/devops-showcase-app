from datetime import date

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    dateOfBirth: date = Field(..., description="Date of birth in YYYY-MM-DD format")


class Message(BaseModel):
    message: str


class HealthCheck(BaseModel):
    status: str = "OK"
