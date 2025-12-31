from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, User, BTECAssessment
from passlib.context import CryptContext
import os

DATABASE_URL = "postgresql://myuser:mypassword@db:5432/btec_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

def run():
    db = SessionLocal()
    try:
        # ????? Admin
        admin = db.query(User).filter(User.email == "admin@btec.com").first()
        if not admin:
            admin = User(email="admin@btec.com", hashed_password=pwd_context.hash("admin123"), role="teacher")
            db.add(admin); db.commit(); db.refresh(admin)
        
        # ????? ??????
        students = [
            {"name": "???? ???????", "unit": "Unit 1", "score": 95},
            {"name": "???? ????", "unit": "Unit 2", "score": 88},
            {"name": "???? ????", "unit": "Unit 1", "score": 76},
            {"name": "???? ???", "unit": "Unit 3", "score": 92},
            {"name": "??? ???", "unit": "Unit 2", "score": 84}
        ]
        for s in students:
            if not db.query(BTECAssessment).filter(BTECAssessment.student_name == s['name']).first():
                db.add(BTECAssessment(student_name=s['name'], competency_unit=s['unit'], score=s['score'], owner_id=admin.id))
        db.commit()
        print("? System Ready: Admin & 5 Students Seeded.")
    finally: db.close()

if __name__ == '__main__': run()
