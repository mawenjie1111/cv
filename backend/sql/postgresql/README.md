# PostgreSQL Bootstrap

This directory contains the first PostgreSQL bootstrap scripts for the project.

## Files

- `00_create_database.sql`: Creates the `cv_db` database if it does not already exist. Run this script from an administrative connection, for example `postgres`.
- `01_init_schema.sql`: Creates the `cv_app` schema plus the `cv_profiles` and `users` tables, comments, and indexes inside `cv_db`.

## Usage

Create the database:

```bash
psql -U postgres -d postgres -f backend/sql/postgresql/00_create_database.sql
```

Initialize the schema:

```bash
psql -U postgres -d cv_db -f backend/sql/postgresql/01_init_schema.sql
```

## Database URL

Use a PostgreSQL connection string like:

```bash
DATABASE_URL=postgresql://postgres:123456@localhost:5432/cv_db
```

The backend auto-selects its repository based on `DATABASE_URL`. When the URL is set, the PostgreSQL-backed repository reads users from `cv_app.users`; when it is absent, the in-memory development repository remains the fallback.

## Notes

- `users.display_name` is required because the current backend user profile response exposes it to the frontend.
- `password_hash` stores hashed credentials only; never persist plaintext passwords.
- `users.cv_id` is a foreign key to `cv_profiles.cv_id`.
- `ext_attributes` is reserved for future metadata that is not stable enough for dedicated columns yet.

Generate a password hash for manual PostgreSQL seed users with:

```bash
cd backend
python -c "from app.core.security import hash_password; print(hash_password('admin123'))"
```

Example seed insert:

```sql
INSERT INTO cv_app.users (
    username,
    display_name,
    password_hash,
    role_code,
    permission_code,
    cv_id
) VALUES (
    'admin',
    'System Admin',
    'REPLACE_WITH_HASH',
    'admin',
    'manage_users',
    NULL
);
```

## User Table Summary

The `cv_app.users` table created by `01_init_schema.sql` includes:

- Primary key: `user_id BIGSERIAL PRIMARY KEY`
- Foreign key: `cv_id` references `cv_app.cv_profiles(cv_id)`
- Unique login account: `username VARCHAR(255) NOT NULL UNIQUE`
- Password column: `password_hash TEXT NOT NULL`
- Authorization columns: `role_code VARCHAR(64) NOT NULL` and `permission_code VARCHAR(64) NOT NULL`
- Extension storage: `ext_attributes JSONB NOT NULL DEFAULT '{}'::jsonb`
- Audit fields: `created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP` and `updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP`

It also includes:

- Column comments via `COMMENT ON ...`
- Indexes on `role_code`, `permission_code`, `cv_id`
- A GIN index on `ext_attributes`
