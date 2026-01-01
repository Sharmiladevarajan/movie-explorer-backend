from fastapi import APIRouter, HTTPException
from app.models import GenreResponse
from app.database import db
from app.utils.logger import logger
import psycopg2

router = APIRouter(prefix="/api/genres", tags=["genres"])


@router.get("", response_model=dict)
def get_genres():
    """Get all genres"""
    try:
        logger.info("Fetching all genres")
        
        query = """
            SELECT id, name, description, created_at
            FROM genres
            ORDER BY name
        """
        genres = db.execute_query(query)
        
        logger.info(f"Retrieved {len(genres)} genres")
        return {"genres": genres, "count": len(genres)}
        
    except psycopg2.Error as e:
        logger.error(f"Database error in get_genres: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error in get_genres: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
