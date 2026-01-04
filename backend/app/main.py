from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import random
import uvicorn
# Use package-style import so the app runs the same inside and outside Docker
from app.api.api_v1.api import api_router
from app.core.config import settings

app = FastAPI(title="BTEC MetaVerse Engine 2500")

# إعدادات CORS - استخدم إعدادات `BACKEND_CORS_ORIGINS` من الإعدادات
allow_origins = settings.all_cors_origins or ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ربط المسارات الأساسية ونظام المدرب الذكي والتعليم التكيفي
app.include_router(api_router, prefix="/api/v1")

# بيانات محاكاة للدخول السريع (حمزة القائد)
USERS = {"hamza": "2200", "admin": "admin123"}

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "BTEC Backend is Online and Ready",
        "engine": "FastAPI 0.1xx",
        "tutor_status": "Active"
    }

@app.get("/api/v1/auth/login")
async def login(u: str, p: str):
    if u in USERS and USERS[u] == p:
        return {
            "status": "success",
            "user": {"username": u, "role": "ADMIN"},
            "token": "BTEC-Q-2500-TOKEN"
        }
    raise HTTPException(status_code=401, detail="Invalid Credentials")

if __name__ == "__main__":
    # Run on port 10000 to match docker-compose mapping
    uvicorn.run(app, host="0.0.0.0", port=10000)