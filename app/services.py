
import csv
from pathlib import Path

from fastapi import HTTPException

from app.models import Expense, ExpenseCreate


CSV_FILE = Path(__file__).resolve().parent.parent / "data" / "expenses.csv"

FIELDS = ["id", "title", "amount", "category", "date", "notes"]


def read_expenses():
    if not CSV_FILE.exists():
        return []

    with CSV_FILE.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [Expense(**row) for row in reader]


def save_expenses(expenses):
    CSV_FILE.parent.mkdir(parents=True, exist_ok=True)

    with CSV_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()

        for expense in expenses:
            writer.writerow(expense.model_dump(mode="json"))


def get_all_expenses():
    return read_expenses()


def get_expense_by_id(expense_id: int):
    for expense in read_expenses():
        if expense.id == expense_id:
            return expense

    raise HTTPException(status_code=404, detail="Expense not found")


def create_expense(data: ExpenseCreate):
    expenses = read_expenses()

    new_id = max((expense.id for expense in expenses), default=0) + 1

    expense = Expense(id=new_id, **data.model_dump())

    expenses.append(expense)
    save_expenses(expenses)

    return expense


def update_expense(expense_id: int, data: ExpenseCreate):
    expenses = read_expenses()

    for index, expense in enumerate(expenses):
        if expense.id == expense_id:
            updated = Expense(id=expense_id, **data.model_dump())
            expenses[index] = updated
            save_expenses(expenses)
            return updated

    raise HTTPException(status_code=404, detail="Expense not found")


def delete_expense(expense_id: int):
    expenses = read_expenses()

    for index, expense in enumerate(expenses):
        if expense.id == expense_id:
            deleted = expenses.pop(index)
            save_expenses(expenses)
            return {"message": "Expense deleted successfully"}

    raise HTTPException(status_code=404, detail="Expense not found")
