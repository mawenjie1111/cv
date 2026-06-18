## 1. Repository Integration

- [x] 1.1 Add a PostgreSQL driver dependency that fits the current synchronous FastAPI backend.
- [x] 1.2 Implement `PostgreSQLUserRepository` with username and user-ID lookup against `cv_app.users`.
- [x] 1.3 Update repository factory logic to auto-select PostgreSQL when `DATABASE_URL` is configured and keep the development adapter only as the no-database fallback.

## 2. Schema Alignment

- [x] 2.1 Amend PostgreSQL bootstrap SQL so `cv_app.users` includes `display_name` required by the current backend `User` model.
- [x] 2.2 Document how persisted user rows should store `password_hash` and `is_active`.
- [x] 2.3 Add a documented way to prepare PostgreSQL test or seed users before registration exists.

## 3. Authentication Contract

- [x] 3.1 Update login flow to distinguish unknown account, wrong password, and inactive-account failures with stable response fields.
- [x] 3.2 Update frontend login error handling so unknown accounts display an explicit account-not-found message.
- [x] 3.3 Add or update backend and frontend verification coverage for PostgreSQL-backed login behavior.

## 4. Registration Placeholder

- [x] 4.1 Reserve a `POST /api/auth/register` backend route and request/response schema.
- [x] 4.2 Return a stable not-implemented response until account creation is built.
- [x] 4.3 Document follow-up implementation work for actual user creation, password hashing, and uniqueness checks.
