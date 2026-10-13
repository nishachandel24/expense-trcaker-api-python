
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Expense Tracker API is running"


def test_list_expenses():
    response = client.get("/expenses")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_monthly_report():
    response = client.get("/reports/monthly")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_category_report():
    response = client.get("/reports/category")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_statistics_report():
    response = client.get("/reports/statistics")
    assert response.status_code == 200
    assert "total" in response.json()
    assert "average" in response.json()
    assert "highest" in response.json()
    assert "count" in response.json()


def test_csv_export():
    response = client.get("/reports/export")
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert "attachment" in response.headers["content-disposition"]
