"""In-memory student operations kept separate from domain models."""
from __future__ import annotations

from typing import Iterable
from oops_student_manager.models import Student


class StudentService:
    """Manage students in memory; persistence can be added independently."""

    def __init__(self, students: Iterable[Student] | None = None) -> None:
        self._students: dict[int, Student] = {}
        for student in students or ():
            self.add_student(student)

    def add_student(self, student: Student) -> None:
        if not isinstance(student, Student):
            raise TypeError("Only Student instances can be added.")
        if student.roll_no in self._students:
            raise ValueError(f"Roll number {student.roll_no} already exists.")
        self._students[student.roll_no] = student

    def get_student(self, roll_no: int) -> Student:
        try:
            return self._students[roll_no]
        except KeyError as exc:
            raise KeyError(f"No student found with roll number {roll_no}.") from exc

    def list_students(self) -> list[Student]:
        return list(self._students.values())

    def update_marks(self, roll_no: int, marks: float) -> Student:
        student = self.get_student(roll_no)
        student.set_marks(marks)
        return student

    def remove_student(self, roll_no: int) -> Student:
        try:
            return self._students.pop(roll_no)
        except KeyError as exc:
            raise KeyError(f"No student found with roll number {roll_no}.") from exc
