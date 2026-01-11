from fastapi import APIRouter
from app.api import assessments, chat

api_router = APIRouter()

# تسجيل المسارات
api_router.include_router(assessments.router, prefix="/assessments", tags=["assessments"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
