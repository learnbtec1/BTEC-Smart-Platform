# Copilot Instructions — BTEC Smart Platform & Backend
Short, actionable guide to get an AI coding agent productive in this repo.

Big picture
- Major components: `backend/` (FastAPI microservices), `Flutter/` (mobile/web UI), `frontend/` (Next.js), `gateway/`, plus orchestration via top-level `docker-compose*.yml`.
- Pattern: thin HTTP routers live in `backend/app/api/` and delegate business logic to `backend/app/services/`. DB models use `SQLModel` in `backend/app/models.py`. Migrations live under `backend/alembic/`.

Quick dev & debug commands
- Start full stack (recommended for integration): `docker compose up --build` (see `docker-compose.yml` and `docker-compose-microservices.yml`).
- Backend local dev (repo root):
  - `cd backend`
  - `python -m venv .venv` then activate (`.venv\Scripts\Activate.ps1` on Windows or `source .venv/bin/activate` on *nix)
  - `uvicorn app.main:app --reload`
- Enter running backend container: `docker compose exec backend bash` (inspect env, run migrations/tests).
- Run tests (match CI): `bash backend/scripts/test.sh` or `cd backend && pytest -q`.

Conventions & project-specific patterns
- Routing: add thin routers to `backend/app/api/` and register them in `backend/app/api/main.py`. App composition occurs in `backend/app/main.py`.
- Services: implement feature logic in `backend/app/services/<feature>.py`. Unit tests should import these service functions directly (see `backend/tests/`).
- Models & migrations: keep models in `backend/app/models.py` (SQLModel). When changing persistent models, add an Alembic revision and commit it under `backend/alembic/versions/`.
- Healthchecks & helpers: use `healthcheck.py`, `auto_healthcheck.py`, and scripts in `backend/scripts/` for CI-friendly flows.

Integration & environment notes
- CORS is configured in `backend/app/main.py`; add origins via the `EXTRA_CORS_ORIGINS` env var.
- Services communicate over HTTP. Use `docker compose` for multi-service integration tests to replicate runtime topology.
- Read-only/static simulator assets live in `BTEC-Virtual-World/` (submodule). Update with `git submodule update --init --recursive` when needed.

Where AI agents should work
- Prefer changing `backend/app/services/` and `backend/tests/`. Avoid large router/recomposition edits unless necessary.
- For DB schema changes: update `backend/app/models.py`, generate an Alembic revision, and run `alembic upgrade head` locally against a dev DB.

Key files to inspect first
- `backend/app/main.py` — app bootstrap, middleware, CORS
- `backend/app/api/main.py` — router registration
- `backend/app/services/` — core business logic and scoring
- `backend/app/models.py` — SQLModel DB definitions
- `backend/alembic/` — migrations and versions
- `backend/scripts/test.sh` — CI/local test runner
- `docker-compose-microservices.yml` / `docker-compose.yml` — service wiring

Practical checklist — add a backend endpoint
1. Add/update `SQLModel` in `backend/app/models.py` and create an Alembic revision if persistent.
2. Add Pydantic request/response models close to the router (or `schemas.py`).
3. Implement logic in `backend/app/services/<feature>.py` and add unit tests under `backend/tests/`.
4. Add a thin router to `backend/app/api/<feature>.py` and register it via `backend/app/api/main.py`.
5. Run `backend/scripts/test.sh` and `alembic upgrade head` to validate locally before pushing.

Notes for AI agents
- Keep changes minimal and consistent with existing patterns (thin routers, service functions, SQLModel). Add tests for behavior changes.
- Use `backend/scripts/test.sh` to reproduce CI behavior locally.
- If scaffolding is requested, implement service + tests first; add the thin router last.

Offer
- If you’d like, I can scaffold an example endpoint + service + test for a named feature (e.g., `assessments`). Tell me the feature name and I will implement it.
# Copilot Instructions — BTEC Smart Platform & Backend
Short, actionable guide to get an AI coding agent productive in this repo.

Big picture
- Major components: `backend/` (FastAPI microservices), `Flutter/` (mobile/web UI), `frontend/` (Next.js app), `gateway/`, and orchestration via top-level `docker-compose*.yml`.
- Design pattern: thin HTTP routers in `backend/app/api/` delegate to `backend/app/services/*` where business rules, validation and AI scoring live. DB models use `SQLModel` in `backend/app/models.py` and migrations live under `backend/alembic/`.

Quick dev & debug commands (practical)
- Start full stack: `docker compose up --build` (see `docker-compose.yml` and `docker-compose-microservices.yml`).
- Backend local dev (repo root):
  - `cd backend`
  - `python -m venv .venv` then activate (`.venv\\Scripts\\Activate.ps1` on Windows or `source .venv/bin/activate` on *nix)
  - `uvicorn app.main:app --reload`
- Enter running backend container: `docker compose exec backend bash` (inspect runtime env, run migrations, run tests).
- Run tests (match CI): `bash backend/scripts/test.sh` or `cd backend && pytest -q`.
- Run migrations (from `backend/`): `alembic revision --autogenerate -m "msg"` then `alembic upgrade head`.

Conventions & project-specific patterns
- Routing: add thin routers under `backend/app/api/` and register them in `backend/app/api/main.py`; composition happens in `backend/app/main.py`.
- Services: implement feature logic inside `backend/app/services/<feature>.py`. Tests should import and call service functions directly (see `backend/tests/`).
- Models: DB models live in `backend/app/models.py` (SQLModel). Use local `schemas.py` near a router when request/response models are needed.
- Migrations: Alembic config lives in `backend/alembic/`. Commit generated revisions under `alembic/versions/` when changing persistent models.
- Healthchecks & helpers: see `healthcheck.py`, `auto_healthcheck.py`, and `backend/scripts/` for CI-friendly utilities.

Integration & environment notes
- CORS: configured in `backend/app/main.py`; supply extra origins via `EXTRA_CORS_ORIGINS` env var.
- Services communicate over HTTP; use `docker compose` to reproduce multi-service behavior for integration testing.
- Read-only/static assets (simulator/world) live in `BTEC-Virtual-World/` as a submodule; update with `git submodule update --init --recursive`.

Key files to inspect first
- `backend/app/main.py` — app bootstrap, middleware, CORS
- `backend/app/api/main.py` — router registration
- `backend/app/services/` — core business logic and scoring
- `backend/app/models.py` — SQLModel DB definitions
- `backend/alembic/` — migrations and versions
- `backend/scripts/test.sh` — CI/local test runner
- `docker-compose-microservices.yml` / `docker-compose.yml` — service wiring

Common tasks checklist (example: add a backend endpoint)
1. Add/update a `SQLModel` in `backend/app/models.py` and create an Alembic revision if persistent.
2. Add Pydantic request/response models in a nearby `schemas.py` or inside the router file.
3. Implement business logic in `backend/app/services/<feature>.py` and add unit tests under `backend/tests/`.
4. Create a thin router in `backend/app/api/<feature>.py` and register it via `backend/app/api/main.py`.
5. Run `backend/scripts/test.sh` and `alembic upgrade head` to validate locally before pushing.

Notes for AI agents
- Prefer touching `services/` and `tests/`; avoid changing routing or composition unless required.
- Keep changes minimal and consistent with existing patterns (thin routers, service functions, SQLModel). Add tests for behavior changes.
- Use `backend/scripts/test.sh` to replicate CI; run `alembic upgrade head` against a local dev DB when changing models.

Next step offer
If you'd like, I can scaffold an example endpoint + service + test for a named feature (e.g., `assessments`). Tell me the feature name and I will implement it.
# Copilot Instructions — BTEC Smart Platform & Backend
Concise, actionable guidance to get an AI coding agent productive in this repo.

Big picture
- Major components: `backend/` (FastAPI microservices), `Flutter/` (mobile/web UI), `BTEC-Virtual-World/` (read-only assets/submodule), plus gateway and orchestration via top-level docker-compose files.
- Pattern: HTTP routers in `backend/app/api/` are intentionally thin; core business logic, validation, and AI scoring live in `backend/app/services/*`. DB models use `SQLModel` in `backend/app/models.py` and migrations live under `backend/alembic/`.

Quick dev commands (practical)
- Start full stack: `docker compose up --build` (see `docker-compose.yml` / `docker-compose-microservices.yml`).
- Enter backend container for debugging: `docker compose exec backend bash`.
- Backend local dev (from repo root):
  - `cd backend`
  - `python -m venv .venv` then activate (`.venv\Scripts\Activate.ps1` on Windows or `source .venv/bin/activate` on *nix)
  - `uvicorn app.main:app --reload`
- Run tests: `bash backend/scripts/test.sh` or `cd backend && pytest -q` (use the script to match CI behavior).
- Migrations (from `backend/`): `alembic revision --autogenerate -m "msg"` then `alembic upgrade head`.
- Update submodule assets: `git submodule update --init --recursive`.

Backend conventions (concrete)
- Routing: place thin routers under `backend/app/api/` and register them in `backend/app/api/main.py`. The app is composed in `backend/app/main.py`.
- Services: implement business rules in `backend/app/services/<feature>.py`. Tests should import service functions directly (see `backend/tests/`).
- Models & schemas: primary DB models live in `backend/app/models.py` (SQLModel). Prefer co-locating Pydantic request/response models with routes or using `schemas.py` alongside the route.
- Migrations: Alembic config is in `backend/alembic/`; commit migrations for any persistent model changes.

Repo-specific patterns & examples
- Healthchecks and dev helpers: see `healthcheck.py`, `auto_healthcheck.py`, and scripts under `backend/scripts/` for CI-compatible flows.
- Docker: `backend/Dockerfile` + top-level compose files define the dev/topology; prefer `docker compose` for integration tests that need multiple services.
- CI expectations: `backend/scripts/test.sh` reproduces test setup used in CI — run it locally to match pipeline behavior.

Integration & env notes
- CORS: configured in `backend/app/main.py`; additional origins can be passed via `EXTRA_CORS_ORIGINS` env var.
- Use `docker compose` orchestration to reproduce service-to-service HTTP interactions during integration debugging.

Key files to inspect (quick)
- `backend/app/main.py` — app bootstrap, CORS, middleware
- `backend/app/api/main.py` — router composition
- `backend/app/services/` — business logic and AI scoring
- `backend/app/models.py` — SQLModel definitions
- `backend/alembic/` — migrations
- `backend/scripts/test.sh` — CI/test runner
- `docker-compose-microservices.yml` / `docker-compose.yml` — orchestration

Practical checklist — add a backend endpoint
1. Update `backend/app/models.py` (SQLModel) and add an Alembic revision if persistent changes are needed.
2. Add Pydantic input/output models near the route or in a `schemas.py`.
3. Implement logic in `backend/app/services/<feature>.py` and add unit tests under `backend/tests/`.
4. Create a thin router in `backend/app/api/<feature>.py` and register it via `backend/app/api/main.py`.
5. Run `backend/scripts/test.sh` and `alembic upgrade head` to verify locally before pushing.

If you want, I can scaffold an example endpoint + service + test (name the feature) or expand any section above.
```instructions
# 🧠 Copilot Instructions — BTEC Smart Platform & Backend
Short, actionable guidance to get an AI coding agent productive in this repo.

---

## Big picture
- Components: `Flutter/` (mobile/web UI), `backend/` (FastAPI microservices), `BTEC-Virtual-World/` (read-only submodule for assets/simulations).
- Primary pattern: thin HTTP routes delegate to `backend/app/services/*` where business rules, validation, and AI scoring live. DB access uses `SQLModel` models in `backend/app/models.py`.

## Quick dev commands (examples)
- Start full stack locally: `docker compose up --build`
- Enter backend container: `docker compose exec backend bash`
- Run backend locally (repo root):
  - `cd backend`
  - `python -m venv .venv && source .venv/bin/activate` (or use Windows PowerShell venv activation)
  - `uvicorn app.main:app --reload`
- Run tests: `bash backend/scripts/test.sh` or `cd backend && pytest -q`
- Create migrations (from `backend/`): `alembic revision --autogenerate -m "msg"` then `alembic upgrade head`
- Update submodule: `git submodule update --init --recursive`

## Backend conventions (concrete)
- Routes: place thin routers under `backend/app/api/` (see `backend/app/api/main.py`) and compose them on `app` in `backend/app/main.py`.
- Services: put business logic in `backend/app/services/<feature>.py`; tests should target services directly under `backend/tests/`.
- Models & schemas: use `SQLModel` in `backend/app/models.py`; use Pydantic request/response models (co-locate with the route or use a `schemas.py` per feature).
- Migrations: Alembic lives under `backend/alembic/` and revisions under `backend/alembic/versions/`.

## Frontend (Flutter) conventions
- Feature layout: `Flutter/lib/features/<feature>/` with `view.dart`, `controller.dart`, and `widgets/`.
- Keep business logic in controllers/services (not StatefulWidgets).
- Fonts/assets: declared in `Flutter/pubspec.yaml` (primary font: Cairo).

## Integration notes
- CORS: configured in `backend/app/main.py` and can be extended via the `EXTRA_CORS_ORIGINS` env var.
- Services communicate over HTTP; prefer `docker compose` for integration testing to mirror network topology.

## Key files to inspect
- `backend/app/main.py` — app bootstrap and CORS setup
- `backend/app/api/main.py` — router composition
- `backend/app/services/` — business logic and AI scoring
- `backend/app/models.py` — `SQLModel` definitions
- `backend/alembic/` — migration config and versions
- `backend/scripts/test.sh` — test runner helper

## Practical checklist — add a backend endpoint
1. Add/update `SQLModel` in `backend/app/models.py` (add Alembic revision if persistent).
2. Add Pydantic request/response models (near route or in `schemas.py`).
3. Implement logic in `backend/app/services/<feature>.py` and add unit tests in `backend/tests/`.
4. Add thin router in `backend/app/api/<feature>.py` and include it via `backend/app/api/main.py`.
5. Run migrations and CI tests.

---
If you'd like, I can:
- scaffold an example endpoint + service + test (pick a feature name), or
- replace the original `.github/copilot-instructions.md` with this cleaned draft.
```