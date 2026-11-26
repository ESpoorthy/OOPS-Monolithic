# OOPS-Monolithic

A Python OOP Student Management System with a FastAPI REST backend and SQLAlchemy persistence. PostgreSQL is supported as the production database, while SQLite remains available as a lightweight local-development fallback. The project separates HTTP routing, application services, SQLAlchemy persistence, and OOP domain models in one modular monolith.

## Features
- Create, list, retrieve, update marks with PATCH or PUT, and delete students through REST endpoints.
- Create regular and graduate students.
- Persist records using SQLAlchemy with PostgreSQL or SQLite.
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

## Install and run

    python -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements-dev.txt

### Use PostgreSQL

Create a PostgreSQL database (for example, `student_management`) and set the connection URL before starting the API.

macOS/Linux:

    export DATABASE_URL="postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/student_management"

PowerShell:

    $env:DATABASE_URL = "postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/student_management"

Then run:

    uvicorn oops_student_manager.api:app --reload

The application creates missing tables the first time the database is accessed. Keep database credentials in environment variables or a local, untracked `.env` file; never commit secrets.

### Use SQLite for quick local development

If `DATABASE_URL` is not set, the application uses `sqlite:///./students.db`.

Open http://127.0.0.1:8000/docs for Swagger UI.

## Database configuration

The `DATABASE_URL` environment variable selects the database. PostgreSQL URLs using `postgresql://` or `postgres://` are normalized to the psycopg 3 driver. SQLite remains the fallback for local development. For production deployments, use a managed PostgreSQL database and a migration tool such as Alembic when schema changes need to be versioned.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | / | Welcome message |
| GET | /health | Health check |
| POST | /students | Create a student |
| GET | /students | List students |
| GET | /students/{roll_no} | Get one student |
| PATCH | /students/{roll_no}/marks | Partially update marks |
| PUT | /students/{roll_no}/marks | Update marks (same operation) |
| DELETE | /students/{roll_no} | Delete a student |

## Tests

    python -m pytest -q

Tests use the PostgreSQL service in GitHub Actions. Locally, they use isolated in-memory SQLite unless `TEST_DATABASE_URL` is set to a PostgreSQL test database. Tests create and drop their own tables; do not point `TEST_DATABASE_URL` at a database containing data you need to keep.

See OOPS_ARCHITECTURE.md for the architecture and request flow.
