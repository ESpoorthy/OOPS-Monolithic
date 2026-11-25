"""SQLAlchemy table definitions, kept separate from OOP domain models."""
from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from oops_student_manager.db import Base


class StudentRecord(Base):
    """Persistent database representation of a student."""

    __tablename__ = "students"

    roll_no: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    branch: Mapped[str] = mapped_column(String(100), nullable=False)
    marks: Mapped[float] = mapped_column(Float, nullable=False)
    college_name: Mapped[str] = mapped_column(
        String(200), nullable=False,
        default="BVRIT Hyderabad College of Engineering for Women",
    )
    student_type: Mapped[str] = mapped_column(
        String(20), nullable=False, default="student"
    )
    specialization: Mapped[str | None] = mapped_column(String(100), nullable=True)
