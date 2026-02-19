import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    """Base class for ORM models."""


def build_database_url() -> str:
    """Build PostgreSQL connection URL from environment variables."""
    db_user = os.getenv("DB_USER", "finance_user")
    db_password = os.getenv("DB_PASSWORD", "finance_pass")
    # Default to localhost for non-Docker local runs.
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "finance_tracker")
    return f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


DATABASE_URL = os.getenv("DATABASE_URL", build_database_url())

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
