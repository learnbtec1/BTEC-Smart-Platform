Quick steps to run backend locally:

1. Copy .env.example to .env and edit values.
2. Install Python dependencies:
   python -m pip install --upgrade pip
   pip install -r backend/requirements.txt

3A. Run locally (sqlite or existing DB):
   uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 10000
   Open: http://localhost:10000/docs

3B. Run with Docker Compose (from repo root):
   docker compose up -d --build
   # API will be at http://localhost:10000 (per docker-compose)

4. Create superuser:
   python backend/scripts/create_superuser.py
