"""SQLAlchemy persistence models (kept separate from OOP domain models)."""
from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from oops_student_manager.database import Base


class StudentRecord(Base):
    """Database representation of a student or graduate student."""

    __tablename__ = "students"

    roll_no: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    branch: Mapped[str] = mapped_column(String(100), nullable=False)
    marks: Mapped[float] = mapped_column(Float, nullable=False)
    student_type: Mapped[str] = mapped_column(String(20), nullable=False, default="student")
    specialization: Mapped[str | None] = mapped_column(String(100), nullable=True)
