from fastapi import APIRouter, HTTPException
from app.models import ReviewCreate, ReviewResponse
from app.database import db
from app.utils.logger import logger
import psycopg2

router = APIRouter(prefix="/api", tags=["reviews"])


@router.get("/movies/{movie_id}/reviews", response_model=dict)
def get_movie_reviews(movie_id: int):
    """Get all reviews for a movie"""
    try:
        logger.info(f"Fetching reviews for movie: id={movie_id}")
        
        query = """
            SELECT id, movie_id, reviewer_name, rating, comment, created_at
            FROM reviews
            WHERE movie_id = %s
            ORDER BY created_at DESC
        """
        reviews = db.execute_query(query, (movie_id,))
        
        logger.info(f"Retrieved {len(reviews)} reviews")
        return {"reviews": reviews, "count": len(reviews)}
        
    except psycopg2.Error as e:
        logger.error(f"Database error in get_movie_reviews: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error in get_movie_reviews: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/reviews", response_model=dict, status_code=201)
def create_review(review: ReviewCreate):
    """Create a new review for a movie"""
    try:
        logger.info(f"Creating review for movie: id={review.movie_id}")
        
        # Check if movie exists
        movie_check = db.execute_query(
            "SELECT id FROM movies WHERE id = %s",
            (review.movie_id,),
            fetch_one=True
        )
        if not movie_check:
            logger.warning(f"Movie not found for review: id={review.movie_id}")
            raise HTTPException(status_code=404, detail="Movie not found")
        
        query = """
            INSERT INTO reviews (movie_id, reviewer_name, rating, comment)
            VALUES (%s, %s, %s, %s)
            RETURNING id, movie_id, reviewer_name, rating, comment, created_at
        """
        new_review = db.execute_insert(query, (
            review.movie_id,
            review.reviewer_name,
            review.rating,
            review.comment
        ))
        
        logger.info(f"Review created successfully: id={new_review['id']}")
        return new_review
        
    except HTTPException:
        raise
    except psycopg2.Error as e:
        logger.error(f"Database error in create_review: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error in create_review: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
