"""Environment-backed backend settings.

The application keeps configuration in a small dataclass so route handlers and
dependencies can receive typed settings without depending directly on os.environ.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


def _get_int(name: str, default: int) -> int:
    """Read an integer environment variable.

    Args:
        name: Environment variable name to inspect.
        default: Value returned when the variable is missing or empty.

    Raises:
        ValueError: If the variable is present but cannot be parsed as an int.
    """
    raw = os.getenv(name)
    if raw is None or raw == "":
        return default
    try:
        return int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc


def _get_csv(name: str, default: list[str]) -> list[str]:
    """Read a comma-separated environment variable as a list of strings.

    Args:
        name: Environment variable name to inspect.
        default: Value returned when the variable is missing or blank.

    Returns:
        Non-empty, stripped comma-separated values.
    """
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    return [item.strip() for item in raw.split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
    """Runtime configuration consumed by API setup and auth dependencies.

    Attributes:
        app_name: Display name used for FastAPI metadata.
        api_prefix: URL prefix shared by all API routers.
        token_secret: HMAC secret used to sign access tokens.
        token_expire_minutes: Access token lifetime in minutes.
        cors_origins: Browser origins allowed to call the API.
        database_url: Optional placeholder for a future database-backed adapter.
        dev_user_*: Seeded development user values used by the local repository.
    """

    app_name: str = os.getenv("APP_NAME", "FastAPI Vue Login")
    api_prefix: str = os.getenv("API_PREFIX", "/api")
    token_secret: str = os.getenv("TOKEN_SECRET", "change-this-local-secret")
    token_expire_minutes: int = _get_int("TOKEN_EXPIRE_MINUTES", 60)
    cors_origins: list[str] = None  # type: ignore[assignment]
    database_url: str | None = os.getenv("DATABASE_URL") or None
    dev_user_id: str = os.getenv("DEV_USER_ID", "dev-user-1")
    dev_username: str = os.getenv("DEV_USERNAME", "admin")
    dev_password: str = os.getenv("DEV_PASSWORD", "admin123")
    dev_display_name: str = os.getenv("DEV_DISPLAY_NAME", "Development Admin")

    def __post_init__(self) -> None:
        """Populate list defaults that cannot be safely declared inline."""
        if self.cors_origins is None:
            object.__setattr__(
                self,
                "cors_origins",
                _get_csv("CORS_ORIGINS", ["http://localhost:5173", "http://127.0.0.1:5173"]),
            )


def get_settings() -> Settings:
    """Build a Settings instance from the current process environment."""
    return Settings()
