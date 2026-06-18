## Why

The backend currently authenticates against an in-memory development repository and exposes `DATABASE_URL` only as a placeholder. The project now needs a concrete PostgreSQL bootstrap plan so user accounts can be stored in a durable relational schema without improvising table structure later.

The requested user table also needs to be production-shaped from the beginning: a primary key, a foreign key for CV ownership, practical indexes for login and lookup paths, timestamp columns, column comments, and a JSONB extension field for future attributes that are not stable enough to model yet.

## What Changes

- Add an OpenSpec change that defines the first PostgreSQL initialization flow for this project.
- Introduce a PostgreSQL schema plan with a `users` table for account storage and a minimal supporting `cv_profiles` table so `cv_id` can be enforced as a real foreign key.
- Define required user columns including `user_id`, `username`, `password_hash`, `role_code`, `permission_code`, `cv_id`, timestamps, and `ext_attributes`.
- Require primary key, unique constraint, foreign key, targeted indexes, JSONB extensibility, and `COMMENT` metadata for the table and columns.
- Keep the scope focused on database bootstrap and schema design; wiring the FastAPI repository boundary to PostgreSQL can follow in implementation work.

## Capabilities

### New Capabilities

- `postgresql-user-storage`: Covers PostgreSQL database initialization artifacts and the concrete relational schema for user account persistence.

### Modified Capabilities

- None.

## Impact

- Adds a concrete storage contract for PostgreSQL-backed user accounts.
- Establishes a stable `cv_id` relationship instead of leaving the future CV linkage implicit.
- Improves future migration readiness by standardizing comments, indexes, and extension storage from the first schema version.
- Does not yet change authentication route behavior, token semantics, or the currently active in-memory development adapter.
