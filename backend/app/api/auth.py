"""Authentication routes for login and token issuance."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.config import Settings, get_settings
from app.core.security import create_access_token, verify_password
from app.models.user import User
from app.repositories.users import UserRepository
from app.dependencies import get_user_repository
from app.schemas.auth import LoginRequest, TokenResponse, UserProfile

router = APIRouter(prefix="/auth", tags=["auth"])


def to_user_profile(user: User) -> UserProfile:
    """Convert an internal user record into the public response schema.

    Args:
        user: Repository user record, including internal fields.

    Returns:
        Public user profile with sensitive values omitted.
    """
    return UserProfile(id=user.id, username=user.username, display_name=user.display_name)


@router.post("/login", response_model=TokenResponse)
def login(
    payload: LoginRequest,
    repository: UserRepository = Depends(get_user_repository),
    settings: Settings = Depends(get_settings),
) -> TokenResponse:
    """Validate credentials and issue a bearer token.

    Args:
        payload: Login request body containing username and plaintext password.
        repository: User lookup boundary used to find the login account.
        settings: Runtime settings containing token lifetime and signing secret.

    Raises:
        HTTPException: 401 when the user is unknown, inactive, or password
            verification fails.

    Returns:
        Access token metadata plus the public profile for the authenticated user.
    """
    user = repository.get_user_by_username(payload.username)
    if user is None or not user.is_active or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    expires_in = settings.token_expire_minutes * 60
    token = create_access_token(user.id, settings.token_secret, expires_in)
    return TokenResponse(access_token=token, expires_in=expires_in, user=to_user_profile(user))
