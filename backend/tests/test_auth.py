"""Behavior tests for the backend authentication API.

These tests document the public contracts that should remain unchanged when
implementation details, comments, or repository adapters evolve.
"""

from fastapi.testclient import TestClient

from app.main import create_app


client = TestClient(create_app())


def test_health_check():
    """The health endpoint returns the stable API-running payload."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_successful_login_returns_token_and_user():
    """Valid seeded credentials produce a bearer token and public user data."""
    response = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    assert response.status_code == 200
    body = response.json()
    assert body["access_token"]
    assert body["token_type"] == "bearer"
    assert body["expires_in"] == 3600
    assert body["user"]["username"] == "admin"


def test_failed_login_rejects_credentials():
    """Invalid passwords must not receive an access token."""
    response = client.post("/api/auth/login", json={"username": "admin", "password": "wrong"})
    assert response.status_code == 401
    assert "access_token" not in response.text


def test_protected_endpoint_requires_token():
    """Protected routes reject requests that omit Authorization credentials."""
    response = client.get("/api/users/me")
    assert response.status_code == 401


def test_protected_endpoint_rejects_invalid_token():
    """Protected routes reject malformed or unverifiable bearer tokens."""
    response = client.get("/api/users/me", headers={"Authorization": "Bearer invalid"})
    assert response.status_code == 401


def test_current_user_with_valid_token():
    """A token returned by login can read the current user's public profile."""
    login_response = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    token = login_response.json()["access_token"]

    response = client.get("/api/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "admin"
