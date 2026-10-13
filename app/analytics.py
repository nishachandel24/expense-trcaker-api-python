
import pandas as pd
import numpy as np

from app.services import get_all_expenses


def get_expenses_dataframe():
    expenses = get_all_expenses()

    columns = ["id", "title", "amount", "category", "date", "notes"]

    records = [
        expense.model_dump(mode="json")
        for expense in expenses
    ]

    df = pd.DataFrame(records, columns=columns)

    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
        df["amount"] = pd.to_numeric(df["amount"])

    return df


def monthly_summary():
    df = get_expenses_dataframe()

    if df.empty:
        return {}

    df["month"] = df["date"].dt.strftime("%Y-%m")

    result = df.groupby("month")["amount"].sum()

    return result.to_dict()


def category_summary():
    df = get_expenses_dataframe()

    if df.empty:
        return {}

    result = df.groupby("category")["amount"].sum()

    return result.to_dict()


def overall_statistics():
    df = get_expenses_dataframe()

    if df.empty:
        return {
            "total": 0,
            "average": 0,
            "highest": 0,
            "count": 0,
        }

    amounts = df["amount"].to_numpy()

    return {
        "total": round(float(np.sum(amounts)), 2),
        "average": round(float(np.mean(amounts)), 2),
        "highest": round(float(np.max(amounts)), 2),
        "count": int(len(amounts)),
    }
