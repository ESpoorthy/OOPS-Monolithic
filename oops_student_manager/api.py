"""FastAPI application for the OOP Student Management System."""
from fastapi import FastAPI

from oops_student_manager.routes import student_router

app = FastAPI(
    title="OOP Student Management API",
    description=(
        "A REST API backed by an object-oriented Student Management System. "
        "The domain models demonstrate abstraction, encapsulation, inheritance, "
        "polymorphism, and operator overloading."
    ),
    version="1.0.0",
)

app.include_router(student_router)


@app.get("/", tags=["Health"])
def root() -> dict[str, str]:
    return {
        "message": "Welcome to the OOP Student Management API",
        "docs": "/docs",
        "students_endpoint": "/students",
    }


@app.get("/health", tags=["Health"])
def health() -> dict[str, str]:
    return {"status": "healthy"}
