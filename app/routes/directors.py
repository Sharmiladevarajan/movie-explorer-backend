from fastapi import APIRouter, HTTPException
from app.models import DirectorResponse
from app.database import db
from app.utils.logger import logger
import psycopg2

router = APIRouter(prefix="/api/directors", tags=["directors"])


@router.get("", response_model=dict)
def get_directors():
    """Get all directors"""
    try:
        logger.info("Fetching all directors")
        
        query = """
            SELECT id, name, bio, birth_year, created_at
            FROM directors
            ORDER BY name
        """
        directors = db.execute_query(query)
        
        logger.info(f"Retrieved {len(directors)} directors")
        return {"directors": directors, "count": len(directors)}
        
    except psycopg2.Error as e:
        logger.error(f"Database error in get_directors: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error in get_directors: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
