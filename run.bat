@echo off
echo Starting Movies API Backend...
echo.

cd /d "%~dp0"

if not exist "venv\" (
    echo Virtual environment not found!
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

if not exist ".env" (
    echo .env file not found!
    echo Please copy .env.example to .env and configure it
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
echo.
echo Starting server on http://localhost:8000
echo API docs at http://localhost:8000/docs
echo.
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
