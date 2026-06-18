# FastAPI Vue Login

This project contains a FastAPI backend and Vue frontend with a basic login flow, protected API access, and a replaceable database adapter boundary.

## Structure

- `backend/`: FastAPI application, authentication services, repository boundary, and backend tests.
- `frontend/`: Vue/Vite application, login screen, authenticated route, API client, and frontend verification script.
- `openspec/changes/add-fastapi-vue-login/`: OpenSpec proposal, design, specs, and implementation tasks.

## Local Backend

```bash
cd backend
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000` by default. Health check:

```bash
curl http://localhost:8000/api/health
```

## Local Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at `http://localhost:5173` by default and calls `http://localhost:8000/api`.

## Development Login

The default development adapter seeds one user:

- Username: `admin`
- Password: `admin123`

Override these with backend environment variables from `backend/.env.example`.

## Database Adapter Boundary

Authentication routes call the `UserRepository` interface in `backend/app/repositories/users.py`. The current `DevelopmentUserRepository` keeps local seeded users in memory. To connect a real database, add a new repository implementing:

- `get_user_by_username(username)`
- `get_user_by_id(user_id)`

The backend now auto-selects its repository based on `DATABASE_URL`:

- When `DATABASE_URL` is unset, it uses `DevelopmentUserRepository`.
- When `DATABASE_URL` is set, it uses the PostgreSQL-backed repository and reads users from `cv_app.users`.

## PostgreSQL Bootstrap

The repository now includes initial PostgreSQL bootstrap scripts under `backend/sql/postgresql/`:

- `backend/sql/postgresql/00_create_database.sql`: creates `cv_db` if it does not already exist.
- `backend/sql/postgresql/01_init_schema.sql`: creates the `cv_app` schema plus `cv_profiles` and `users` tables, constraints, comments, and indexes.

Example bootstrap commands:

```bash
psql -U postgres -d postgres -f backend/sql/postgresql/00_create_database.sql
psql -U postgres -d cv_db -f backend/sql/postgresql/01_init_schema.sql
```

Example PostgreSQL connection string:

```bash
DATABASE_URL=postgresql://postgres:123456@localhost:5432/cv_db
```

Seed PostgreSQL users with hashed passwords only:

```bash
cd backend
python -c "from app.core.security import hash_password; print(hash_password('admin123'))"
```

The `users` table now includes `display_name` because authenticated profile responses expose that field to the frontend.

## Authentication Notes

- Unknown usernames return `error_code: account_not_found`, which the frontend maps to `账号不存在`.
- Wrong passwords return `error_code: invalid_password`.
- The registration route `POST /api/auth/register` is reserved and currently returns `501 Not Implemented`.

## Verification

Backend:

```bash
cd backend
pytest
```

Frontend:

```bash
cd frontend
npm test
```
