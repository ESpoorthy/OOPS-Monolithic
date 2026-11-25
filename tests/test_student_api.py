"""Integration tests for the FastAPI student endpoints using isolated SQLite."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from oops_student_manager.api import app
from oops_student_manager.database import Base, get_db


@pytest.fixture
def client():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=test_engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


def test_root_and_health(client):
    assert client.get("/").status_code == 200
    assert client.get("/health").json() == {"status": "healthy"}


def test_student_crud_flow(client):
    payload = {
        "name": "Spoorthy",
        "age": 20,
        "roll_no": 101,
        "branch": "CSE-AIML",
        "marks": 92,
    }
    created = client.post("/students", json=payload)
    assert created.status_code == 201
    assert created.json()["grade"] == "A"

    assert client.get("/students/101").json()["name"] == "Spoorthy"
    assert len(client.get("/students").json()) == 1

    updated = client.patch("/students/101/marks", json={"marks": 95})
    assert updated.status_code == 200
    assert updated.json()["marks"] == 95
    assert updated.json()["grade"] == "A"

    deleted = client.delete("/students/101")
    assert deleted.status_code == 200
    assert deleted.json()["roll_no"] == 101
    assert client.get("/students/101").status_code == 404


def test_create_graduate_student(client):
    response = client.post(
        "/students",
        json={
            "name": "Ananya",
            "age": 21,
            "roll_no": 102,
            "branch": "CSE",
            "marks": 96,
            "student_type": "graduate",
            "specialization": "Data Science",
        },
    )
    assert response.status_code == 201
    assert response.json()["student_type"] == "graduate"
    assert response.json()["grade"] == "A+"
    assert response.json()["specialization"] == "Data Science"


def test_duplicate_roll_number_returns_conflict(client):
    payload = {
        "name": "Asha",
        "age": 20,
        "roll_no": 5,
        "branch": "CSE",
        "marks": 80,
    }
    assert client.post("/students", json=payload).status_code == 201
    assert client.post("/students", json=payload).status_code == 409


def test_invalid_marks_and_missing_student(client):
    invalid = {
        "name": "Asha",
        "age": 20,
        "roll_no": 8,
        "branch": "CSE",
        "marks": 101,
    }
    assert client.post("/students", json=invalid).status_code == 422
    assert client.patch("/students/999/marks", json={"marks": 90}).status_code == 404


def test_graduate_requires_specialization(client):
    response = client.post(
        "/students",
        json={
            "name": "Mira",
            "age": 22,
            "roll_no": 12,
            "branch": "CSE",
            "marks": 90,
            "student_type": "graduate",
        },
    )
    assert response.status_code == 422


def test_student_data_survives_new_request_session(client):
    payload = {
        "name": "Persistent Student",
        "age": 20,
        "roll_no": 777,
        "branch": "CSE",
        "marks": 88,
    }
    assert client.post("/students", json=payload).status_code == 201
    # A separate HTTP request receives a fresh SQLAlchemy session.
    assert client.get("/students/777").json()["name"] == "Persistent Student"
