from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session
from app.main import app
from app.api import deps

# 1. إعداد الاتصال بالعقل المحلي الذي أنشأناه
engine = create_engine("sqlite:///./knowledge.db", connect_args={"check_same_thread": False})

# 2. دالة لاستبدال قاعدة البيانات الرئيسية بقاعدة المعرفة المحلية
def override_get_db():
    with Session(engine) as session:
        yield session

# 3. تطبيق الاستبدال (Dependency Override)
app.dependency_overrides[deps.get_db] = override_get_db

client = TestClient(app)

def test_api_brain():
    print("\n🤖 Testing API Endpoint: /api/v1/assistant/ask")
    print("⏳ Sending request...")
    
    # إرسال السؤال
    payload = {"question": "Business"} 
    
    try:
        response = client.post("/api/v1/assistant/ask", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ API RESPONSE SUCCESS!")
            print("-" * 50)
            print(f"📝 Answer Preview:\n{data['answer'][:200]}...")
            print("-" * 50)
            print(f"📚 Sources Used ({len(data['sources'])}):")
            for source in data['sources']:
                print(f"   - {source}")
        else:
            print(f"\n❌ API Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"\n❌ Connection Error: {e}")

if __name__ == "__main__":
    test_api_brain()
