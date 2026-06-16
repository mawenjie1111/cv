## Why

The project needs a usable web application foundation with a Python API backend and a Vue frontend so future features can be added without reworking the stack. User login is the first cross-cutting capability because it establishes identity, session handling, protected API access, and the database boundary that later modules will depend on.

## What Changes

- Add a FastAPI backend structure with health checks, authentication endpoints, protected user profile access, and clear module boundaries.
- Add a Vue frontend structure with login page, authenticated app shell, API client, route protection, and persisted login state.
- Implement user login using password verification and token-based authentication.
- Reserve database integration behind repository/session interfaces so the first version can run with a development implementation while remaining ready for a real database adapter.
- Add environment-based configuration for API settings, token signing, CORS, and database connection values.
- Add focused tests for authentication success, authentication failure, protected endpoint access, and frontend login flow behavior where practical.

## Capabilities

### New Capabilities

- `user-authentication`: Covers login, logout, token issuance, token validation, current-user retrieval, and protected route/API access.
- `web-application-shell`: Covers the FastAPI and Vue application skeleton, frontend routing, API integration, and authenticated page layout.
- `database-adapter-boundary`: Covers the reserved database interface for user lookup and future persistence without coupling authentication logic to a concrete database.

### Modified Capabilities

- None.

## Impact

- Adds backend Python/FastAPI application files, dependency declarations, configuration, and tests.
- Adds frontend Vue application files, package configuration, authentication views/state, routing, and API client code.
- Introduces authentication API endpoints such as login and current-user profile retrieval.
- Introduces configurable CORS, token secret, token expiration, and database connection placeholders.
- Establishes a repository/database boundary that later implementation can replace with PostgreSQL, MySQL, SQLite, or another supported adapter.
