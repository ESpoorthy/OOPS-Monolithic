"""Run the OOP Student Management demonstration."""
from oops_student_manager.models import GraduateStudent, Student
from oops_student_manager.services import StudentService


def main() -> None:
    service = StudentService()

    student1 = Student("Spoorthy", 20, 101, "CSE-AIML", 92)
    student2 = GraduateStudent(
        "Ananya", 21, 102, "CSE", 85, "Data Science"
    )

    service.add_student(student1)
    service.add_student(student2)

    print("STUDENT MANAGEMENT SYSTEM")
    print("=" * 40)

    print("\n1. Student details")
    print(student1.display_details())

    print("\n2. Graduate student details (overridden methods)")
    print(student2.display_details())

    print("\n3. Encapsulation: update private marks through setter")
    service.update_marks(101, 95)
    print(f"{student1.name}'s updated marks: {student1.get_marks():g}")
    print(f"Updated grade: {student1.calculate_grade()}")

    print("\n4. Operator overloading: add two students' marks")
    print(f"Combined marks: {student1 + student2:g}")

    print("\n5. Class method")
    Student.change_college("BVRIT Hyderabad")
    print(f"Updated college: {student1.college_name}")

    print("\n6. Static method")
    print(f"Is age 20 an adult? {Student.is_adult(20)}")

    print("\n7. Polymorphism")
    for person in service.list_students():
        print(f"{person.name}: {person.calculate_grade()}")


if __name__ == "__main__":
    main()
