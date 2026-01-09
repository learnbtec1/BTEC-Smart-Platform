from pydantic import EmailStr
from typing import Optional, List
import uuid
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

# ----------------------------
# User / Item models (SQLModel)
# ----------------------------

# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    __table_args__ = {"extend_existing": True}
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", sa_relationship_kwargs={"cascade": "all, delete-orphan"})


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# ----------------------------
# Item models
# ----------------------------

# Shared properties for items
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    # AR model url for .glb/.usdz etc. Optional.
    ar_model_url: str | None = Field(default=None, max_length=2048)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    __table_args__ = {"extend_existing": True}
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# ----------------------------
# Auth / Token models
# ----------------------------

# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)


# ----------------------------
# Student progress models
# ----------------------------

class StudentProgressBase(SQLModel):
    module_name: str = Field(max_length=255)
    progress: int = Field(default=0, ge=0, le=100)
    struggling: bool = Field(default=False)
    last_active: datetime | None = None


class StudentProgressCreate(StudentProgressBase):
    pass


class StudentProgressUpdate(SQLModel):
    progress: int | None = Field(default=None, ge=0, le=100)
    struggling: bool | None = None
    last_active: datetime | None = None


class StudentProgress(StudentProgressBase, table=True):
    __table_args__ = {"extend_existing": True}
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, index=True)


class StudentProgressPublic(StudentProgressBase):
    id: uuid.UUID
    user_id: uuid.UUID


# ----------------------------
# Conversation model for chat persistence
# ----------------------------

from typing import Optional as _Optional

class Conversation(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: _Optional[uuid.UUID] = Field(default=None, foreign_key="user.id", index=True)
    session_id: _Optional[str] = Field(default=None, index=True, max_length=128)
    role: str = Field(..., max_length=16)  # "user" | "assistant" | "system"
    content: str = Field(...)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))

    def __repr__(self) -> str:
        return f"<Conversation id={self.id} session_id={self.session_id} role={self.role}>"


# ----------------------------
# Lightweight Chat input model (for API)
# ----------------------------
from pydantic import BaseModel as _BaseModel

class ChatIn(_BaseModel):
    q: str
# --- Backwards-compatibility aliases ---
UserOut = UserPublic
UsersOut = UsersPublic
TokenData = TokenPayload

# --- Compatibility aliases (temporary) ---
CourseCreate = ItemCreate
CourseUpdate = ItemUpdate
CourseOut = ItemPublic
CoursePublic = ItemPublic
CoursesOut = ItemsPublic
LessonOut = ItemPublic
LessonCreate = ItemCreate


# ----------------------------
# Assignment & Submission schemas
# ----------------------------


class AssignmentCreate(SQLModel):
    title: str
    description: Optional[str] = None
    module_name: Optional[str] = None
    due_date: Optional[datetime] = None


class AssignmentUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    module_name: Optional[str] = None
    due_date: Optional[datetime] = None


class AssignmentRead(SQLModel):
    id: int
    title: str
    description: Optional[str] = None
    module_name: Optional[str] = None
    due_date: Optional[datetime] = None
    created_at: Optional[datetime] = None


class SubmissionCreate(SQLModel):
    content_url: Optional[str] = None
    content_text: Optional[str] = None


class SubmissionUpdate(SQLModel):
    id: Optional[int] = None
    grade: Optional[int] = None
    feedback: Optional[str] = None


class SubmissionRead(SQLModel):
    id: int
    assignment_id: int
    student_id: Optional[uuid.UUID]
    content_url: Optional[str]
    content_text: Optional[str]
    grade: Optional[int]
    feedback: Optional[str]
    submitted_at: Optional[datetime]


# ----------------------------
# BTEC assessment lightweight models (placeholder)
# ----------------------------
class BTECAssessmentBase(SQLModel):
    title: str = Field(max_length=255)
    content: str | None = None


class BTECAssessmentCreate(BTECAssessmentBase):
    pass


class BTECAssessment(BTECAssessmentBase, table=True):
    __table_args__ = {"extend_existing": True}
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)


class BTECAssessmentPublic(BTECAssessmentBase):
    id: uuid.UUID
    owner_id: uuid.UUID


# ----------------------------
# Persisted Assessment model (for assistant results)
# ----------------------------
class AssessmentBase(SQLModel):
    question: str
    level: str
    major: str
    difficulty_score: int | None = None
    advice: str | None = None


class AssessmentCreate(AssessmentBase):
    pass


class Assessment(AssessmentBase, table=True):
    __table_args__ = {"extend_existing": True}
    id: int | None = Field(default=None, primary_key=True)
    owner_id: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id", index=True)
    created_at: datetime | None = Field(default=None, sa_column=Column(DateTime(timezone=True), server_default=func.now()))


class AssessmentPublic(AssessmentBase):
    id: int
    owner_id: Optional[uuid.UUID]
    created_at: datetime | None