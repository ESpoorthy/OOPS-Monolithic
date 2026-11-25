"""Abstract base class shared by people in the system."""
from abc import ABC, abstractmethod


class Person(ABC):
    """Represent a person; subclasses must define display_details."""

    def __init__(self, name: str, age: int) -> None:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string.")
        if isinstance(age, bool) or not isinstance(age, int) or age < 0:
            raise ValueError("Age must be a non-negative integer.")
        self.name = name.strip()
        self.age = age

    @abstractmethod
    def display_details(self) -> str:
        """Return a human-readable description of this person."""
        raise NotImplementedError
