# OOP Student Management System — FastAPI + SQLAlchemy + SQLite

## Overview

The application combines an object-oriented Student Management domain with a FastAPI REST interface and persistent SQL storage. It is a modular monolith: routes, services, persistence, and domain models run in one Python application.

## Architecture

    Swagger UI / HTTP Client
             |
         FastAPI app
             |
       Student Routes ---- Pydantic Schemas
             |
       StudentService
          /       \
   OOP Domain    SQLAlchemy ORM
    Models            |
                 SQLite students.db

## Layer responsibilities

| Layer | Module | Responsibility |
|---|---|---|
| API | oops_student_manager/api.py | Creates FastAPI app and includes routers |
| Routes | routes/student_routes.py | HTTP methods, status codes, dependency injection |
| Schemas | schemas/student_schema.py | Validates request and response data |
| Services | services/student_service.py | Coordinates database operations and OOP objects |
| Database | database.py | SQLAlchemy engine, Base, and request-scoped sessions |
| ORM model | db_models.py | Maps the students table to Python attributes |
| Domain models | models/ | OOP state, validation, grading, and behaviour |

## OOP principles

- Abstraction: Person is an abstract base class.
- Encapsulation: Student marks are private and updated through a validated setter.
- Inheritance: Student extends Person; GraduateStudent extends Student.
- Polymorphism: GraduateStudent overrides display_details() and calculate_grade().
- Operator overloading: adding two Student objects returns the sum of their marks.
- Class method: change_college() updates the college name at class level.
- Static method: is_adult() evaluates an age without requiring an object.

## Request lifecycle

1. A client calls an endpoint such as POST /students.
2. FastAPI validates the JSON against StudentCreate.
3. FastAPI injects a request-scoped SQLAlchemy session through get_db().
4. The route constructs a Student or GraduateStudent domain object.
5. StudentService maps the domain object to a StudentRecord ORM row.
6. SQLAlchemy commits the row to the SQLite students table.
7. The route returns a JSON StudentResponse.
8. The request-scoped database session is closed.

For marks updates, the service calls the OOP model's validated set_marks() method before persisting the new value.

## Storage

The default database URL is sqlite:///./students.db. The database file is created automatically. Records survive application restarts. Set DATABASE_URL to use another SQLAlchemy-supported database.

The OOP domain classes remain separate from SQLAlchemy ORM classes: Student and GraduateStudent express business behaviour, while StudentRecord represents persisted rows.

## API surface

| Method | Path | Result |
|---|---|---|
| GET | / | Welcome message |
| GET | /health | Health status |
| POST | /students | Create student; duplicate roll number returns 409 |
| GET | /students | List students |
| GET | /students/{roll_no} | Read one student; 404 when absent |
| PATCH | /students/{roll_no}/marks | Update marks after validation |
| DELETE | /students/{roll_no} | Remove and return a student |

## Run and test

    python -m pip install -r requirements-dev.txt
    uvicorn oops_student_manager.api:app --reload
    python -m pytest -q

Tests use isolated in-memory SQLite databases and do not write to the developer's local database file.