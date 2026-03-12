"""
schemas.py — Pydantic models for request validation and response formatting.
Pydantic automatically validates incoming data types and returns clear errors
if the user sends bad data (e.g. text instead of a number for amount).
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from models import CategoryEnum


class ExpenseCreate(BaseModel):
    """Schema for creating a new expense — what the user sends in the request body."""
    title:    str            = Field(..., min_length=1, max_length=100, example="Lunch at cafe")
    amount:   float          = Field(..., gt=0, example=150.00)
    category: CategoryEnum   = Field(default=CategoryEnum.OTHER, example="food")
    note:     Optional[str]  = Field(None, max_length=300, example="Ate out with friends")


class ExpenseUpdate(BaseModel):
    """Schema for updating — all fields optional so user can update just one field."""
    title:    Optional[str]          = Field(None, min_length=1, max_length=100)
    amount:   Optional[float]        = Field(None, gt=0)
    category: Optional[CategoryEnum] = None
    note:     Optional[str]          = Field(None, max_length=300)


class ExpenseResponse(BaseModel):
    """Schema for what we send back to the user — includes DB-generated fields."""
    id:         int
    title:      str
    amount:     float
    category:   CategoryEnum
    note:       Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True  # Lets Pydantic read SQLAlchemy model objects directly


class SummaryResponse(BaseModel):
    """Schema for the spending summary endpoint."""
    total_expenses:     int
    total_amount:       float
    average_amount:     float
    highest_expense:    float
    by_category:        dict
