from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import os
import bcrypt
import jwt
from sqlmodel import Session, select
# lightweight local imports — adapt if your project has other modules
from sqlmodel import SQLModel, create_engine

router = APIRouter()

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

# Minimal in-file user model for dev convenience — if repo has User model, replace accordingly
class User(SQLModel, table=True):
    __tablename__ = "user"
    id: str = None
    email: str = None
    full_name: Optional[str] = None
    hashed_password: str = None
    created_at: datetime = datetime.utcnow()

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserRegister(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None

# Very small get_db stub — in repo adapt to existing dependency
def get_engine():
    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./dev.db")
    return create_engine(DATABASE_URL, echo=False)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/access-token", response_model=Token)
def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # minimal auth: look up user in sqlite (or use project-specific user)
    from sqlmodel import select
    engine = get_engine()
    with Session(engine) as session:
        stmt = select(User).where(User.email == form_data.username)
        user = session.exec(stmt).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
        if not bcrypt.checkpw(form_data.password.encode(), user.hashed_password.encode()):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
        token = create_access_token({"sub": user.email, "id": user.id})
        return Token(access_token=token)

@router.post("/register", response_model=dict, status_code=201)
def register(user_in: UserRegister):
    engine = get_engine()
    with Session(engine) as session:
        # create user table if not exists (simple)
        try:
            user = User()
            user.id = str(datetime.utcnow().timestamp()).replace('.', '')
        except Exception:
            pass
        hashed = bcrypt.hashpw(user_in.password.encode(), bcrypt.gensalt()).decode()
        u = User(id=str(datetime.utcnow().timestamp()).replace('.', ''), email=user_in.email, full_name=user_in.full_name, hashed_password=hashed)
        session.add(u)
        session.commit()
        return {"id": u.id, "email": u.email, "full_name": u.full_name}
