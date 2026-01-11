<#
apply_backend_scaffold.ps1
آمن: ينسخ بناءة backend إلى مجلد backend\app. لا يستبدل الملفات الموجودة؛ إذا وُجد ملف موجود
سيضع النسخة الجديدة باسم filename.ext.new للمراجعة اليدوية.

تشغيل:
Set-Location 'D:\BTEC-backend'
PowerShell -NoProfile -ExecutionPolicy Bypass -File .\apply_backend_scaffold.ps1
#>

function WriteStep($m) { Write-Host "==> $m" -ForegroundColor Cyan }

# تأكد أنك في جذر المشروع
$root = Get-Location
WriteStep "Repo root: $root"

# تأكد وجود git و الفرع الحالي
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "تحذير: git غير موجود في PATH. تابع لكن لن أتمكن من عمل commit تلقائياً." -ForegroundColor Yellow
}
$branch = ""
try { $branch = git rev-parse --abbrev-ref HEAD 2>$null } catch {}
WriteHost "Current branch: $branch"

# 1) نسخ احتياطي لمجلد backend الحالي
$timestamp = (Get-Date).ToString("yyyyMMdd-HHmmss")
$backupDir = Join-Path $root "backups\backend-$timestamp"
if (Test-Path ".\backend") {
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
    WriteStep "Copying backend to backup: $backupDir ..."
    Copy-Item -Path .\backend -Destination $backupDir -Recurse -Force
    WriteStep "Backup complete."
} else {
    WriteStep "No backend folder found to backup; continuing."
}

# 2) Map of files to create (relative to repo root). If target exists -> write .new
$files = @{
"backend\app\__init__.py" = "# package init`n"
"backend\app\database.py" = @'
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL_INTERNAL") or os.getenv("DATABASE_URL") or "sqlite:///./dev.db"
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
'@
"backend\app\models.py" = @'
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)

class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    title = Column(String)
    content = Column(Text, nullable=True)
    course = relationship("Course", backref="lessons")

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    filename = Column(String)
'@
"backend\app\schemas.py" = @'
from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_superuser: bool
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None

class CourseOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    class Config:
        orm_mode = True

class ChatIn(BaseModel):
    q: str
'@
"backend\app\crud.py" = @'
from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate, is_superuser: bool = False):
    hashed = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed, is_superuser=is_superuser)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not pwd_context.verify(password, user.hashed_password):
        return None
    return user

def create_course(db: Session, course: schemas.CourseCreate):
    db_course = models.Course(title=course.title, description=course.description)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def get_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Course).offset(skip).limit(limit).all()
'@
"backend\app\deps.py" = @'
from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import crud, models
from jose import JWTError, jwt
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME_IN_ENV")
ALGORITHM = "HS256"

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user
'@
"backend\app\api\__init__.py" = "# package for api routers`n"
"backend\app\api\auth.py" = @'
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
import os

from .. import crud, schemas
from ..deps import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME_IN_ENV")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded

@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    new = crud.create_user(db, user)
    return new

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.verify_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect credentials")
    access_token = create_access_token({"sub": user.email}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}
'@
"backend\app\api\courses.py" = @'
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..deps import get_db

router = APIRouter(prefix="/courses", tags=["courses"])

@router.post("/", response_model=schemas.CourseOut)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    return crud.create_course(db, course)

@router.get("/", response_model=list[schemas.CourseOut])
def list_courses(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return crud.get_courses(db, skip=skip, limit=limit)
'@
"backend\app\api\files.py" = @'
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
'@
"backend\app\api\chat.py" = @'
from fastapi import APIRouter
from ..schemas import ChatIn

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/")
async def chat_endpoint(payload: ChatIn):
    return {"answer": f"Received: {payload.q}"}
'@
"backend\app\main.py" = @'
from fastapi import FastAPI
from .database import engine, Base
from .api import auth, courses, files, chat

app = FastAPI(title="BTEC-like Platform")

# Create DB tables on startup for development (use alembic for production)
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(files.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {"status": "ok"}
'@
"backend\scripts\create_superuser.py" = @'
#!/usr/bin/env python3
import getpass
import os
import sys

try:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from app import database, crud, schemas
    db = database.SessionLocal()
except Exception as e:
    print("Run this script from repository root with installed dependencies. Error:", e)
    raise SystemExit(1)

def main():
    email = input("Email for admin: ").strip()
    pwd = getpass.getpass("Password: ")
    existing = crud.get_user_by_email(db, email)
    if existing:
        print("User exists, updating to superuser.")
        existing.is_superuser = True
        db.add(existing)
        db.commit()
        print("Updated.")
    else:
        user = schemas.UserCreate(email=email, password=pwd)
        crud.create_user(db, user, is_superuser=True)
        print("Created superuser.")

if __name__ == "__main__":
    main()
'@
"backend\requirements.txt" = @'
fastapi
uvicorn[standard]
sqlalchemy>=1.4
psycopg2-binary
alembic
passlib[bcrypt]
python-jose[cryptography]
python-multipart
pydantic
python-dotenv
pytest
httpx
'@
"backend\Dockerfile" = @'
FROM python:3.11-slim

WORKDIR /app
COPY ./backend /app

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1
EXPOSE 10000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
'@
"README-backend.md" = @'
Quick steps to run backend locally:

1. Copy .env.example to .env and edit values.
2. Install Python dependencies:
   python -m pip install --upgrade pip
   pip install -r backend/requirements.txt

3A. Run locally (sqlite or existing DB):
   uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 10000
   Open: http://localhost:10000/docs

3B. Run with Docker Compose (from repo root):
   docker compose up -d --build
   # API will be at http://localhost:10000 (per docker-compose)

4. Create superuser:
   python backend/scripts/create_superuser.py
'@
}

# 3) Create files safely
$created = @()
$createdNew = @()
foreach ($relPath in $files.Keys) {
    $target = Join-Path $root $relPath
    $dir = Split-Path $target
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }

    $content = $files[$relPath]
    if (-not (Test-Path $target)) {
        $content | Out-File -FilePath $target -Encoding utf8 -Force
        $created += $relPath
    } else {
        $newPath = $target + ".new"
        $content | Out-File -FilePath $newPath -Encoding utf8 -Force
        $createdNew += $relPath + ".new"
    }
}

# 4) Summary
WriteStep "Done. Summary:"
if ($created.Count -gt 0) {
    Write-Host "New files created:" -ForegroundColor Green
    $created | ForEach-Object { Write-Host " - $_" }
}
if ($createdNew.Count -gt 0) {
    Write-Host "Existing files preserved. New candidate files written as .new (review and merge manually):" -ForegroundColor Yellow
    $createdNew | ForEach-Object { Write-Host " - $_" }
}

# 5) Offer to create commit
if (Get-Command git -ErrorAction SilentlyContinue) {
    $ans = Read-Host "Create local git commit with these new files? (y/n)"
    if ($ans -match '^[Yy]') {
        git add .
        git commit -m "chore(scaffold): add backend scaffold (new files added or .new candidates)" -q
        WriteStep "Committed changes locally."
        Write-Host "Push with: git push -u origin $branch"
    } else {
        WriteStep "Skipped git commit. Review .new files and commit when ready."
    }
} else {
    WriteStep "git not available; please review files and commit manually."
}
WriteStep "Finished. Review .new files and merge carefully into existing code."