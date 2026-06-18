## Context

The current backend was intentionally built around a replaceable repository boundary and a seeded development adapter. That leaves room for a real SQL-backed implementation, but the project does not yet define what the first PostgreSQL schema should look like. This change narrows that uncertainty by specifying the bootstrap structure for user persistence before repository integration begins.

The request is specific about the user table contents: user ID as the primary key, account, password, permissions, and CV number, plus practical PostgreSQL details such as field types, indexes, comments, and a JSONB extension column. A clean schema should satisfy those requirements while leaving room for future role and profile growth.

## Goals / Non-Goals

**Goals:**

- Define a repeatable PostgreSQL bootstrap approach for a fresh environment.
- Define a `users` table with a primary key, foreign key, unique constraint, lookup indexes, timestamps, and JSONB extensibility.
- Use safe storage semantics for authentication by storing `password_hash` instead of plaintext password values.
- Introduce a concrete `cv_id` foreign key target so referential integrity is enforceable from the first SQL version.
- Keep naming and types straightforward enough to map later into the existing FastAPI repository boundary.

**Non-Goals:**

- No immediate replacement of the in-memory `DevelopmentUserRepository`.
- No ORM selection, migration framework selection, or FastAPI adapter implementation in this change.
- No full CV domain modeling beyond the minimal table needed to anchor `cv_id`.
- No many-to-many permission redesign or authorization policy engine in this first schema.

## Decisions

1. Use PostgreSQL as the first concrete relational store.

   PostgreSQL is a strong fit for authentication and profile workloads because it offers mature relational constraints, `JSONB`, rich indexing options, and clear support for future migrations. This also aligns well with the project's existing plan to keep a swappable repository boundary while choosing a first production-shaped database.

2. Create a dedicated application schema and a minimal CV table.

   The bootstrap should create a dedicated schema such as `cv_app` instead of placing application tables directly into `public`. A minimal `cv_profiles` table is included so the requested `cv_id` field in `users` can be enforced with a true foreign key rather than left as an unchecked scalar.

3. Store account identity and authorization fields directly on `users` for the first version.

   The initial `users` table will include:

   - `user_id`: primary key
   - `username`: login account, unique
   - `password_hash`: stored credential hash
   - `role_code`: coarse-grained user role such as `admin` or `editor`
   - `permission_code`: current effective permission label or tier
   - `cv_id`: optional foreign key to the user's CV/profile record
   - `is_active`: authentication enable/disable flag
   - `ext_attributes`: future-proof JSONB storage
   - `created_at` / `updated_at`: audit timestamps

   This keeps the first schema simple while leaving room to split permissions into normalized tables later if the domain outgrows a single permission field.

4. Use explicit constraints, comments, and indexes from the first version.

   Login and profile lookup will frequently query by `username`, `user_id`, and potentially by `cv_id` or authorization fields. The schema should therefore include a unique constraint on `username`, B-tree indexes for common lookups, and a GIN index on `ext_attributes` for future metadata filtering. `COMMENT` statements are part of the schema contract so the table remains self-describing for maintainers and DBAs.

5. Keep the bootstrap portable by separating database creation from table creation logic.

   Database creation often runs with higher privileges than application migrations. The proposal therefore treats bootstrap as two layers: a one-time database creation step and a repeatable schema/table initialization script executed inside the target database.

## Planned DDL

```sql
CREATE DATABASE cv_app_db
  WITH ENCODING = 'UTF8'
       TEMPLATE = template0;

-- Connect to cv_app_db before running the remaining statements.

CREATE SCHEMA IF NOT EXISTS cv_app;
COMMENT ON SCHEMA cv_app IS 'Application schema for CV platform data.';

CREATE TABLE IF NOT EXISTS cv_app.cv_profiles (
    cv_id BIGSERIAL PRIMARY KEY,
    cv_code VARCHAR(64) NOT NULL UNIQUE,
    title VARCHAR(255),
    ext_attributes JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE cv_app.cv_profiles IS 'Minimal CV profile table used to anchor user-to-CV relationships.';
COMMENT ON COLUMN cv_app.cv_profiles.cv_id IS 'CV primary key.';
COMMENT ON COLUMN cv_app.cv_profiles.cv_code IS 'Business-facing CV identifier.';
COMMENT ON COLUMN cv_app.cv_profiles.title IS 'Optional CV title or summary label.';
COMMENT ON COLUMN cv_app.cv_profiles.ext_attributes IS 'Reserved JSONB extension attributes for future CV metadata.';
COMMENT ON COLUMN cv_app.cv_profiles.created_at IS 'Row creation timestamp.';
COMMENT ON COLUMN cv_app.cv_profiles.updated_at IS 'Row update timestamp.';

CREATE TABLE IF NOT EXISTS cv_app.users (
    user_id BIGSERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password_hash TEXT NOT NULL,
    role_code VARCHAR(64) NOT NULL,
    permission_code VARCHAR(64) NOT NULL,
    cv_id BIGINT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    ext_attributes JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_users_username UNIQUE (username),
    CONSTRAINT fk_users_cv_id
        FOREIGN KEY (cv_id)
        REFERENCES cv_app.cv_profiles (cv_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

COMMENT ON TABLE cv_app.users IS 'Application user account table.';
COMMENT ON COLUMN cv_app.users.user_id IS 'User ID primary key.';
COMMENT ON COLUMN cv_app.users.username IS 'User login account; must be unique.';
COMMENT ON COLUMN cv_app.users.password_hash IS 'Hashed password value; plaintext passwords are never stored.';
COMMENT ON COLUMN cv_app.users.role_code IS 'Coarse-grained user role such as admin or editor.';
COMMENT ON COLUMN cv_app.users.permission_code IS 'Current permission label or access tier.';
COMMENT ON COLUMN cv_app.users.cv_id IS 'Associated CV identifier referencing cv_profiles.cv_id.';
COMMENT ON COLUMN cv_app.users.is_active IS 'Whether the user account is allowed to authenticate.';
COMMENT ON COLUMN cv_app.users.ext_attributes IS 'Reserved JSONB extension attributes for future user metadata.';
COMMENT ON COLUMN cv_app.users.created_at IS 'Row creation timestamp.';
COMMENT ON COLUMN cv_app.users.updated_at IS 'Row update timestamp.';

CREATE INDEX IF NOT EXISTS idx_users_role_code
    ON cv_app.users (role_code);

CREATE INDEX IF NOT EXISTS idx_users_permission_code
    ON cv_app.users (permission_code);

CREATE INDEX IF NOT EXISTS idx_users_cv_id
    ON cv_app.users (cv_id);

CREATE INDEX IF NOT EXISTS idx_users_ext_attributes_gin
    ON cv_app.users
    USING GIN (ext_attributes);

CREATE INDEX IF NOT EXISTS idx_cv_profiles_ext_attributes_gin
    ON cv_app.cv_profiles
    USING GIN (ext_attributes);
```

## Risks / Trade-offs

- A single `permission_code` field may be too limited for future multi-permission authorization -> Mitigation: keep the first schema simple, and reserve later normalization into join tables if required.
- The supporting `cv_profiles` table is intentionally minimal and may not match the final CV domain model -> Mitigation: keep only the fields needed to support referential integrity now.
- `updated_at` is defined but not yet auto-maintained -> Mitigation: add trigger or application-managed updates in the implementation phase.
- Choosing `BIGSERIAL` now may differ from a future UUID strategy -> Mitigation: keep identifier mapping localized inside the eventual PostgreSQL repository adapter.

## Migration Plan

1. Add PostgreSQL bootstrap artifacts under the backend data-access area.
2. Document required bootstrap commands and `DATABASE_URL` examples for local and deployed environments.
3. Create the application schema, `cv_profiles`, and `users` tables with comments, constraints, and indexes.
4. In a later follow-up, implement a PostgreSQL-backed repository that maps this schema into the existing `UserRepository` contract.

Rollback is dropping the new schema or removing the initialization artifacts before production data exists.

## Open Questions

- Should `user_id` remain `BIGSERIAL`, or does the team prefer UUIDs before the first persisted deployment?
- Will one user own at most one CV, or should the longer-term model allow multiple CVs per account?
- Does `permission_code` represent a single effective permission tier, or should follow-up work model many permissions per user?
