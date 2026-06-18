"""Authentication request and response schemas.

These Pydantic models define the public JSON shape exposed by auth and user
routes. They intentionally exclude internal fields such as password_hash.
"""

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """JSON payload accepted by POST /api/auth/login.

    Attributes:
        username: Login name to look up through the user repository.
        password: Plaintext candidate password verified against the stored hash.
    """

    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class RegistrationRequest(BaseModel):
    """JSON payload reserved for future POST /api/auth/register support."""

    username: str = Field(min_length=1)
    password: str = Field(min_length=1)
    display_name: str = Field(min_length=1)


class UserProfile(BaseModel):
    """Public user data returned to the frontend."""

    id: str
    username: str
    display_name: str


class TokenResponse(BaseModel):
    """Successful login response.

    Attributes:
        access_token: Signed bearer token used for protected API requests.
        token_type: Authentication scheme clients place before the token.
        expires_in: Token lifetime in seconds.
        user: Public profile for the authenticated user.
    """

    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserProfile


class AuthErrorResponse(BaseModel):
    """Structured authentication error payload surfaced to the frontend."""

    detail: str
    error_code: str
