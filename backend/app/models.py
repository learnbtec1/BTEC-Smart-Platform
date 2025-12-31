from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="student")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"

class BTECAssessment(Base):
    __tablename__ = "btec_assessments"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String, index=True, nullable=False)
    competency_unit = Column(String, index=True, nullable=False)
    score = Column(Float, nullable=False)
    feedback = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User")

    def __repr__(self):
        return f"<BTECAssessment(id={self.id}, student_name='{self.student_name}', score={self.score})>"
