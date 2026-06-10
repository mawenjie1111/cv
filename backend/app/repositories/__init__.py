"""Repository boundary exports.

Routes and services depend on UserRepository instead of a concrete database so
the development adapter can be replaced later without changing route behavior.
"""

from app.repositories.users import DevelopmentUserRepository, UserRepository

__all__ = ["DevelopmentUserRepository", "UserRepository"]
