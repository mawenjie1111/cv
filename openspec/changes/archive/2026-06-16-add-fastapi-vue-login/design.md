## Context

This change introduces a full-stack web application foundation built with FastAPI, Python, and Vue. The current proposal requires a usable login flow, protected application area, and a database boundary that can be connected to a real persistence layer later without rewriting authentication logic.

The implementation should favor a small but production-shaped structure: backend modules for configuration, API routes, authentication services, schemas, and repository interfaces; frontend modules for routing, API access, authentication state, and views. The first implementation can use an in-memory or file-backed development repository if no database is configured, but all user lookup and persistence access must flow through the same database adapter boundary expected by a future SQL implementation.

## Goals / Non-Goals

**Goals:**

- Provide a FastAPI backend with authentication endpoints, token validation, CORS configuration, and protected user profile access.
- Provide a Vue frontend with a login screen, authenticated route guard, API client, persisted token handling, and a basic authenticated page.
- Keep password verification and token handling on the server side, with frontend code only storing and presenting authentication state.
- Reserve a database interface for user lookup and future persistence while keeping the initial implementation runnable without a deployed database.
- Add tests or verification coverage for successful login, failed login, protected API access, and frontend route/auth behavior where practical.

**Non-Goals:**

- Full user registration, password reset, email verification, MFA, role-based authorization, or account administration.
- A production migration system or concrete production database deployment.
- OAuth, SSO, or third-party identity provider integration.
- A broad design system or complex dashboard beyond the minimum authenticated shell.

## Decisions

1. Use FastAPI as the backend API framework.

   FastAPI provides typed request/response schemas, dependency injection, OpenAPI docs, and simple testability through its test client. Alternatives considered were Flask and Django. Flask is lighter but would require more manual validation and OpenAPI plumbing; Django is strong for database-backed applications but heavier than needed for a small API-first foundation.

2. Use token-based authentication with server-issued signed access tokens.

   The login endpoint will validate credentials and return an access token plus basic user metadata. Protected endpoints will require an `Authorization: Bearer <token>` header. This fits Vue API calls and keeps the backend stateless for the initial version. Alternatives considered were cookie sessions and server-side sessions. Cookie sessions can be a good production option but need additional CSRF and deployment decisions; server-side sessions introduce persistence before the database boundary is finalized.

3. Store frontend authentication state through a small auth store and API client wrapper.

   The Vue app will centralize token persistence, logout, current-user loading, and route guard decisions. Components will not call `fetch` directly for protected API access. This keeps authentication behavior consistent and makes later changes, such as cookie-based auth or refresh tokens, localized.

4. Define a repository/database adapter boundary before selecting the final database.

   The backend will depend on an abstract user repository or protocol for operations such as `get_user_by_username` and `get_user_by_id`. A development adapter can provide seeded users. A future SQL adapter can implement the same interface using SQLAlchemy, SQLModel, asyncpg, or another concrete library. This avoids scattering placeholder data access through route handlers.

5. Keep configuration environment-driven.

   Backend settings will include token secret, token expiration, CORS origins, database URL placeholder, and development seed credentials. Frontend settings will include the API base URL. This allows local development and later deployment without source changes.

## Risks / Trade-offs

- Development repository mistaken for production storage -> Make the development adapter explicit, document required production settings, and keep database URL configuration visible.
- Token stored in browser storage can be exposed by XSS -> Keep the frontend simple and avoid unsafe HTML rendering; document that cookie/refresh-token hardening is a future production enhancement.
- Login scope expands into account management -> Keep registration, password reset, MFA, and authorization roles out of this change unless later specs add them.
- Placeholder database adapter lacks real migration coverage -> Keep repository interfaces and tests focused so replacing the adapter does not alter API behavior.
- CORS misconfiguration blocks local development -> Provide default local origins for the Vue dev server and expose settings through environment variables.

## Migration Plan

1. Add backend and frontend project structure without replacing unrelated existing code.
2. Implement development authentication with a seeded user repository and signed access tokens.
3. Connect Vue login flow to the FastAPI endpoints and guard authenticated routes.
4. Add tests and run backend/frontend verification commands available in the repo.
5. When a real database is chosen, add a concrete adapter implementing the same repository contract and update environment configuration.

Rollback is straightforward while this remains a new application foundation: remove the new backend/frontend files and OpenSpec change artifacts, or disable the new routes from the application entrypoint.

## Open Questions

- Which production database should the first concrete adapter target: PostgreSQL, MySQL, SQLite, or another system?
- Should production authentication remain bearer-token based, or should it later move to secure HTTP-only cookies with refresh tokens?
- What user fields are required beyond id, username, display name, active status, and password hash?
