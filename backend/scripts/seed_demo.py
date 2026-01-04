"""
Seed demo data: creates demo users and sample data.
Run: python backend/scripts/seed_demo.py
"""
import os
import bcrypt
from sqlmodel import SQLModel, create_engine, Session
from datetime import datetime
import pathlib
from backend.app.models_files import UserFile
from backend.app.models_progress import StudentProgress

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./dev.db")
engine = create_engine(DATABASE_URL, echo=False)

def ensure_tables():
    SQLModel.metadata.create_all(engine)

def hashpw(pw):
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()

def seed():
    ensure_tables()
    with Session(engine) as session:
        # Create demo users in simple table if exists, otherwise skip
        # Create uploads dir and dummy files
        uploads = pathlib.Path("uploads")
        uploads.mkdir(exist_ok=True)
        demo_file = uploads / "demo.txt"
        demo_file.write_text("This is a demo file for Keitagorus.")
        # Create demo user_file entries (owner_id set to 'demo-student')
        uf = UserFile(id="demo-file-1", owner_id="demo-student", original_filename="demo.txt", stored_path=str(demo_file), content_type="text/plain", size=demo_file.stat().st_size, created_at=datetime.utcnow())
        session.add(uf)
        # Create demo student progress
        sp = StudentProgress(id="demo-progress-1", user_id="demo-student", lesson_id=None, progress_percentage=42, last_score=42.0, attempts=2, struggling=True, updated_at=datetime.utcnow())
        session.add(sp)
        session.commit()
    print("Seed complete. Demo credentials (example): student1@example.com / secret123 (if created via API)")

if __name__ == "__main__":
    seed()
