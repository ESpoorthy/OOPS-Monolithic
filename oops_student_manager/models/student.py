"""Student model demonstrating encapsulation and class-level behaviour."""
from .person import Person


class Student(Person):
    """A student with validated marks and standard grading behaviour."""

    college_name = "BVRIT Hyderabad College of Engineering for Women"

    def __init__(
        self,
        name: str,
        age: int,
        roll_no: int,
        branch: str,
        marks: float,
    ) -> None:
        super().__init__(name, age)
        if isinstance(roll_no, bool) or not isinstance(roll_no, int) or roll_no <= 0:
            raise ValueError("Roll number must be a positive integer.")
        if not isinstance(branch, str) or not branch.strip():
            raise ValueError("Branch must be a non-empty string.")
        self.roll_no = roll_no
        self.branch = branch.strip()
        self.__marks = self._validate_marks(marks)

    @staticmethod
    def _validate_marks(marks: float) -> float:
        if isinstance(marks, bool) or not isinstance(marks, (int, float)):
            raise ValueError("Marks must be a number between 0 and 100.")
        if not 0 <= marks <= 100:
            raise ValueError("Marks must be between 0 and 100.")
        return float(marks)

    def get_marks(self) -> float:
        """Read the private marks value."""
        return self.__marks

    def set_marks(self, marks: float) -> None:
        """Update marks only after validating the new value."""
        self.__marks = self._validate_marks(marks)

    def calculate_grade(self) -> str:
        """Convert the student's percentage into a grade."""
        marks = self.__marks
        if marks >= 90:
            return "A"
        if marks >= 80:
            return "B"
        if marks >= 70:
            return "C"
        if marks >= 60:
            return "D"
        return "F"

    def display_details(self) -> str:
        """Return the student's details."""
        return (
            f"Student: {self.name}\n"
            f"Age: {self.age}\n"
            f"Roll number: {self.roll_no}\n"
            f"Branch: {self.branch}\n"
            f"College: {self.college_name}\n"
            f"Marks: {self.__marks:g}\n"
            f"Grade: {self.calculate_grade()}"
        )

    def __add__(self, other: object) -> float:
        """Add the marks of two Student instances."""
        if not isinstance(other, Student):
            return NotImplemented
        return self.__marks + other.__marks

    @classmethod
    def change_college(cls, new_college: str) -> None:
        """Change the college name for this class and its subclasses."""
        if not isinstance(new_college, str) or not new_college.strip():
            raise ValueError("College name must be a non-empty string.")
        cls.college_name = new_college.strip()

    @staticmethod
    def is_adult(age: int) -> bool:
        """Return whether an age represents an adult."""
        if isinstance(age, bool) or not isinstance(age, int) or age < 0:
            raise ValueError("Age must be a non-negative integer.")
        return age >= 18
