"""FastAPI dependency functions for repositories and authenticated users.

Route modules import these callables with Depends(...) so request handling,
repository selection, token decoding, and user loading stay outside individual
route handlers.
"""

from __future__ import annotations

from functools import lru_cache

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import Settings, get_settings
from app.core.security import TokenError, decode_access_token
from app.models.user import User
from app.repositories.users import DevelopmentUserRepository, PostgreSQLUserRepository, UserRepository

bearer_scheme = HTTPBearer(auto_error=False)


@lru_cache(maxsize=1)
def _get_repository() -> UserRepository:
    """Create the process-wide user repository instance.

    The repository stays behind one cached factory so routes and auth code only
    depend on UserRepository. When DATABASE_URL is configured, PostgreSQL
    becomes the active adapter; otherwise the development repository remains the
    local fallback.
    """
    settings = get_settings()
    return build_user_repository(settings)


def build_user_repository(settings: Settings) -> UserRepository:
    """Select the active repository implementation from runtime settings.

    Args:
        settings: Runtime configuration including the optional DATABASE_URL.

    Returns:
        A PostgreSQL-backed repository when DATABASE_URL is configured;
        otherwise the seeded development repository.
    """
    if settings.database_url:
        return PostgreSQLUserRepository(settings.database_url)
    return DevelopmentUserRepository(settings)


def get_user_repository() -> UserRepository:
    """Return the repository dependency used for user lookups."""
    return _get_repository()


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    repository: UserRepository = Depends(get_user_repository),
    settings: Settings = Depends(get_settings),
) -> User:
    """Resolve the authenticated user for protected endpoints.

    Args:
        credentials: Parsed HTTP Authorization credentials from FastAPI's
            HTTPBearer helper; None when the header is absent.
        repository: User lookup boundary used to load the token subject.
        settings: Runtime settings containing the token signing secret.

    Raises:
        HTTPException: 401 when credentials are missing, invalid, expired, or
            point at an inactive/missing user.

    Returns:
        The active user represented by the validated bearer token.
    """
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        payload = decode_access_token(credentials.credentials, settings.token_secret)
    except TokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from None

    # The token subject is an identifier only; the repository remains the source
    # of truth for current user state such as active/inactive status.
    user = repository.get_user_by_id(str(payload["sub"]))
    if user is None or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user
