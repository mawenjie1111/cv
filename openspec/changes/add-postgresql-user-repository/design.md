## Context

The current backend keeps its authentication logic cleanly separated from persistence through `UserRepository`, but only the in-memory development adapter exists today. A prior PostgreSQL schema proposal established the first SQL shape, yet the application still cannot use it for login. This change closes that gap by planning a PostgreSQL repository implementation and automatic adapter selection driven by `DATABASE_URL`.

There are two important compatibility issues to solve in the same change. First, the current internal `User` model requires `display_name`, but the proposed PostgreSQL `users` table does not yet include it. Second, the frontend currently surfaces whatever error string the backend returns. If the product wants "账号不存在" for unknown accounts, the backend needs a stable, intentional error contract rather than a generic 401 detail for every login failure.

## Goals / Non-Goals

**Goals:**

- Implement a PostgreSQL-backed adapter that satisfies `get_user_by_username` and `get_user_by_id`.
- Auto-select the PostgreSQL adapter whenever `DATABASE_URL` is configured.
- Fail login when the account does not exist in PostgreSQL and surface a distinct account-not-found response the frontend can display directly.
- Continue verifying passwords with the existing password-hash helper instead of introducing plaintext or database-native auth shortcuts.
- Reserve a registration endpoint contract for future account creation without implementing inserts yet.
- Add tests that keep adapter switching and login semantics stable.

**Non-Goals:**

- No ORM adoption; the first adapter can use direct SQL through a lightweight PostgreSQL driver.
- No implementation of user self-registration, password reset, or multi-factor auth.
- No redesign of token creation/validation.
- No full authorization redesign beyond carrying existing role/permission fields through persistence.

## Decisions

1. Use a direct PostgreSQL driver instead of introducing an ORM.

   The existing backend is intentionally dependency-light and built around a small repository abstraction. A direct PostgreSQL driver such as `psycopg` keeps the first SQL adapter simple, explicit, and aligned with the current synchronous request handlers.

2. Auto-switch repositories based on `DATABASE_URL`, but do not silently fall back when the URL is invalid.

   If `DATABASE_URL` is unset, the backend should keep using `DevelopmentUserRepository` for local development. If `DATABASE_URL` is set, the backend should initialize the PostgreSQL adapter and fail clearly if the database is unreachable or the configuration is invalid. Silent fallback would hide production misconfiguration and make debugging much harder.

3. Extend the PostgreSQL `users` table to satisfy the current domain model.

   The repository must return the same internal `User` shape the auth routes already expect. That means the PostgreSQL schema needs at least:

   - `user_id`
   - `username`
   - `display_name`
   - `password_hash`
   - `is_active`
   - `role_code`
   - `permission_code`
   - `cv_id`
   - `ext_attributes`
   - `created_at` / `updated_at`

   This change should therefore amend the prior SQL plan by adding `display_name VARCHAR(255) NOT NULL`.

4. Use structured login failure semantics for unknown accounts.

   The backend should intentionally distinguish between "account not found" and "password incorrect" outcomes because the requested frontend behavior depends on it. To keep the contract stable, the response should include a machine-readable code in addition to a human-readable message. A practical first version is:

   - unknown account -> `401` with code `account_not_found`
   - wrong password -> `401` with code `invalid_password`
   - inactive account -> `401` with code `account_disabled`

   This is a deliberate product trade-off because it reveals account existence. The change accepts that trade-off explicitly instead of doing it accidentally.

5. Reserve registration with a stable endpoint that is not implemented yet.

   A placeholder `POST /api/auth/register` endpoint, request schema, and response contract should be introduced now so frontend and backend work can converge on one path later. Until account creation is implemented, the endpoint should return a consistent "not implemented" response such as `501 Not Implemented`.

## Architecture Outline

### Repository selection

- `get_user_repository()` keeps the existing boundary.
- A repository factory checks `settings.database_url`.
- When absent: return `DevelopmentUserRepository`.
- When present: return `PostgreSQLUserRepository`.

### PostgreSQL repository responsibilities

- Parse and store the configured `DATABASE_URL`.
- Query `cv_app.users` by `username` for login and by `user_id` for token subject resolution.
- Map database rows into the existing `app.models.user.User`.
- Leave password verification in `app.core.security.verify_password`.
- Return `None` for unknown accounts or missing user IDs.

### Login error contract

The login handler should stop collapsing all failures into `"Invalid credentials"` and instead return a structured payload that the frontend can surface. One example contract is:

```json
{
  "detail": "Account not found",
  "error_code": "account_not_found"
}
```

The frontend auth store can then map `account_not_found` to a localized message such as `账号不存在`.

### Registration placeholder

- Route: `POST /api/auth/register`
- Request: reserve fields such as `username`, `password`, and `display_name`
- Current behavior: return `501 Not Implemented`
- Future follow-up: validate uniqueness, hash password, insert into PostgreSQL, and optionally create default CV/profile linkage

## Risks / Trade-offs

- Distinguishing unknown accounts from bad passwords leaks account existence -> Mitigation: treat this as an explicit product requirement and document it clearly.
- Direct SQL requires careful row-to-model mapping -> Mitigation: keep queries small, typed, and covered by focused tests.
- Schema drift may occur between the earlier PostgreSQL proposal and the repository's actual field needs -> Mitigation: include the `display_name` schema amendment in this change instead of relying on implicit assumptions.
- A configured but broken `DATABASE_URL` could prevent startup or login -> Mitigation: prefer fast, clear failure over silent fallback to development data.

## Migration Plan

1. Add PostgreSQL driver dependency and repository implementation.
2. Amend the PostgreSQL schema definition to include `display_name` on persisted users.
3. Update dependency selection to choose PostgreSQL when `DATABASE_URL` is present.
4. Update login error responses and frontend error handling for account-not-found behavior.
5. Add a registration placeholder endpoint, schemas, tests, and documentation.

Rollback can restore the development-only repository factory and remove the PostgreSQL adapter path while preserving existing token behavior.

## Open Questions

- Should the frontend display the backend-provided message directly, or should it map `error_code` values to localized Chinese copy client-side?
- Should the registration placeholder be exposed publicly now, or should it exist behind a feature flag until account creation work starts?
- Do we want a helper command or script to generate `password_hash` values for manually seeded PostgreSQL users before registration exists?
