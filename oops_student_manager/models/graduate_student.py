"""Graduate student model demonstrating inheritance and overriding."""
from .student import Student


class GraduateStudent(Student):
    """A student with a specialization and graduate-specific grading."""

    def __init__(
        self,
        name: str,
        age: int,
        roll_no: int,
        branch: str,
        marks: float,
        specialization: str,
    ) -> None:
        super().__init__(name, age, roll_no, branch, marks)
        if not isinstance(specialization, str) or not specialization.strip():
            raise ValueError("Specialization must be a non-empty string.")
        self.specialization = specialization.strip()

    def calculate_grade(self) -> str:
        """Apply a graduate-specific distinction threshold."""
        marks = self.get_marks()
        if marks >= 95:
            return "A+"
        return super().calculate_grade()

    def display_details(self) -> str:
        """Override display while reusing the parent implementation."""
        return f"{super().display_details()}\nSpecialization: {self.specialization}"
