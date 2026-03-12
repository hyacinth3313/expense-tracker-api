"""
main.py — The core FastAPI application.
Defines all API routes (endpoints) and their logic.

Run with:  uvicorn main:app --reload
Docs at:   http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime

import models, schemas
from database import engine, get_db, Base
from models import CategoryEnum

# Create all database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="💸 Expense Tracker API",
    description="A REST API to track personal expenses — built with FastAPI + SQLite.",
    version="1.0.0"
)


# ─────────────────────────────────────────────
#  ROOT
# ─────────────────────────────────────────────

@app.get("/", tags=["General"])
def root():
    """Health check — confirms the API is running."""
    return {"message": "Expense Tracker API is running!", "docs": "/docs"}


# ─────────────────────────────────────────────
#  CREATE
# ─────────────────────────────────────────────

@app.post("/expenses", response_model=schemas.ExpenseResponse, status_code=201, tags=["Expenses"])
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    """
    Add a new expense.
    - **title**: Name of the expense
    - **amount**: Amount spent (must be > 0)
    - **category**: One of: food, transport, shopping, health, education, other
    - **note**: Optional extra detail
    """
    new_expense = models.Expense(**expense.model_dump())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


# ─────────────────────────────────────────────
#  READ ALL (with optional filters)
# ─────────────────────────────────────────────

@app.get("/expenses", response_model=List[schemas.ExpenseResponse], tags=["Expenses"])
def get_all_expenses(
    category: Optional[CategoryEnum] = Query(None, description="Filter by category"),
    min_amount: Optional[float]      = Query(None, description="Minimum amount"),
    max_amount: Optional[float]      = Query(None, description="Maximum amount"),
    db: Session = Depends(get_db)
):
    """
    Get all expenses. Optionally filter by category or amount range.
    Example: /expenses?category=food&max_amount=500
    """
    query = db.query(models.Expense)

    if category:
        query = query.filter(models.Expense.category == category)
    if min_amount is not None:
        query = query.filter(models.Expense.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(models.Expense.amount <= max_amount)

    return query.order_by(models.Expense.created_at.desc()).all()


# ─────────────────────────────────────────────
#  READ ONE
# ─────────────────────────────────────────────

@app.get("/expenses/{expense_id}", response_model=schemas.ExpenseResponse, tags=["Expenses"])
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    """Get a single expense by its ID."""
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail=f"Expense with id {expense_id} not found")
    return expense


# ─────────────────────────────────────────────
#  UPDATE
# ─────────────────────────────────────────────

@app.patch("/expenses/{expense_id}", response_model=schemas.ExpenseResponse, tags=["Expenses"])
def update_expense(expense_id: int, updates: schemas.ExpenseUpdate, db: Session = Depends(get_db)):
    """
    Update one or more fields of an existing expense.
    Only send the fields you want to change.
    """
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail=f"Expense with id {expense_id} not found")

    # Only update fields that were actually sent in the request
    update_data = updates.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(expense, field, value)

    db.commit()
    db.refresh(expense)
    return expense


# ─────────────────────────────────────────────
#  DELETE
# ─────────────────────────────────────────────

@app.delete("/expenses/{expense_id}", tags=["Expenses"])
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    """Delete an expense by its ID."""
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail=f"Expense with id {expense_id} not found")

    db.delete(expense)
    db.commit()
    return {"message": f"Expense {expense_id} deleted successfully"}


# ─────────────────────────────────────────────
#  SUMMARY / ANALYTICS
# ─────────────────────────────────────────────

@app.get("/expenses/summary/stats", response_model=schemas.SummaryResponse, tags=["Analytics"])
def get_summary(db: Session = Depends(get_db)):
    """
    Get a financial summary of all expenses:
    - Total count and amount
    - Average and highest expense
    - Breakdown of spending by category
    """
    expenses = db.query(models.Expense).all()

    if not expenses:
        return {
            "total_expenses": 0,
            "total_amount": 0.0,
            "average_amount": 0.0,
            "highest_expense": 0.0,
            "by_category": {}
        }

    amounts = [e.amount for e in expenses]

    # Build per-category totals
    by_category = {}
    for expense in expenses:
        cat = expense.category.value
        by_category[cat] = round(by_category.get(cat, 0) + expense.amount, 2)

    return {
        "total_expenses":  len(expenses),
        "total_amount":    round(sum(amounts), 2),
        "average_amount":  round(sum(amounts) / len(amounts), 2),
        "highest_expense": round(max(amounts), 2),
        "by_category":     by_category
    }
