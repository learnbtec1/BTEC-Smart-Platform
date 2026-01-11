from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import os
from uuid import uuid4
from ..deps import get_db, get_current_user

router = APIRouter(prefix="/files", tags=["files"])
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/app/uploads")

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), user=Depends(get_current_user)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ext = os.path.splitext(file.filename)[1]
    fname = f"{uuid4().hex}{ext}"
    path = os.path.join(UPLOAD_DIR, fname)
    try:
        content = await file.read()
        with open(path, "wb") as f:
            f.write(content)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to store file")
    return {"filename": fname, "path": path}
