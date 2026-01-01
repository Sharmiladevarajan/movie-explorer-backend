# Backend Setup Guide

## Prerequisites

1. **Python 3.8+** installed
2. **PostgreSQL** installed and running
3. Database `movies_db` created with the schema

## Step-by-Step Setup

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy the example environment file:
```bash
copy .env.example .env
```

Edit `.env` and update with your PostgreSQL credentials:
```env
DB_HOST=localhost
DB_NAME=movies_db
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_PORT=5432

DB_MIN_CONN=2
DB_MAX_CONN=10

LOG_LEVEL=INFO
```

### 4. Create Database (if not done)

Connect to PostgreSQL and run:
```sql
-- From the database folder
\i ../database/schema.sql
\i ../database/sample_data.sql
```

### 5. Start the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or use the run script:
```bash
run.bat
```

## Verify Setup

1. **Health Check:**
   Visit http://localhost:8000/ - Should return `{"status": "healthy"}`

2. **Database Check:**
   Visit http://localhost:8000/health - Should show database as "connected"

3. **API Docs:**
   Visit http://localhost:8000/docs - Interactive API documentation

## Troubleshooting

### Connection Pool Error
```
Failed to create connection pool: password authentication failed
```
**Solution:** Check your PostgreSQL credentials in `.env` file

### Database Does Not Exist
```
database "movies_db" does not exist
```
**Solution:** Run the schema creation script first (see Step 4)

### Import Error
```
ModuleNotFoundError: No module named 'app'
```
**Solution:** Make sure you're running from the `backend` directory and using:
```bash
uvicorn app.main:app --reload
```

### Port Already in Use
```
ERROR: [Errno 10048] Only one usage of each socket address
```
**Solution:** Stop other processes using port 8000 or use a different port:
```bash
uvicorn app.main:app --reload --port 8001
```

## Logs

The application logs all operations with timestamps:
- Request information
- Database queries
- Errors with full stack traces
- Connection pool status

Set `LOG_LEVEL=DEBUG` in `.env` for more detailed logs.

## Production Deployment

For production, use a proper WSGI server:

```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

Update your `.env` for production:
- Set `LOG_LEVEL=WARNING`
- Increase `DB_MAX_CONN` based on your load
- Use environment variables instead of `.env` file
