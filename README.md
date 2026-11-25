# OOPS-Monolithic

This repository contains two independent examples of modular-monolith organization:

1. **OOP Student Management System** — a Python OOP learning project that splits a single-file student example into domain models, a service layer, a runnable entry point, tests, and architecture notes.
2. **AgriN Connect FastAPI backend** — the existing API project under `app/`, retained without being overwritten.

## OOP Student Management System

The OOP example is in [`oops_student_manager/`](oops_student_manager/README.md). It demonstrates abstraction, encapsulation, inheritance, polymorphism, operator overloading, class methods, and static methods.

Run the demonstration from the repository root:

```bash
python -m oops_student_manager.main
```

Run its tests:

```bash
pip install -r requirements-dev.txt
python -m pytest tests/test_oops_student_manager.py -q
```

See [`OOPS_ARCHITECTURE.md`](OOPS_ARCHITECTURE.md) for the package diagram, responsibilities, and execution flow.

### OOP package layout

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

## Existing AgriN Connect API

The existing FastAPI backend remains under `app/`. Its API setup and run instructions are documented in [`AGRI` README history?](ARCHITECTURE.md).

Run it from the repository root:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API documentation: http://127.0.0.1:8000/docs

The OOP package and FastAPI API have separate entry points. The OOP demo does not import or depend on the FastAPI application.

## Test suite

Run all tests:

```bash
pip install -r requirements-dev.txt
python -m pytest -q
```

The full suite includes both the existing API tests and the OOP student-management tests.
