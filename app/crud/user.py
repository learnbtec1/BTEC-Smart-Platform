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
