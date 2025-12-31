# انتقل إلى جذر المشروع أولاً
cd D:\BTEC-backend   # عدّل المسار إن لزم

# أنشئ فرع جديد باسم timestamped
$branch = "feature/fix-bcrypt-72-$(Get-Date -Format yyyyMMddHHmmss)"
git fetch origin main 2>$null | Out-Null
git checkout -b $branch

# 1) Backup and overwrite app/crud/user.py
if (Test-Path "app\crud\user.py") {
  Copy-Item "app\crud\user.py" "app\crud\user.py.bak.$(Get-Date -Format yyyyMMddHHmmss)" -Force
  Write-Host "Backup created: app\crud\user.py.bak.*"
}

$crud = @'
from sqlalchemy.orm import Session
from app.models.user import User
from passlib.context import CryptContext
from typing import Optional
from fastapi import HTTPException, status

# Use bcrypt_sha256 to avoid the 72-byte limit of raw bcrypt input.
# bcrypt_sha256 pre-hashes with SHA256 before bcrypt, allowing arbitrarily long passwords.
pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, password: str) -> User:
    # Basic validation: ensure password present and not absurdly huge
    if not password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is required")
    if len(password) > 4096:
        # defensive ceiling — adjust as needed
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password too long")

    hashed_password = pwd_context.hash(password)
    user = User(email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
'@

# اكتب الملف (سينشئ المجلد إذا لزم)
if (-not (Test-Path "app\crud")) { New-Item -ItemType Directory -Path "app\crud" | Out-Null }
Set-Content -Path "app\crud\user.py" -Value $crud -Encoding UTF8
Write-Host "Updated: app/crud/user.py"

# 2) (اختياري) إذا كان موجودا، حدّث app/schemas/user.py لإضافة قيد طول
if (Test-Path "app\schemas\user.py") {
  Copy-Item "app\schemas\user.py" "app\schemas\user.py.bak.$(Get-Date -Format yyyyMMddHHmmss)" -Force
  $schema = @'
from pydantic import BaseModel, EmailStr, constr
from typing import Optional

# enforce reasonable password length at validation level (e.g. 8..4096)
class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=4096)

class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    sub: Optional[str] = None
'@
  if (-not (Test-Path "app\schemas")) { New-Item -ItemType Directory -Path "app\schemas" | Out-Null }
  Set-Content -Path "app\schemas\user.py" -Value $schema -Encoding UTF8
  Write-Host "Updated: app/schemas/user.py"
} else {
  Write-Host "app/schemas/user.py not found — skipped updating schema."
}

# 3) Git add & commit
git add app/crud/user.py
if (Test-Path "app/schemas/user.py") { git add app/schemas/user.py }
git commit -m "fix: use bcrypt_sha256 to avoid bcrypt 72-byte limit; add password validation" || Write-Host "No changes to commit"

Write-Host "`nBranch prepared locally: $branch"
Write-Host "Push the branch and open a PR when ready:"
Write-Host "  git push --set-upstream origin $branch"
Write-Host "  gh pr create --title 'fix: bcrypt 72-byte limit -> bcrypt_sha256' --body 'Use bcrypt_sha256 instead of raw bcrypt; add password validation' --base main"