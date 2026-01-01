from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.config import settings
from app.database import db_pool
from app.utils.logger import logger
from app.routes import movies, reviews, directors, genres


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting Movies API...")
    try:
        db_pool.initialize()
        logger.info("Database connection pool initialized")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Movies API...")
    db_pool.close_all()
    logger.info("Application shutdown complete")


# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle uncaught exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error_type": type(exc).__name__}
    )


# Include routers
app.include_router(movies.router)
app.include_router(reviews.router)
app.include_router(directors.router)
app.include_router(genres.router)


# Health check
@app.get("/")
def health_check():
    """API health check endpoint"""
    logger.info("Health check requested")
    return {
        "status": "healthy",
        "message": "Movies API is running",
        "version": settings.API_VERSION
    }


@app.get("/health")
def health():
    """Detailed health check"""
    try:
        # Test database connection
        from app.database import db
        db.execute_query("SELECT 1", fetch_one=True)
        db_status = "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        db_status = "disconnected"
    
    return {
        "status": "healthy" if db_status == "connected" else "unhealthy",
        "database": db_status,
        "version": settings.API_VERSION
    }
