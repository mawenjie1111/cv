# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

FastAPI backend + Vue 3 frontend demonstrating a login flow with token-based auth and a deliberately replaceable database boundary. The codebase is small and intentionally dependency-light (standard-library crypto, no ORM, no state-management library).

## Commands

Backend (run from `backend/`):
```bash
python -m pip install -r requirements.txt   # or: pip install -e ".[test]"
uvicorn app.main:app --reload               # serve at http://localhost:8000
pytest                                       # run all tests
pytest tests/test_auth.py::test_successful_login_returns_token_and_user  # single test
```

Frontend (run from `frontend/`):
```bash
npm install
npm run dev        # Vite dev server at http://localhost:5173
npm run build
npm test           # runs scripts/verify.mjs (assertion-based, not a test framework)
```

There is no linter configured. `npm test` is a hand-rolled Node assertion script, not Vitest/Jest — it exercises session logic and greps `router/index.js` for required route guards.

## Architecture

### Backend (`backend/app/`)
The app is assembled by a factory (`main.py::create_app`) that registers all routers under a configurable prefix (default `/api`). Tests and the dev server both call `create_app`, so route registration must stay there.

Request flow for auth:
- `api/auth.py` `POST /auth/login` → looks up user via repository → `core/security.verify_password` → issues token via `core/security.create_access_token`.
- `api/users.py` `GET /users/me` → `dependencies.get_current_user` decodes/validates the bearer token, then re-loads the user from the repository (token `sub` is an identifier only; the repository is the source of truth for active/inactive state).

Two boundaries matter most:
- **Repository boundary** (`repositories/users.py`): `UserRepository` is a `Protocol` with `get_user_by_username` / `get_user_by_id`. The only implementation today is `DevelopmentUserRepository` (in-memory, single seeded user). To add a real database, implement the Protocol and swap the factory in `dependencies.py::_get_repository` (currently `@lru_cache`'d to one process-wide instance) — do not couple route handlers to a concrete adapter.
- **Security boundary** (`core/security.py`): self-contained PBKDF2 password hashing and HMAC-signed compact tokens (`base64(payload).base64(sig)`), using only the standard library. `decode_access_token` verifies the signature before trusting any payload field and enforces expiry. If you change the token format, update both `create_access_token` and `decode_access_token` together.

Config (`config.py`) is a frozen `Settings` dataclass read from environment variables (see `backend/.env.example`). `get_settings()` is used as a FastAPI dependency. `DATABASE_URL` is currently an unused placeholder reserved for the future adapter.

### Frontend (`frontend/src/`)
- `auth/session.js`: pure localStorage serialization helpers (`SESSION_KEY`, load/save/clear). Storage object is injected as an argument, which is what makes it testable from `scripts/verify.mjs`.
- `stores/auth.js`: a module-level `reactive` singleton (not Pinia/Vuex) exposed via `useAuth()`. Holds token/user/initialized/loading/error.
- `services/api.js`: `fetch` wrapper that reads the token from session storage and sets the `Authorization` header; base URL from `VITE_API_BASE_URL`.
- `router/index.js`: route guards enforce `meta.requiresAuth` and redirect authenticated users away from `/login`. `npm test` asserts these guards exist, so keep `requiresAuth: true` and the `name: 'login'` route intact.

## OpenSpec workflow

This repo uses OpenSpec (`openspec/`, `schema: spec-driven`). Feature work is proposed as a change under `openspec/changes/<name>/` (proposal.md, design.md, tasks.md, specs/) before implementation; completed changes are moved to `openspec/changes/archive/`. Established specs live in `openspec/specs/`. Consult the relevant change/spec docs when extending a capability, and follow the existing convention of writing the proposal/design before code for non-trivial features.

## Conventions

- Backend source carries thorough module + function docstrings with `Args:`/`Returns:`/`Raises:` sections (enforced as a documentation capability). Match this style when adding backend code.
- Public JSON shapes are defined by Pydantic schemas in `schemas/auth.py` and intentionally omit internal fields like `password_hash` — never leak the internal `User` dataclass directly.
- Backend tests in `tests/test_auth.py` document public API contracts (status codes, response keys); treat them as the behavior spec rather than implementation tests.
