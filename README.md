# OOPS-Monolithic

A Python OOP Student Management System with a FastAPI REST backend and SQLite persistence. The project separates HTTP routing, application services, SQLAlchemy persistence, and OOP domain models in one modular monolith.

## Features
- Create, list, retrieve, update marks with PATCH or PUT, and delete students through REST endpoints.
- Create regular and graduate students.
- Persist records in the local SQLite database file students.db.
- Use SQLAlchemy ORM to map database rows to Python objects.
- Demonstrate abstraction, encapsulation, inheritance, polymorphism, and operator overloading.

## Project structure

    oops_student_manager/
      api.py
      database.py       # SQLAlchemy engine, Base, and session dependency
      db_models.py      # SQLAlchemy table model
      models/           # OOP domain classes
      routes/           # FastAPI endpoints
      schemas/          # Pydantic schemas
      services/         # Business operations and persistence coordination
    tests/

## Run

    python -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements-dev.txt
    uvicorn oops_student_manager.api:app --reload

The application creates students.db automatically. Records remain available after the server restarts. Open http://127.0.0.1:8000/docs for Swagger UI.

## Database configuration

The default SQLAlchemy URL is sqlite:///./students.db. Set the DATABASE_URL environment variable before starting the API to use another SQLAlchemy-supported database. Keep database credentials out of source control.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | / | Welcome message |
| GET | /health | Health check |
| POST | /students | Create a student |
| GET | /students | List students |
| GET | /students/{roll_no} | Get one student |
| PATCH | /students/{roll_no}/marks | Partially update marks |\n| PUT | /students/{roll_no}/marks | Update marks (same operation) |
| DELETE | /students/{roll_no} | Delete a student |

## Tests

    python -m pytest -q

Tests use isolated in-memory SQLite databases and do not modify your local students.db file.

See OOPS_ARCHITECTURE.md for the architecture and request flow.