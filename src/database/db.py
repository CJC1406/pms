
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# Find the root directory of the PMS project.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# SQLite database file in the project root.
DATABASE_PATH = PROJECT_ROOT / "pms.db"

# Configure the SQLite database connection.
engine = create_engine(
    f"sqlite:///{DATABASE_PATH.as_posix()}",
    connect_args={"check_same_thread": False},
)

# Factory for creating database sessions.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""


def init_db() -> None:
    """Create database tables for all registered models."""
    # Import models so SQLAlchemy registers their tables.
    from src.models.batch import Batch  # noqa: F401
    from src.models.product import Product  # noqa: F401

    Base.metadata.create_all(bind=engine)

