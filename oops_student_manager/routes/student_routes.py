"""REST endpoints for the Student Management System."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from oops_student_manager.database import Base, engine, get_db
from oops_student_manager.db_models import StudentRecord
from oops_student_manager.models import GraduateStudent, Student
from oops_student_manager.schemas import StudentCreate, StudentMarksUpdate, StudentResponse
from oops_student_manager.services import StudentService

# Create the SQLite table when the application starts/imports.
Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/students", tags=["Students"])


def get_student_service(db: Session = Depends(get_db)) -> StudentService:
    """Provide a service connected to the request-scoped database session."""
    return StudentService(db)


def _to_response(student: Student) -> StudentResponse:
    is_graduate = isinstance(student, GraduateStudent)
    return StudentResponse(
        name=student.name,
        age=student.age,
        roll_no=student.roll_no,
        branch=student.branch,
        marks=student.get_marks(),
        grade=student.calculate_grade(),
        college_name=student.college_name,
        student_type="graduate" if is_graduate else "student",
        specialization=student.specialization if is_graduate else None,
    )


@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(
    payload: StudentCreate,
    service: StudentService = Depends(get_student_service),
) -> StudentResponse:
    """Create either a regular or graduate student."""
    if payload.student_type == "graduate" and not (
        payload.specialization and payload.specialization.strip()
    ):
        raise HTTPException(status_code=422, detail="Specialization is required for a graduate student.")
    if payload.student_type == "student" and payload.specialization:
        raise HTTPException(status_code=422, detail="Specialization is only valid for a graduate student.")
    try:
        if payload.student_type == "graduate":
            student = GraduateStudent(
                name=payload.name, age=payload.age, roll_no=payload.roll_no,
                branch=payload.branch, marks=payload.marks,
                specialization=payload.specialization or "",
            )
        else:
            student = Student(
                name=payload.name, age=payload.age, roll_no=payload.roll_no,
                branch=payload.branch, marks=payload.marks,
            )
        service.add_student(student)
    except ValueError as exc:
        code = status.HTTP_409_CONFLICT if "already exists" in str(exc) else status.HTTP_422_UNPROCESSABLE_ENTITY
        raise HTTPException(status_code=code, detail=str(exc)) from exc
    return _to_response(student)


@router.get("", response_model=list[StudentResponse])
def list_students(service: StudentService = Depends(get_student_service)) -> list[StudentResponse]:
    """Return all students ordered by roll number."""
    return [_to_response(student) for student in service.list_students()]


@router.get("/{roll_no}", response_model=StudentResponse)
def get_student(
    roll_no: int, service: StudentService = Depends(get_student_service)
) -> StudentResponse:
    """Return one student by roll number."""
    try:
        return _to_response(service.get_student(roll_no))
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc).strip("'")) from exc


@router.patch("/{roll_no}/marks", response_model=StudentResponse)
def update_student_marks(
    roll_no: int,
    payload: StudentMarksUpdate,
    service: StudentService = Depends(get_student_service),
) -> StudentResponse:
    """Update marks through the model's validated setter."""
    try:
        return _to_response(service.update_marks(roll_no, payload.marks))
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc).strip("'")) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.delete("/{roll_no}", response_model=StudentResponse)
def delete_student(
    roll_no: int, service: StudentService = Depends(get_student_service)
) -> StudentResponse:
    """Remove and return a student."""
    try:
        return _to_response(service.remove_student(roll_no))
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc).strip("'")) from exc
