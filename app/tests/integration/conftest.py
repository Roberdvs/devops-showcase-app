"""
Integration test configuration and fixtures.
Uses Testcontainers to spin up a real PostgreSQL instance for testing.
"""

import pytest
from fastapi.testclient import TestClient
from testcontainers.postgres import PostgresContainer
from sqlmodel import Session, create_engine, SQLModel
from main import app
from app.database import get_session
from app.models import User


@pytest.fixture(scope="session")
def postgres_container():
    """Start PostgreSQL container for integration tests."""
    with PostgresContainer("postgres:15") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def database_engine(postgres_container):
    """Create database engine with test container."""
    database_url = postgres_container.get_connection_url()
    engine = create_engine(database_url, echo=False)

    # Create tables using SQLModel
    SQLModel.metadata.create_all(engine)

    return engine


@pytest.fixture
def database_session(database_engine):
    """Create database session for each test."""
    from sqlmodel import select

    with Session(database_engine) as session:
        yield session
        # Cleanup after each test
        users = session.exec(select(User)).all()
        for user in users:
            session.delete(user)
        session.commit()


@pytest.fixture
def client(database_engine):
    """Create test client with real database."""
    from contextlib import asynccontextmanager

    # Create a test lifespan that doesn't initialize the database
    @asynccontextmanager
    async def test_lifespan(_app):
        yield

    # Temporarily replace the lifespan
    original_lifespan = app.router.lifespan_context
    app.router.lifespan_context = test_lifespan

    def override_get_session():
        with Session(database_engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as test_client:
        yield test_client

    # Restore original lifespan and clear overrides
    app.router.lifespan_context = original_lifespan
    app.dependency_overrides.clear()
