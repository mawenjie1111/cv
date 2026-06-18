"""Repository boundary exports.

Routes and services depend on UserRepository instead of a concrete database so
the development and PostgreSQL adapters can be swapped without changing route
behavior.
"""

from app.repositories.users import DevelopmentUserRepository, PostgreSQLUserRepository, UserRepository

__all__ = ["DevelopmentUserRepository", "PostgreSQLUserRepository", "UserRepository"]
