from fastapi import APIRouter, HTTPException
from app.models import ReviewCreate, ReviewUpdate, ReviewResponse
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


@router.put("/reviews/{review_id}", response_model=dict)
def update_review(review_id: int, review_update: ReviewUpdate):
    """Update a review"""
    try:
        logger.info(f"Updating review: id={review_id}")
        
        # Check if review exists
        review_check = db.execute_query(
            "SELECT id FROM reviews WHERE id = %s",
            (review_id,),
            fetch_one=True
        )
        if not review_check:
            logger.warning(f"Review not found: id={review_id}")
            raise HTTPException(status_code=404, detail="Review not found")
        
        # Build update query
        update_fields = []
        values = []
        
        if review_update.comment is not None:
            update_fields.append("comment = %s")
            values.append(review_update.comment)
        
        if review_update.rating is not None:
            update_fields.append("rating = %s")
            values.append(review_update.rating)
        
        if not update_fields:
            logger.info(f"No fields to update for review: id={review_id}")
        else:
            query = f"""
                UPDATE reviews
                SET {', '.join(update_fields)}
                WHERE id = %s
            """
            values.append(review_id)
            db.execute_update(query, tuple(values))
        
        # Return updated review
        review_query = """
            SELECT id, movie_id, reviewer_name, rating, comment, created_at
            FROM reviews
            WHERE id = %s
        """
        updated_review = db.execute_query(review_query, (review_id,), fetch_one=True)
        
        logger.info(f"Review updated successfully: id={review_id}")
        return updated_review
        
    except HTTPException:
        raise
    except psycopg2.Error as e:
        logger.error(f"Database error in update_review: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error in update_review: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/reviews/{review_id}", response_model=dict)
def delete_review(review_id: int):
    """Delete a review"""
    try:
        logger.info(f"Deleting review: id={review_id}")
        
        # Check if review exists
        review_check = db.execute_query(
            "SELECT id FROM reviews WHERE id = %s",
            (review_id,),
            fetch_one=True
        )
        if not review_check:
            logger.warning(f"Review not found: id={review_id}")
            raise HTTPException(status_code=404, detail="Review not found")
        
        query = "DELETE FROM reviews WHERE id = %s"
        db.execute_delete(query, (review_id,))
        
        logger.info(f"Review deleted successfully: id={review_id}")
        return {"message": "Review deleted successfully"}
        
    except HTTPException:
        raise
    except psycopg2.Error as e:
        logger.error(f"Database error in delete_review: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error in delete_review: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
