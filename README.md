
# Movie Explorer Backend

This is the backend for the Movie Explorer app, built with FastAPI and PostgreSQL. It provides a RESTful API for managing movies, actors, directors, genres, and reviews.

## Features
- Full CRUD for movies, actors, directors, genres, and reviews
- Admin endpoints for data management
- Database migrations and demo/demo data scripts
- End-to-end tested with pytest
- Docker and docker-compose support
- Interactive API docs (Swagger/OpenAPI)

## Quick Setup

### Prerequisites
- Python 3.10+
- PostgreSQL

### 1. Clone & Install
```bash
git clone <repo-url>
cd movie-explorer-backend
pip install -r requirements.txt
```

### 2. Database Setup
1. Create a PostgreSQL database and user.
2. Update the DB connection in `app/config.py` or set the `DATABASE_URL` env variable.
3. Run schema and demo data:
   ```bash
   psql -U <user> -d <dbname> -f schema.sql
   psql -U <user> -d <dbname> -f demo_data.sql
   ```

### 3. Run the API Server
```bash
uvicorn app.main:app --reload
```

### 4. API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 5. Run Tests
```bash
pytest tests/test_all_routes.py
```

### 6. Docker
```bash
docker build -t movie-explorer-backend .
docker run -p 8000:8000 movie-explorer-backend
# or
docker-compose up --build
```

## Project Structure
- `app/` - FastAPI app code
- `app/routes/` - API route modules
- `app/models.py` - SQLAlchemy models
- `app/database.py` - Database connection
- `tests/` - API tests
- `*.sql` - DB schema and migration scripts

## End-to-End Testing
All API endpoints are tested in `tests/test_all_routes.py`.

## License
MIT
