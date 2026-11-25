# OOPS-Monolithic

A Python **OOP Student Management System with a FastAPI REST backend**. The project keeps object-oriented domain logic separate from HTTP routing and request validation, while running as one deployable application (a modular monolith).

## Features

- Create, list, retrieve, update marks, and delete students through REST endpoints.
- Create both regular and graduate students.
- Validate roll numbers, ages, branches, marks, and graduate specializations.
- Keep student data in memory for this learning project (data resets when the server stops).
- Demonstrate core OOP concepts in the model layer.

## OOP concepts

| Concept | Implementation |
|---|---|
| Abstraction | Abstract `Person` class |
| Encapsulation | Private `Student.__marks` and validated getter/setter |
| Inheritance | `Student(Person)`, `GraduateStudent(Student)` |
| Polymorphism | Graduate overrides `display_details()` and `calculate_grade()` |
| Operator overloading | `Student.__add__()` combines marks |
| Class method | `Student.change_college()` |
| Static method | `Student.is_adult()` |
| Composition / separation | FastAPI routes call `StudentService`, which works with domain models |

## Project structure

```text
oops_student_manager/
├── api.py
├── main.py
├── models/
│   ├── person.py
│   ├── student.py
│   └── graduate_student.py
├── routes/
│   └── student_routes.py
├── schemas/
│   └── student_schema.py
└── services/
    └── student_service.py
tests/
├── test_oops_student_manager.py
└── test_student_api.py
OOPS_ARCHITECTURE.md
requirements.txt
requirements-dev.txt
```

## Run the FastAPI application

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
python -m pip install -r requirements-dev.txt
uvicorn oops_student_manager.api:app --reload
```

Open the interactive API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Welcome message and API links |
| GET | `/health` | Health check |
| POST | `/students` | Create a regular or graduate student |
| GET | `/students` | List all students |
| GET | `/students/{roll_no}` | Get one student |
| PATCH | `/students/{roll_no}/marks` | Update student marks |
| DELETE | `/students/{roll_no}` | Delete a student |

### Example: create a student

Send this JSON body to `POST /students`:

```json
{
  "name": "Spoorthy",
  "age": 20,
  "roll_no": 101,
  "branch": "CSE-AIML",
  "marks": 92
}
```

### Example: create a graduate student

Send this JSON body to `POST /students`:

```json
{
  "name": "Ananya",
  "age": 21,
  "roll_no": 102,
  "branch": "CSE",
  "marks": 96,
  "student_type": "graduate",
  "specialization": "Data Science"
}
```

### Example: update marks

Send `PATCH /students/101/marks`:

```json
{
  "marks": 95
}
```

## Run the OOP console demonstration

The original object-oriented demonstration is still available:

```bash
python -m oops_student_manager.main
```

## Tests

Run all model, service, and API tests:

```bash
python -m pytest -q
```

The tests use an isolated in-memory service per API test; they do not depend on a running server or external database.

## Architecture

See [OOPS_ARCHITECTURE.md](OOPS_ARCHITECTURE.md) for the layers, component diagram, request flow, and design decisions.
