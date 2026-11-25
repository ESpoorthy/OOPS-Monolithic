# OOPS-Monolithic

A Python project demonstrating object-oriented programming through a modular Student Management System.

## Features and OOP concepts

- **Abstraction:** abstract `Person` base class.
- **Encapsulation:** private student marks with validated getter/setter methods.
- **Inheritance:** `Student` extends `Person`; `GraduateStudent` extends `Student`.
- **Polymorphism:** graduate students override `display_details()` and `calculate_grade()`.
- **Operator overloading:** `+` combines the marks of two students.
- **Class method:** updates the college name for the class.
- **Static method:** checks whether an age represents an adult.
- **Modular organization:** domain models, service logic, entry point, and tests are separated.

## Project structure

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
OOPS_ARCHITECTURE.md
```

## Run the application

Python 3.10 or newer is recommended. From the repository root:

```bash
python -m oops_student_manager.main
```

No third-party dependency is required to run the example.

## Run tests

Install the development dependency and execute the tests:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

## Architecture

See [OOPS_ARCHITECTURE.md](OOPS_ARCHITECTURE.md) for the component diagram, module responsibilities, execution flow, and design decisions.

The models own domain behaviour and validation. `StudentService` manages an in-memory collection of students. `main.py` wires the components together and demonstrates the concepts. Everything runs in one Python process; this is a modular monolith, not a microservices architecture.
