from __future__ import annotations
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
import uuid

class StudentProgressBase(SQLModel):
    lesson_id: Optional[str] = None
    progress_percentage: int = 0
    last_score: Optional[float] = None
    attempts: int = 0
    struggling: bool = False

class StudentProgress(StudentProgressBase, table=True):
    __tablename__ = "student_progress"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(index=True, nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.utcnow())

class StudentProgressCreate(StudentProgressBase):
    lesson_id: Optional[str] = None

class StudentProgressUpdate(SQLModel):
    progress_percentage: Optional[int] = None
    last_score: Optional[float] = None
    attempts: Optional[int] = None
    struggling: Optional[bool] = None

class StudentProgressPublic(StudentProgress):
    pass
