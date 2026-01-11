from sqlmodel import create_engine, Session, select
from app.models import KnowledgeItem

# الاتصال بقاعدة البيانات
print("🧠 Connecting to Knowledge Base...")
engine = create_engine("sqlite:///./knowledge.db")

with Session(engine) as session:
    # جلب كل أسماء الملفات المخزنة
    statement = select(KnowledgeItem.source_file)
    results = session.exec(statement).all()
    
    # فلترة الأسماء لتكون فريدة (بدون تكرار)
    unique_files = set(results)
    
    print(f"\n📂 Files found in Database ({len(unique_files)} files):")
    print("-" * 50)
    if unique_files:
        for f in unique_files:
            print(f"📄 {f}")
    else:
        print("❌ Database is EMPTY!")
    print("-" * 50)
