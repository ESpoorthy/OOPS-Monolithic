"""Tests for the OOP Student Management package."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from oops_student_manager.database import Base
from oops_student_manager.models import GraduateStudent, Person, Student
from oops_student_manager.services import StudentService


def make_student(roll_no: int = 1, marks: float = 85) -> Student:
    return Student("Asha", 20, roll_no, "CSE", marks)


@pytest.fixture
def service():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    yield StudentService(db)
    db.close()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


def test_person_is_abstract():
    with pytest.raises(TypeError):
        Person("Asha", 20)


def test_student_encapsulation_and_validation():
    student = make_student()
    assert student.get_marks() == 85
    student.set_marks(95)
    assert student.get_marks() == 95
    with pytest.raises(ValueError):
        student.set_marks(101)


def test_graduate_inheritance_and_overriding():
    graduate = GraduateStudent("Mira", 22, 2, "CSE", 96, "AI")
    assert isinstance(graduate, Student)
    assert graduate.calculate_grade() == "A+"
    assert "Specialization: AI" in graduate.display_details()


def test_operator_overloading():
    assert make_student(marks=90) + make_student(2, 80) == 170


def test_class_and_static_methods():
    original = Student.college_name
    try:
        Student.change_college("Example College")
        assert make_student().college_name == "Example College"
        assert Student.is_adult(18) is True
        assert Student.is_adult(17) is False
    finally:
        Student.college_name = original


def test_service_add_get_update_remove(service):
    student = make_student()
    service.add_student(student)
    assert service.get_student(1).name == "Asha"
    service.update_marks(1, 91)
    assert service.get_student(1).get_marks() == 91
    assert service.remove_student(1).roll_no == 1
    assert service.list_students() == []


def test_service_rejects_duplicate_roll_number(service):
    service.add_student(make_student())
    with pytest.raises(ValueError):
        service.add_student(make_student())


def test_student_validates_constructor_fields():
    with pytest.raises(ValueError):
        Student("Asha", 20, 0, "CSE", 80)
    with pytest.raises(ValueError):
        Student("Asha", 20, 3, "CSE", 101)
