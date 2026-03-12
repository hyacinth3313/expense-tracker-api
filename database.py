"""
database.py — Sets up the SQLite database and SQLAlchemy session.
SQLAlchemy is an ORM (Object Relational Mapper) — it lets us interact
with the database using Python objects instead of raw SQL queries.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database file — will be created automatically on first run
DATABASE_URL = "sqlite:///./expenses.db"

# The engine is the core connection to the database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Each request gets its own database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class that all our database models will inherit from
Base = declarative_base()


def get_db():
    """
    Dependency function — FastAPI calls this automatically to provide
    a database session to each route, then closes it when done.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
