"""Student operations backed by SQLAlchemy persistence."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from oops_student_manager.db_models import StudentRecord
from oops_student_manager.models import GraduateStudent, Student


class StudentService:
    """Coordinate database records and the existing OOP domain objects."""

    def __init__(self, db: Session) -> None:
        self.db = db

    @staticmethod
    def _to_domain(record: StudentRecord) -> Student:
        if record.student_type == "graduate":
            return GraduateStudent(
                name=record.name, age=record.age, roll_no=record.roll_no,
                branch=record.branch, marks=record.marks,
                specialization=record.specialization or "",
            )
        return Student(
            name=record.name, age=record.age, roll_no=record.roll_no,
            branch=record.branch, marks=record.marks,
        )

    @staticmethod
    def _to_record(student: Student) -> StudentRecord:
        is_graduate = isinstance(student, GraduateStudent)
        return StudentRecord(
            name=student.name, age=student.age, roll_no=student.roll_no,
            branch=student.branch, marks=student.get_marks(),
            student_type="graduate" if is_graduate else "student",
            specialization=student.specialization if is_graduate else None,
        )

    def add_student(self, student: Student) -> Student:
        if not isinstance(student, Student):
            raise TypeError("Only Student instances can be added.")
        if self.db.get(StudentRecord, student.roll_no) is not None:
            raise ValueError(f"Roll number {student.roll_no} already exists.")
        self.db.add(self._to_record(student))
        self.db.commit()
        return student

    def get_student(self, roll_no: int) -> Student:
        record = self.db.get(StudentRecord, roll_no)
        if record is None:
            raise KeyError(f"No student found with roll number {roll_no}.")
        return self._to_domain(record)

    def list_students(self) -> list[Student]:
        records = self.db.scalars(
            select(StudentRecord).order_by(StudentRecord.roll_no)
        ).all()
        return [self._to_domain(record) for record in records]

    def update_marks(self, roll_no: int, marks: float) -> Student:
        record = self.db.get(StudentRecord, roll_no)
        if record is None:
            raise KeyError(f"No student found with roll number {roll_no}.")
        student = self._to_domain(record)
        student.set_marks(marks)
        record.marks = student.get_marks()
        self.db.commit()
        return student

    def remove_student(self, roll_no: int) -> Student:
        record = self.db.get(StudentRecord, roll_no)
        if record is None:
            raise KeyError(f"No student found with roll number {roll_no}.")
        student = self._to_domain(record)
        self.db.delete(record)
        self.db.commit()
        return student
