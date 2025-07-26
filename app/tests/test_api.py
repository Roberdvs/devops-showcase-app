from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool
from datetime import date, timedelta

from app.main import app
from app import database

# Create a new in-memory SQLite engine for testing
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create the tables
SQLModel.metadata.create_all(engine)


def get_session_override():
    with Session(engine) as session:
        yield session


app.dependency_overrides[database.get_session] = get_session_override

client = TestClient(app)


def test_create_user_valid():
    resp = client.put("/hello/foo", json={"dateOfBirth": "2000-01-01"})
    assert resp.status_code == 200


def test_update_user_valid():
    # Create
    resp = client.put("/hello/bar", json={"dateOfBirth": "1990-01-01"})
    assert resp.status_code == 200
    # Update
    resp = client.put("/hello/bar", json={"dateOfBirth": "1991-02-02"})
    assert resp.status_code == 200


def test_create_user_invalid_username():
    resp = client.put("/hello/foo123", json={"dateOfBirth": "2000-01-01"})
    assert resp.status_code == 422
    resp = client.put("/hello/foo!", json={"dateOfBirth": "2000-01-01"})
    assert resp.status_code == 422


def test_create_user_invalid_date():
    today = date.today().isoformat()
    future = (date.today() + timedelta(days=1)).isoformat()
    resp = client.put("/hello/baz", json={"dateOfBirth": today})
    assert resp.status_code == 400
    assert "dateOfBirth must be before today" in resp.json()["detail"]
    resp = client.put("/hello/baz", json={"dateOfBirth": future})
    assert resp.status_code == 400
    assert "dateOfBirth must be before today" in resp.json()["detail"]


def test_get_hello_happy_birthday():
    today = date.today()
    dob = today.replace(year=2000).isoformat()
    client.put("/hello/alice", json={"dateOfBirth": dob})
    resp = client.get("/hello/alice")
    assert resp.status_code == 200
    assert "Happy birthday!" in resp.json()["message"]


def test_get_hello_birthday_in_n_days():
    today = date.today()
    n = 5
    future_birthday = today + timedelta(days=n)
    date_of_birth = future_birthday.replace(year=2000).isoformat()
    client.put("/hello/bob", json={"dateOfBirth": date_of_birth})
    resp = client.get("/hello/bob")
    assert resp.status_code == 200
    assert f"Your birthday is in {n} day" in resp.json()["message"]


def test_get_hello_user_not_found():
    resp = client.get("/hello/nouser")
    assert resp.status_code == 404
