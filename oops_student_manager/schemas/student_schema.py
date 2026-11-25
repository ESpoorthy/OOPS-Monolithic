"""HTTP validation and response schemas for students."""
from typing import Literal

from pydantic import BaseModel, Field


class StudentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=120)
    roll_no: int = Field(gt=0)
    branch: str = Field(min_length=1, max_length=100)
    marks: float = Field(ge=0, le=100)
    student_type: Literal["student", "graduate"] = "student"
    specialization: str | None = Field(default=None, max_length=100)


class StudentMarksUpdate(BaseModel):
    marks: float = Field(ge=0, le=100)


class StudentResponse(BaseModel):
    name: str
    age: int
    roll_no: int
    branch: str
    marks: float
    grade: str
    college_name: str
    student_type: Literal["student", "graduate"]
    specialization: str | None = None
