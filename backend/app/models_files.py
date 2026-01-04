from __future__ import annotations
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
import uuid

class UserFileBase(SQLModel):
    original_filename: str
    stored_path: str
    content_type: Optional[str] = None
    size: Optional[int] = None

class UserFile(UserFileBase, table=True):
    __tablename__ = "user_file"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    owner_id: str = Field(index=True, nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow())

class UserFilePublic(SQLModel):
    id: str
    original_filename: str
    content_type: Optional[str]
    created_at: datetime
