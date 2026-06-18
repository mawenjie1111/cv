"""User repository contract plus development and PostgreSQL adapters.

Authentication code reads users through this boundary. The in-memory
DevelopmentUserRepository supports local login without a database, while the
PostgreSQLUserRepository loads persisted users when DATABASE_URL is configured.
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


class PostgreSQLUserRepository:
    """Read user records from PostgreSQL using the existing UserRepository contract."""

    def __init__(self, database_url: str) -> None:
        """Store the PostgreSQL connection URL for later user lookups.

        Args:
            database_url: PostgreSQL connection string from runtime settings.

        Raises:
            ValueError: If the connection string is blank.
            RuntimeError: If the PostgreSQL driver is unavailable.
        """
        if not database_url.strip():
            raise ValueError("DATABASE_URL must not be blank when PostgreSQL is enabled")

        self._database_url = database_url
        self._load_driver()

    def _load_driver(self):
        """Import psycopg lazily so development mode works without database access."""
        try:
            import psycopg
        except ImportError as exc:
            raise RuntimeError(
                "psycopg is required for PostgreSQL-backed user authentication"
            ) from exc
        return psycopg

    def _fetch_user(self, query: str, parameter: object) -> User | None:
        """Execute a single-row lookup and map the result into the internal User model."""
        psycopg = self._load_driver()
        with psycopg.connect(self._database_url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (parameter,))
                row = cursor.fetchone()
        if row is None:
            return None

        user_id, username, display_name, is_active, password_hash = row
        return User(
            id=str(user_id),
            username=username,
            display_name=display_name,
            is_active=is_active,
            password_hash=password_hash,
        )

    def get_user_by_username(self, username: str) -> User | None:
        """Find a persisted PostgreSQL user by login username."""
        return self._fetch_user(
            """
            SELECT user_id, username, display_name, is_active, password_hash
            FROM cv_app.users
            WHERE username = %s
            """,
            username,
        )

    def get_user_by_id(self, user_id: str) -> User | None:
        """Find a persisted PostgreSQL user by stable identifier."""
        try:
            user_id_value = int(user_id)
        except (TypeError, ValueError):
            return None

        return self._fetch_user(
            """
            SELECT user_id, username, display_name, is_active, password_hash
            FROM cv_app.users
            WHERE user_id = %s
            """,
            user_id_value,
        )
