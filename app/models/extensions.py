"""
app/extensions.py
-----------------
Central place for SQLAlchemy setup.
Provides Base (declarative base) and get_db() context manager.
"""
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Declarative base all models inherit from this
Base = declarative_base()

# Database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///attendify.db")

# Engine and session factory
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db():
    """
    Yields a database session and ensures it's properly closed.
    Usage:
        with get_db() as db:
            # use db here
            db.commit()
    """
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db():
    """Create all tables defined by models that inherit from Base."""
    Base.metadata.create_all(bind=engine)