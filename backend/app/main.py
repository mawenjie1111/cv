"""FastAPI application factory and runtime entrypoint.

This module wires middleware and route packages into a single ASGI app. Keep
route registration here so tests and the development server build the same app.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, health, users
from app.config import get_settings


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        A FastAPI app with CORS middleware and all API routers registered under
        the configured API prefix.
    """
    settings = get_settings()
    app = FastAPI(title=settings.app_name)

    # CORS origins come from environment-backed settings so the Vue dev server
    # can call the API locally and deployments can tighten the allowed origins.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # All routers share the same configurable API prefix, defaulting to /api.
    app.include_router(health.router, prefix=settings.api_prefix)
    app.include_router(auth.router, prefix=settings.api_prefix)
    app.include_router(users.router, prefix=settings.api_prefix)
    return app


app = create_app()
