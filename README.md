# Movies API Backend

Production-ready FastAPI backend with proper architecture, connection pooling, logging, and error handling.

## Architecture

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app and startup
│   ├── config.py            # Configuration settings
│   ├── database.py          # Connection pool & DB operations
│   ├── models.py            # Pydantic models
│   ├── routes/              # API routes
│   │   ├── movies.py
│   │   ├── reviews.py
│   │   ├── directors.py
│   │   └── genres.py
│   └── utils/
│       └── logger.py        # Logging configuration
├── requirements.txt
└── .env
```

## Features

✅ **Connection Pooling** - ThreadedConnectionPool for efficient DB connections  
✅ **Proper Logging** - Structured logging with timestamps  
✅ **Error Handling** - Try-catch blocks with proper error responses  
✅ **SQL Injection Protection** - Parameterized queries throughout  
✅ **Input Validation** - Pydantic models with Field validators  
✅ **Modular Structure** - Organized routes and database layer  
✅ **No Code Duplication** - Common DB operations in database.py  

## Setup

1. **Create virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment:**
```bash
copy .env.example .env
# Edit .env with your database credentials
```

4. **Run the server:**
```bash
# From backend directory
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Visit http://localhost:8000/docs for interactive API documentation.

## Endpoints

### Movies
- `GET /api/movies` - Get all movies
- `GET /api/movies/{id}` - Get movie by ID
- `POST /api/movies` - Create movie
- `PUT /api/movies/{id}` - Update movie
- `DELETE /api/movies/{id}` - Delete movie
- `GET /api/movies/search/{term}` - Search movies

### Reviews
- `GET /api/movies/{id}/reviews` - Get movie reviews
- `POST /api/reviews` - Create review

### Directors & Genres
- `GET /api/directors` - Get all directors
- `GET /api/genres` - Get all genres

## Database Connection Pool

- Min connections: 2 (configurable via `DB_MIN_CONN`)
- Max connections: 10 (configurable via `DB_MAX_CONN`)
- Automatic connection management
- Connection reuse for performance

## Logging

Logs include:
- Request information
- Database operations
- Errors with stack traces
- Query execution details

Log level configurable via `LOG_LEVEL` environment variable (DEBUG, INFO, WARNING, ERROR).

## Error Handling

All endpoints have:
- Try-catch blocks
- Specific error logging
- Proper HTTP status codes
- User-friendly error messages
- Database error handling
