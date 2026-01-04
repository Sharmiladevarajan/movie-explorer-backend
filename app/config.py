import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_NAME: str = os.getenv("DB_NAME", "movies_db")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "postgres")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    
    # Connection Pool
    DB_MIN_CONN: int = int(os.getenv("DB_MIN_CONN", "2"))
    DB_MAX_CONN: int = int(os.getenv("DB_MAX_CONN", "10"))
    
    # API
    API_TITLE: str = "Movies API"
    API_VERSION: str = "1.0.0"
    CORS_ORIGINS: list = ["http://localhost:3000","https://movie-explorer-frontend-ten.vercel.app","https://movie-explorer-frontend-0oks.onrender.com"]
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
