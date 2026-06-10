"""Health-check route for uptime and local smoke tests."""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    """Return a simple API-running signal.

    Returns:
        A stable JSON object used by tests, local checks, and load balancers.
    """
    return {"status": "ok"}
