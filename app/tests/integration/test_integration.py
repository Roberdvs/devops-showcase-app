"""
Simple integration tests for critical database and API functionality.
"""

from datetime import date
from app.crud import create_or_update_user, get_user


def test_database_connection(database_session):
    """Test that we can connect to the database."""
    from sqlalchemy import text

    assert database_session is not None
    result = database_session.exec(text("SELECT 1")).first()
    assert result[0] == 1


def test_create_and_get_user(database_session):
    """Test creating and retrieving a user in the database."""
    # Create user
    username = "testuser"
    dob = date(1990, 1, 15)
    create_or_update_user(database_session, username, dob)

    # Retrieve user
    retrieved_user = get_user(database_session, username)
    assert retrieved_user is not None
    assert retrieved_user.username == username
    assert retrieved_user.date_of_birth == dob


def test_health_live_endpoint(client):
    """Test health/live endpoint."""
    response = client.get("/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "OK"


def test_create_and_get_user_via_api(client):
    """Test the complete create and get user flow via API."""
    username = "apitest"
    user_data = {"dateOfBirth": "1995-12-25"}

    # Create user via API
    create_response = client.put(f"/hello/{username}", json=user_data)
    assert create_response.status_code == 200

    # Get user via API
    get_response = client.get(f"/hello/{username}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert "message" in data
    assert username in data["message"]


def test_get_nonexistent_user(client):
    """Test retrieving a user that doesn't exist."""
    response = client.get("/hello/nouser")
    assert response.status_code == 404
