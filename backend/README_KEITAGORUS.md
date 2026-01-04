# Keitagorus Foundation — README

This file explains how to run migrations, seed demo data, and start the server for the Keitagorus AI foundation.

## Quickstart (local)
1. Create virtualenv and install:
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   pip install sqlmodel alembic bcrypt pyjwt

2. Prepare .env (or set env vars):
   export DATABASE_URL="sqlite:///./dev.db"
   export SECRET_KEY="replace-with-secure-key"

3. Run migrations (alembic must be configured):
   cd backend
   alembic upgrade head

4. Seed demo:
   python backend/scripts/seed_demo.py

5. Run server:
   uvicorn backend.app.main:app --reload --port 10001

## Demo credentials
- student1@example.com / secret123 (if registered via API)
- teacher1@example.com / secret123
- admin@example.com / secret123

> Note: register endpoint is dev-only. Change secrets before production.
