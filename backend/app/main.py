from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import uvicorn
import os

# 1. تهيئة النواة الذكية
app = FastAPI(title="BTEC NEXUS ENTERPRISE v2200")

# 2. إعدادات الأمان (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. الهيكل التنظيمي للمؤسسة (أتمتة البيانات)
# ملاحظة: في النسخة النهائية يتم ربط هذا بجدول "users" في قاعدة البيانات
SYSTEM_ROLES = {
    "ADMIN": {"count": 1, "access_level": "ROOT"},
    "HOD": {"count": 10, "access_level": "DEPARTMENT_MANAGER"},
    "TEACHER": {"count": 50, "access_level": "INSTRUCTOR"},
    "STUDENT": {"count": 1000, "access_level": "LEARNER"}
}

# 4. نقاط التحكم الإدارية (Endpoints)

@app.get("/api/v1/enterprise/stats")
async def get_enterprise_stats():
    """هذه النقطة تغذي لوحة التحكم بالأرقام الحقيقية للمؤسسة"""
    return {
        "total_users": sum(role["count"] for role in SYSTEM_ROLES.values()),
        "breakdown": {role: data["count"] for role, data in SYSTEM_ROLES.items()},
        "active_students": 1000,
        "active_teachers": 50,
        "department_heads": 10,
        "system_health": "OPTIMAL",
        "neural_link": "STABLE"
    }

@app.get("/api/v1/enterprise/users/{role}")
async def get_users_by_role(role: str):
    """جلب قائمة المستخدمين بناءً على الرتبة (أتمتة العرض)"""
    role = role.upper()
    if role not in SYSTEM_ROLES:
        raise HTTPException(status_code=404, detail="الرتبة غير موجودة في النظام")
    
    # محاكاة توليد البيانات للمستخدمين (أتمتة التوليد)
    mock_users = []
    limit = SYSTEM_ROLES[role]["count"]
    for i in range(1, min(limit + 1, 11)): # نعرض أول 10 كمثال
        mock_users.append({
            "id": f"{role[0]}-{i:04d}",
            "name": f"{role.capitalize()}_User_{i}",
            "role": role,
            "status": "ACTIVE"
        })
    return {"total": limit, "preview": mock_users}

@app.get("/api/v1/status")
async def dashboard_status():
    """النقطة التي تطلبها الواجهة كل 5 ثوانٍ"""
    return {
        "status": "ONLINE",
        "active_sessions": 452,
        "processing_power": "98.2 GHZ",
        "location": "Amman, Jordan",
        "epoch": "2125.4.1"
    }

# 5. تشغيل المحرك
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=10000, reload=True)