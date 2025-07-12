# Ruh Backend

A FastAPI-based backend service for the Ruh wellness platform.

## Prerequisites

- Python 3.11+
- PostgreSQL
- Virtual environment (recommended)

## Setup

1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure Database:
   - The application uses PostgreSQL
   - Update database configuration in `app/core/config.py` if needed
   - Default configuration uses:
     - Host: postgresql-199561-0.cloudclusters.net
     - Port: 16348
     - Database: ruh
     - Username: Burhan

## Database Migrations

To manage database migrations, we use Alembic. Here are the common commands:

1. Generate a new migration:
```bash
PYTHONPATH=$PYTHONPATH:. alembic revision --autogenerate -m "Migration description"
```

2. Apply migrations:
```bash
PYTHONPATH=$PYTHONPATH:. alembic upgrade head
```

3. Rollback last migration:
```bash
PYTHONPATH=$PYTHONPATH:. alembic downgrade -1
```

## Running the Application

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

API Documentation will be available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
backend/
├── alembic/              # Database migration files
├── app/
│   ├── api/             # API endpoints
│   ├── core/            # Core configuration
│   ├── db/              # Database models and session
│   ├── schemas/         # Pydantic models
│   └── services/        # Business logic
├── requirements.txt     # Project dependencies
└── alembic.ini         # Alembic configuration
``` 