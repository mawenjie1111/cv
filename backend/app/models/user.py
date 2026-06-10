"""Domain model for authenticated application users."""

from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    """Internal user record used by authentication and repositories.

    Attributes:
        id: Stable identifier stored as the access-token subject.
        username: Login name and public profile handle.
        display_name: Human-readable name shown by the frontend.
        is_active: Whether the user is allowed to authenticate.
        password_hash: Stored PBKDF2 hash; plaintext passwords are never stored.
    """

    id: str
    username: str
    display_name: str
    is_active: bool
    password_hash: str
