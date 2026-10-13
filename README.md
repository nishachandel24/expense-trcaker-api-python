# Expense Tracker API

A RESTful backend application built with Python and FastAPI to manage, search, and analyze daily expenses. It uses CSV files for storage and Pandas and NumPy for expense analytics.

## Features

- Create, read, update, and delete expenses (CRUD)
- Request validation using Pydantic
- CSV-based expense storage
- Search expenses by category and date
- Sort expenses by title, date, or amount
- Pagination
- Monthly spending summaries
- Category-wise spending reports
- Overall statistics: total, average, highest expense, and count
- Downloadable CSV export
- Interactive API documentation using Swagger UI
- Automated tests using pytest

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Pydantic
- Pandas
- NumPy
- CSV
- pytest

## Project Structure

```text
expense_tracker_api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── services.py
│   ├── analytics.py
│   ├── utils.py
│   └── config.py
├── data/
│   └── expenses.csv
├── tests/
│   └── test_api.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

Clone the repository and navigate into the project folder.

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the API

```bash
uvicorn app.main:app --reload
```

API base URL: `http://127.0.0.1:8000`

Swagger documentation: `http://127.0.0.1:8000/docs`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API health check |
| POST | `/expenses` | Create an expense |
| GET | `/expenses` | List, search, sort, and paginate expenses |
| GET | `/expenses/{expense_id}` | Get an expense by ID |
| PUT | `/expenses/{expense_id}` | Update an expense |
| DELETE | `/expenses/{expense_id}` | Delete an expense |
| GET | `/reports/monthly` | Monthly spending summary |
| GET | `/reports/category` | Category-wise spending summary |
| GET | `/reports/statistics` | Overall expense statistics |
| GET | `/reports/export` | Download expenses as CSV |

## Example Expense

```json
{
  "title": "Lunch",
  "amount": 250,
  "category": "Food",
  "date": "2026-10-12",
  "notes": "College lunch"
}
```

## Search, Sorting, and Pagination

Example request:

```text
/expenses?category=Food&sort_by=amount&order=desc&skip=0&limit=10
```

Supported sorting fields: `title`, `date`, and `amount`.

## Run Automated Tests

From the project root, run:

```bash
PYTHONPATH=. pytest -v
```

The current test suite covers the home endpoint, expense listing, analytics reports, and CSV export.

## Storage

Expenses are stored in `data/expenses.csv`. This is a learning project; a database such as SQLite or PostgreSQL would be more suitable for concurrent writes and larger applications.

## Future Improvements

- Database integration
- JWT authentication
- More comprehensive CRUD and validation tests
- Docker support
- Cloud deployment
- CI/CD using GitHub Actions

## Learning Outcomes

This project demonstrates Python classes, type hints, data validation, CSV file handling, REST API development, CRUD operations, data analysis, and automated API testing.