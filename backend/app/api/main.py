from fastapi import APIRouter
# استيراد الملفات الموجودة لديك مسبقاً + الملف الجديد
from app.api import auth, chat, courses, files, assessments

api_router = APIRouter()

# تسجيل الموجهات (Routers)
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
api_router.include_router(courses.router, prefix="/courses", tags=["Courses"])
api_router.include_router(files.router, prefix="/files", tags=["Files"])
api_router.include_router(assessments.router, prefix="/assessments", tags=["Assessments"])
