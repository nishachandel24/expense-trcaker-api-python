from fastapi.responses import StreamingResponse
import csv
import io

from datetime import date
from typing import Literal

from fastapi import FastAPI, Query

from app.models import Expense, ExpenseCreate
from app.services import (
    create_expense,
    get_all_expenses,
    get_expense_by_id,
    update_expense,
    delete_expense,
)
from app.analytics import (
    monthly_summary,
    category_summary,
    overall_statistics,
)


app = FastAPI(
    title="Expense Tracker API",
    description="A REST API to manage and analyze daily expenses",
    version="1.0.0",
)


# Home route
@app.get("/")
def home():
    return {"message": "Expense Tracker API is running"}


# Create an expense
@app.post("/expenses", response_model=Expense, status_code=201)
def add_expense(data: ExpenseCreate):
    return create_expense(data)


# Get all expenses with search, sorting, and pagination
@app.get("/expenses", response_model=list[Expense])
def list_expenses(
    category: str | None = None,
    expense_date: date | None = Query(default=None, alias="date"),
    sort_by: Literal["date", "amount", "title"] = "date",
    order: Literal["asc", "desc"] = "asc",
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
):
    expenses = get_all_expenses()

    # Filter by category
    if category:
        expenses = [
            expense
            for expense in expenses
            if expense.category.lower() == category.lower()
        ]

    # Filter by date
    if expense_date:
        expenses = [
            expense
            for expense in expenses
            if expense.date == expense_date
        ]

    # Sort expenses
    if sort_by == "title":
        expenses.sort(
            key=lambda expense: expense.title.lower(),
            reverse=(order == "desc"),
        )
    else:
        expenses.sort(
            key=lambda expense: getattr(expense, sort_by),
            reverse=(order == "desc"),
        )

    # Apply pagination
    return expenses[skip:skip + limit]


# Get a single expense
@app.get("/expenses/{expense_id}", response_model=Expense)
def get_expense(expense_id: int):
    return get_expense_by_id(expense_id)


# Update an expense
@app.put("/expenses/{expense_id}", response_model=Expense)
def edit_expense(expense_id: int, data: ExpenseCreate):
    return update_expense(expense_id, data)


# Delete an expense
@app.delete("/expenses/{expense_id}")
def remove_expense(expense_id: int):
    return delete_expense(expense_id)


# Monthly spending report
@app.get("/reports/monthly")
def get_monthly_report():
    return monthly_summary()


# Category-wise spending report
@app.get("/reports/category")
def get_category_report():
    return category_summary()


# Overall spending statistics
@app.get("/reports/statistics")
def get_statistics():
    return overall_statistics()


@app.get("/reports/export")
def export_expenses():
    expenses = get_all_expenses()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "id", "title", "amount",
        "category", "date", "notes"
    ])

    for expense in expenses:
        writer.writerow([
            expense.id,
            expense.title,
            expense.amount,
            expense.category,
            expense.date,
            expense.notes,
        ])

    output.seek(0)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition":
                "attachment; filename=expenses.csv"
        },
    )