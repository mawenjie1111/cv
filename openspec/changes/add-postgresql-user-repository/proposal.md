## Why

The backend currently authenticates against `DevelopmentUserRepository`, which keeps one seeded user in memory and ignores the PostgreSQL bootstrap work that has already been proposed. To move the application toward durable authentication, the user module now needs a real PostgreSQL-backed repository that can read persisted user records, validate passwords, and become the active adapter automatically when `DATABASE_URL` is configured.

The login flow also needs one product-specific behavior change: when a submitted account does not exist, the frontend should be able to show an explicit "账号不存在" style error instead of collapsing every failure into a generic invalid-credentials message. At the same time, the project wants to reserve a registration API boundary now without implementing account creation yet.

## What Changes

- Add a PostgreSQL-backed user repository implementation for backend authentication lookups by username and user ID.
- Update dependency selection so the backend automatically uses PostgreSQL when `DATABASE_URL` is set and falls back to the development repository only when it is absent.
- Align the PostgreSQL user schema with the current backend domain model by ensuring persisted users include `display_name` and `is_active` in addition to authentication fields.
- Update the login contract so nonexistent accounts return a frontend-usable account-not-found response while password mismatches still fail authentication.
- Reserve a registration endpoint and request/response schema boundary without implementing the write path yet.
- Add focused tests and documentation for repository switching, PostgreSQL login behavior, and the registration placeholder contract.

## Capabilities

### New Capabilities

- `registration-interface-placeholder`: Covers reserving a stable user registration API boundary before account creation is implemented.

### Modified Capabilities

- `database-adapter-boundary`: Extends the repository boundary from a placeholder into an auto-selected PostgreSQL adapter path.
- `user-authentication`: Extends login behavior to support PostgreSQL-backed user lookup and explicit account-not-found feedback.
- `postgresql-user-storage`: Extends the PostgreSQL schema contract so it can fully satisfy the existing backend `User` domain model.

## Impact

- Affects backend repository selection, PostgreSQL data access, login error responses, and backend tests.
- Requires a small PostgreSQL schema adjustment so persisted users can provide the current public profile fields.
- Affects frontend login error presentation because the backend will return a distinct account-not-found outcome.
- Does not yet implement user self-registration or replace token semantics.
