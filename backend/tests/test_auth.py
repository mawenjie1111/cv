"""Behavior tests for the backend authentication API.

These tests document the public contracts that should remain unchanged when
implementation details, comments, or repository adapters evolve.
"""

from fastapi.testclient import TestClient

from app import dependencies
from app.config import Settings
from app.main import create_app
from app.repositories.users import DevelopmentUserRepository


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


def test_failed_login_rejects_unknown_account():
    """Unknown usernames return a stable account-not-found authentication error."""
    response = client.post("/api/auth/login", json={"username": "missing-user", "password": "admin123"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Account not found", "error_code": "account_not_found"}


def test_failed_login_rejects_invalid_password():
    """Invalid passwords must not receive an access token."""
    response = client.post("/api/auth/login", json={"username": "admin", "password": "wrong"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid password", "error_code": "invalid_password"}


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


def test_registration_placeholder_returns_not_implemented():
    """The reserved registration route exists before account creation is implemented."""
    response = client.post(
        "/api/auth/register",
        json={"username": "new-user", "password": "password123", "display_name": "New User"},
    )
    assert response.status_code == 501
    assert response.json() == {
        "detail": "Registration is not implemented yet",
        "error_code": "registration_not_implemented",
    }


def test_repository_factory_uses_development_adapter_without_database_url():
    """Local development still falls back to the seeded in-memory repository."""
    dependencies._get_repository.cache_clear()
    repository = dependencies.build_user_repository(Settings(database_url=None))
    assert isinstance(repository, DevelopmentUserRepository)


def test_repository_factory_uses_postgresql_adapter_when_database_url(monkeypatch):
    """A configured DATABASE_URL switches repository selection to PostgreSQL."""

    class FakePostgreSQLUserRepository:
        def __init__(self, database_url: str) -> None:
            self.database_url = database_url

    dependencies._get_repository.cache_clear()
    monkeypatch.setattr(dependencies, "PostgreSQLUserRepository", FakePostgreSQLUserRepository)

    repository = dependencies.build_user_repository(
        Settings(database_url="postgresql://cv_app:secret@localhost:5432/cv_app_db")
    )

    assert isinstance(repository, FakePostgreSQLUserRepository)
    assert repository.database_url == "postgresql://cv_app:secret@localhost:5432/cv_app_db"
