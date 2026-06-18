"""Authentication routes for login, token issuance, and reserved registration."""

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.config import Settings, get_settings
from app.core.security import create_access_token, verify_password
from app.models.user import User
from app.repositories.users import UserRepository
from app.dependencies import get_user_repository
from app.schemas.auth import AuthErrorResponse, LoginRequest, RegistrationRequest, TokenResponse, UserProfile

router = APIRouter(prefix="/auth", tags=["auth"])


def to_user_profile(user: User) -> UserProfile:
    """Convert an internal user record into the public response schema.

    Args:
        user: Repository user record, including internal fields.

    Returns:
        Public user profile with sensitive values omitted.
    """
    return UserProfile(id=user.id, username=user.username, display_name=user.display_name)


def auth_error(detail: str, error_code: str, status_code: int = status.HTTP_401_UNAUTHORIZED) -> JSONResponse:
    """Build a stable structured authentication error response."""
    return JSONResponse(status_code=status_code, content={"detail": detail, "error_code": error_code})


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
    if user is None:
        return auth_error("Account not found", "account_not_found")
    if not user.is_active:
        return auth_error("Account disabled", "account_disabled")
    if not verify_password(payload.password, user.password_hash):
        return auth_error("Invalid password", "invalid_password")

    expires_in = settings.token_expire_minutes * 60
    token = create_access_token(user.id, settings.token_secret, expires_in)
    return TokenResponse(access_token=token, expires_in=expires_in, user=to_user_profile(user))


@router.post(
    "/register",
    response_model=AuthErrorResponse,
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
)
def register(payload: RegistrationRequest) -> JSONResponse:
    """Reserve the registration endpoint before account creation is implemented.

    Args:
        payload: Future registration input; currently validated but unused.

    Returns:
        Stable not-implemented payload for clients integrating ahead of full registration support.
    """
    _ = payload
    return auth_error(
        "Registration is not implemented yet",
        "registration_not_implemented",
        status.HTTP_501_NOT_IMPLEMENTED,
    )
