from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool
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


# Dependency override
def get_session_override():
    with Session(engine) as session:
        yield session


app.dependency_overrides[database.get_session] = get_session_override

client = TestClient(app)


def test_put_and_get_hello():
    resp = client.put("/hello/testuser", json={"dateOfBirth": "2000-01-01"})
    assert resp.status_code == 200
    resp = client.get("/hello/testuser")
    assert resp.status_code == 200
    assert "Hello, testuser!" in resp.json()["message"]
