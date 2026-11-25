"""Pydantic request and response schemas for the HTTP API."""
from .student_schema import StudentCreate, StudentMarksUpdate, StudentResponse

__all__ = ["StudentCreate", "StudentMarksUpdate", "StudentResponse"]
