"""REST endpoints for the Student Management System."""
from fastapi import APIRouter, Depends, HTTPException, status

from oops_student_manager.models import GraduateStudent, Student
from oops_student_manager.schemas import (
    StudentCreate,
    StudentMarksUpdate,
    StudentResponse,
)
from oops_student_manager.services import StudentService

router = APIRouter(prefix="/students", tags=["Students"])
_student_service = StudentService()


def get_student_service() -> StudentService:
    """Dependency that supplies the in-process student service."""
    return _student_service


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


@router.post(
    "",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_student(
    payload: StudentCreate,
    service: StudentService = Depends(get_student_service),
) -> StudentResponse:
    """Create either a regular or graduate student."""
    if payload.student_type == "graduate" and not (
        payload.specialization and payload.specialization.strip()
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Specialization is required for a graduate student.",
        )
    if payload.student_type == "student" and payload.specialization:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Specialization is only valid for a graduate student.",
        )
    if any(s.roll_no == payload.roll_no for s in service.list_students()):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Roll number {payload.roll_no} already exists.",
        )

    try:
        if payload.student_type == "graduate":
            student = GraduateStudent(
                name=payload.name,
                age=payload.age,
                roll_no=payload.roll_no,
                branch=payload.branch,
                marks=payload.marks,
                specialization=payload.specialization or "",
            )
        else:
            student = Student(
                name=payload.name,
                age=payload.age,
                roll_no=payload.roll_no,
                branch=payload.branch,
                marks=payload.marks,
            )
        service.add_student(student)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    return _to_response(student)


@router.get("", response_model=list[StudentResponse])
def list_students(
    service: StudentService = Depends(get_student_service),
) -> list[StudentResponse]:
    """Return all students ordered by roll number."""
    return [
        _to_response(student)
        for student in sorted(service.list_students(), key=lambda item: item.roll_no)
    ]


@router.get("/{roll_no}", response_model=StudentResponse)
def get_student(
    roll_no: int,
    service: StudentService = Depends(get_student_service),
) -> StudentResponse:
    """Return one student by roll number."""
    try:
        return _to_response(service.get_student(roll_no))
    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc).strip("'"),
        ) from exc


@router.patch("/{roll_no}/marks", response_model=StudentResponse)
def update_student_marks(
    roll_no: int,
    payload: StudentMarksUpdate,
    service: StudentService = Depends(get_student_service),
) -> StudentResponse:
    """Update marks through the model's validated setter."""
    try:
        student = service.update_marks(roll_no, payload.marks)
    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc).strip("'"),
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    return _to_response(student)


@router.delete("/{roll_no}", response_model=StudentResponse)
def delete_student(
    roll_no: int,
    service: StudentService = Depends(get_student_service),
) -> StudentResponse:
    """Remove and return a student."""
    try:
        return _to_response(service.remove_student(roll_no))
    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc).strip("'"),
        ) from exc
