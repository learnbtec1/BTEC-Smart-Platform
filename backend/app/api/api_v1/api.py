from fastapi import APIRouter

from .endpoints import login, files, assistant

api_router = APIRouter()
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(files.router, prefix="/files", tags=["files"])
api_router.include_router(assistant.router, prefix="/assistant", tags=["assistant"])
