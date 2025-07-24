import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_put_and_get_hello(monkeypatch):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Insert user
        resp = await ac.put("/hello/testuser", json={"dateOfBirth": "2000-01-01"})
        assert resp.status_code == 204
        # Get user
        resp = await ac.get("/hello/testuser")
        assert resp.status_code == 200
        assert "Hello, testuser!" in resp.json()["message"] 