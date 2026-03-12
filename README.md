# 💸 Expense Tracker API

A RESTful backend API built with **FastAPI** and **SQLite**, designed to track personal expenses with category filtering and spending analytics.

---

## Tech Stack

| Layer        | Technology              |
|--------------|-------------------------|
| Framework    | FastAPI (Python)        |
| Database     | SQLite via SQLAlchemy   |
| Validation   | Pydantic                |
| Server       | Uvicorn (ASGI)          |

---

## Setup & Run

```bash
# 1. Install dependencies
pip install fastapi uvicorn sqlalchemy pydantic

# 2. Start the server
uvicorn main:app --reload

# 3. Open interactive docs
http://127.0.0.1:8000/docs
```

---

## API Endpoints

| Method   | Endpoint                      | Description                          |
|----------|-------------------------------|--------------------------------------|
| GET      | `/`                           | Health check                         |
| POST     | `/expenses`                   | Add a new expense                    |
| GET      | `/expenses`                   | Get all expenses (with filters)      |
| GET      | `/expenses/{id}`              | Get a single expense                 |
| PATCH    | `/expenses/{id}`              | Update an expense                    |
| DELETE   | `/expenses/{id}`              | Delete an expense                    |
| GET      | `/expenses/summary/stats`     | Spending summary & category breakdown|

---

## Example Usage

**Add an expense:**
```json
POST /expenses
{
  "title": "Lunch",
  "amount": 150.00,
  "category": "food",
  "note": "Ate out with friends"
}
```

**Filter by category:**
```
GET /expenses?category=food&max_amount=500
```

**Get spending summary:**
```json
GET /expenses/summary/stats

{
  "total_expenses": 5,
  "total_amount": 1240.50,
  "average_amount": 248.10,
  "highest_expense": 600.00,
  "by_category": {
    "food": 450.00,
    "transport": 200.00,
    "shopping": 590.50
  }
}
```

---

## Project Structure

```
expense-tracker/
├── main.py        # API routes and application logic
├── models.py      # Database table definitions (SQLAlchemy)
├── schemas.py     # Request/response validation (Pydantic)
├── database.py    # DB connection and session management
└── expenses.db    # SQLite database (auto-created on first run)
```


