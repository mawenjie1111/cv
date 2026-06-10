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

Then update the repository factory in `backend/app/dependencies.py` to return the concrete adapter based on `DATABASE_URL` or another environment setting.

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
