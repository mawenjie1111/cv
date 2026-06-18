# PostgreSQL Bootstrap

This directory contains the first PostgreSQL bootstrap scripts for the project.

## Files

- `00_create_database.sql`: Creates the `cv_app_db` database if it does not already exist. Run this script from an administrative connection, for example `postgres`.
- `01_init_schema.sql`: Creates the `cv_app` schema plus the `cv_profiles` and `users` tables, comments, and indexes inside `cv_app_db`.

## Usage

Create the database:

```bash
psql -U postgres -d postgres -f backend/sql/postgresql/00_create_database.sql
```

Initialize the schema:

```bash
psql -U postgres -d cv_app_db -f backend/sql/postgresql/01_init_schema.sql
```

## Database URL

Use a PostgreSQL connection string like:

```bash
DATABASE_URL=postgresql://cv_app:change-me@localhost:5432/cv_app_db
```

The backend still uses `DevelopmentUserRepository` today. A follow-up implementation needs to add a PostgreSQL-backed repository adapter and switch `backend/app/dependencies.py` to use it when `DATABASE_URL` is configured.

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
