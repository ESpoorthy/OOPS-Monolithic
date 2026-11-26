"""SQLAlchemy database configuration with PostgreSQL and SQLite support."""
import os
from collections.abc import Generator
from threading import Lock

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

_raw_database_url = os.getenv("DATABASE_URL", "sqlite:///./students.db")

# Hosted PostgreSQL providers commonly supply postgres:// or postgresql:// URLs.
# Use psycopg 3 explicitly so the required driver is unambiguous.
if _raw_database_url.startswith("postgres://"):
    DATABASE_URL = _raw_database_url.replace("postgres://", "postgresql+psycopg://", 1)
elif _raw_database_url.startswith("postgresql://"):
    DATABASE_URL = _raw_database_url.replace("postgresql://", "postgresql+psycopg://", 1)
else:
    DATABASE_URL = _raw_database_url

_url = make_url(DATABASE_URL)
connect_args = {"check_same_thread": False} if _url.get_backend_name() == "sqlite" else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy table models."""


_initialization_lock = Lock()
_database_initialized = False


def init_db() -> None:
    """Create missing tables once, when the database is first needed."""
    global _database_initialized
    if _database_initialized:
        return

    with _initialization_lock:
        if not _database_initialized:
            # Import the ORM models before create_all so their tables are registered.
            from oops_student_manager import db_models  # noqa: F401

            Base.metadata.create_all(bind=engine)
            _database_initialized = True


def get_db() -> Generator[Session, None, None]:
    """Yield one database session per request and always close it."""
    init_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
