
from datetime import date

from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    amount: float = Field(gt=0)
    category: str = Field(min_length=1, max_length=50)
    date: date
    notes: str = Field(default="", max_length=500)


class Expense(ExpenseCreate):
    id: int
