"""Protected user routes that require a valid bearer token."""

from fastapi import APIRouter, Depends

from app.api.auth import to_user_profile
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth import UserProfile

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserProfile)
def read_current_user(current_user: User = Depends(get_current_user)) -> UserProfile:
    """Return the profile represented by the validated access token.

    Args:
        current_user: Active user resolved by the get_current_user dependency.

    Returns:
        Public profile for the authenticated user.
    """
    return to_user_profile(current_user)
