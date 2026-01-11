import uvicorn
import os
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import create_engine, Session
from app.main import app
from app.api import deps

# محاولة تحميل المفتاح من ملف .env
try:
    from dotenv import load_dotenv
    load_dotenv() 
except ImportError:
    pass

print("🧠 Loading Local Knowledge Base...")
DATABASE_URL = "sqlite:///./knowledge.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def override_get_db():
    with Session(engine) as session:
        yield session

app.dependency_overrides[deps.get_db] = override_get_db

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    print("\n🚀 Server is starting...")
    
    # فحص المفتاح وعرض الحالة
    key = os.getenv("OPENAI_API_KEY")
    if key and key.startswith("sk-"):
        print("✅ OpenAI Key Detected! AI Mode is ON.")
    else:
        print("⚠️ No valid key found. Using Simulation Mode.")
        
    print("👉 API runs at: http://127.0.0.1:8000")
    print("👉 Open 'chat.html' to start chatting!")
    print("-------------------------------------------------------")
    uvicorn.run(app, host="127.0.0.1", port=8000)
