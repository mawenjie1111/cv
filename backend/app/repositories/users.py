"""User repository contract and development adapter.

Authentication code reads users through this boundary. The in-memory
DevelopmentUserRepository is sufficient for local login while leaving a clear
contract for a future SQL-backed adapter.
"""

from __future__ import annotations

from typing import Protocol

from app.config import Settings
from app.core.security import hash_password
from app.models.user import User


class UserRepository(Protocol):
    """Lookup operations required by authentication flows."""

    def get_user_by_username(self, username: str) -> User | None:
        """Return a user by login username, or None when it is unknown."""
        ...

    def get_user_by_id(self, user_id: str) -> User | None:
        """Return a user by stable identifier, or None when it is unknown."""
        ...


class DevelopmentUserRepository:
    """In-memory development adapter seeded from environment-backed settings."""

    def __init__(self, settings: Settings) -> None:
        """Create a local repository with one seeded development user.

        Args:
            settings: Runtime settings containing seeded user identity and
                password values.
        """
        password_hash = hash_password(settings.dev_password, salt="development-seed")
        self._users = {
            settings.dev_user_id: User(
                id=settings.dev_user_id,
                username=settings.dev_username,
                display_name=settings.dev_display_name,
                is_active=True,
                password_hash=password_hash,
            )
        }
        self._username_index = {user.username: user.id for user in self._users.values()}

    def get_user_by_username(self, username: str) -> User | None:
        """Find the seeded user by username for login credential checks."""
        user_id = self._username_index.get(username)
        if user_id is None:
            return None
        return self._users.get(user_id)

    def get_user_by_id(self, user_id: str) -> User | None:
        """Find the seeded user by id for token subject resolution."""
        return self._users.get(user_id)
