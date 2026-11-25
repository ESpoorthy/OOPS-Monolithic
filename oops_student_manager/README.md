# OOP Student Management System

A small, dependency-light Python project that demonstrates object-oriented programming and a simple modular-monolith organization. The OOP domain example lives in this package, independently of the repository's existing FastAPI application.

## Run

From the repository root:

```bash
python -m oops_student_manager.main
```

No third-party package is needed to run the demo.

## Structure

```text
oops_student_manager/
├── main.py
├── models/
│   ├── person.py
│   ├── student.py
│   └── graduate_student.py
└── services/
    └── student_service.py
tests/
└── test_oops_student_manager.py
```

## OOP concepts demonstrated

| Concept | Where it appears |
|---|---|
| Class and objects | `Student` and `GraduateStudent` instances in `main.py` |
| Abstraction | Abstract `Person` class and `display_details()` contract |
| Encapsulation | Private `Student.__marks`, `get_marks()`, and validated `set_marks()` |
| Inheritance | `Student(Person)` and `GraduateStudent(Student)` |
| Polymorphism | Overridden `display_details()` and `calculate_grade()` |
| Operator overloading | `Student.__add__()` adds marks |
| Class method | `Student.change_college()` updates the class-level college |
| Static method | `Student.is_adult()` checks adult status |
| `super()` | Child constructors and overridden methods reuse parent behaviour |

## Design boundaries

- **Models** own the student/person data and OOP behaviour.
- **Services** own in-memory student collection operations.
- **main.py** wires the example together and demonstrates the concepts.
- The service uses an in-memory dictionary; data resets when the process exits.

## Tests

Install the existing development requirements from the repository root and run:

```bash
python -m pytest tests/test_oops_student_manager.py -q
```
