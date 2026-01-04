from fastapi import APIRouter

router = APIRouter()

@router.get("", tags=["health"])
def health_root():
    return {"status": "ok", "message": "API v1 health check passed"}