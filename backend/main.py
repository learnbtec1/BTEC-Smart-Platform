from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# إعداد CORS للسماح للواجهة الأمامية بالاتصال
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        # أضف رابط Vercel عند النشر
        # "https://your-frontend.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# نموذج بيانات تسجيل الدخول
class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/token")
async def login(data: LoginRequest):
    # تحقق بسيط — سيتم استبداله بقاعدة بيانات لاحقًا
    if data.username != "admin" or data.password != "admin":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": "test_token_123",
        "token_type": "bearer",
        "user": {
            "id": 1,
            "email": data.username,
            "name": "Test User",
            "role": "teacher"
        }
    }