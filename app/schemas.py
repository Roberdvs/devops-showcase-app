from pydantic import BaseModel, Field
from datetime import date


class UserCreate(BaseModel):
    dateOfBirth: date = Field(..., description="Date of birth in YYYY-MM-DD format")


class Message(BaseModel):
    message: str


class HealthCheck(BaseModel):
    status: str = "OK"
