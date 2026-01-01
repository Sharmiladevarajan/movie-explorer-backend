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


@router.get("/{director_id}", response_model=dict)
def get_director(director_id: int):
    """
    Get a single director by ID with their filmography
    
    Returns director details along with all movies they've directed
    """
    try:
        logger.info(f"Fetching director with id={director_id}")
        
        # Get director details
        director_query = """
            SELECT id, name, bio, birth_year, created_at
            FROM directors
            WHERE id = %s
        """
        director = db.execute_query(director_query, (director_id,), fetch_one=True)
        
        if not director:
            logger.warning(f"Director not found: id={director_id}")
            raise HTTPException(status_code=404, detail="Director not found")
        
        # Get director's movies
        movies_query = """
            SELECT m.id, m.title, g.name as genre, m.release_year, 
                   m.rating, m.description
            FROM movies m
            JOIN genres g ON m.genre_id = g.id
            WHERE m.director_id = %s
            ORDER BY m.release_year DESC
        """
        movies = db.execute_query(movies_query, (director_id,))
        
        logger.info(f"Retrieved director: {director['name']} with {len(movies)} movies")
        return {
            **director,
            "movies": movies,
            "movie_count": len(movies)
        }
        
    except HTTPException:
        raise
    except psycopg2.Error as e:
        logger.error(f"Database error in get_director: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error in get_director: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
