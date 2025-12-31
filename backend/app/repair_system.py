from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, User, BTECAssessment
from passlib.context import CryptContext

# إعدادات الاتصال
DATABASE_URL = "postgresql://myuser:mypassword@db:5432/btec_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

def safe_seed():
    db = SessionLocal()
    try:
        print("🌱 Injecting Admin...")
        admin = db.query(User).filter(User.email == "admin@btec.com").first()
        if not admin:
            # قمنا بإزالة حقل 'name' لتجنب الخطأ
            admin = User(
                email="admin@btec.com",
                hashed_password=pwd_context.hash("admin123"),
                role="teacher"
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print("✅ Admin created successfully.")
        
        print("🌱 Injecting Students...")
        students = [
            {"name": "حمزة الأردني", "unit": "Unit 1", "score": 95},
            {"name": "سارة أحمد", "unit": "Unit 2", "score": 88},
            {"name": "خالد وليد", "unit": "Unit 1", "score": 76},
            {"name": "ليلى حسن", "unit": "Unit 3", "score": 92},
            {"name": "عمر علي", "unit": "Unit 2", "score": 84}
        ]
        for s in students:
            if not db.query(BTECAssessment).filter(BTECAssessment.student_name == s['name']).first():
                db.add(BTECAssessment(
                    student_name=s['name'], 
                    competency_unit=s['unit'], 
                    score=s['score'], 
                    owner_id=admin.id
                ))
        db.commit()
        print("✅ 5 Students seeded successfully.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == '__main__':
    safe_seed()
