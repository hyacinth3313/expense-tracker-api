"""
models.py — Defines the database table structure using SQLAlchemy.
Each class here maps to a table in the SQLite database.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.sql import func
from database import Base
import enum


class CategoryEnum(str, enum.Enum):
    """Allowed expense categories."""
    FOOD        = "food"
    TRANSPORT   = "transport"
    SHOPPING    = "shopping"
    HEALTH      = "health"
    EDUCATION   = "education"
    OTHER       = "other"


class Expense(Base):
    """
    Maps to the 'expenses' table in the database.
    Each attribute = one column in the table.
    """
    __tablename__ = "expenses"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String, nullable=False)
    amount      = Column(Float, nullable=False)
    category    = Column(Enum(CategoryEnum), default=CategoryEnum.OTHER)
    note        = Column(String, nullable=True)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
