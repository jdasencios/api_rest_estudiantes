from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from pydantic import BaseModel, Field


from database.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    dni = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    grade = Column(Float, nullable=False)
    is_approved = Column(Boolean, nullable=False)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)


class StudentCreate(BaseModel):
    dni: str = Field(..., min_length=8, max_length=8)
    name: str = Field(..., min_length=2)
    age: int = Field(..., ge=1, le=120)
    grade: float = Field(..., ge=0, le=20)
    is_approved: bool


class StudentUpdate(BaseModel):
    dni: str = Field(..., min_length=8, max_length=8)
    name: str = Field(..., min_length=2)
    age: int = Field(..., ge=1, le=120)
    grade: float = Field(..., ge=0, le=20)
    is_approved: bool


class StudentResponse(BaseModel):
    id: int
    dni: str
    name: str
    age: int
    grade: float
    is_approved: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True