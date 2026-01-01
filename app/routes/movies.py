from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.models import MovieCreate, MovieUpdate, MovieResponse, ErrorResponse
from app.database import db
from app.utils.logger import logger
import psycopg2

router = APIRouter(prefix="/api/movies", tags=["movies"])


@router.get("", response_model=dict)
def get_movies(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    genre: Optional[str] = None,
    director: Optional[str] = None,
    actor: Optional[str] = None,
    year: Optional[int] = None
):
    """
    Get all movies with optional filters
    
    Query Parameters:
    - limit: Maximum number of movies to return
    - offset: Number of movies to skip (pagination)
    - genre: Filter by genre name
    - director: Filter by director name
    - actor: Filter by actor name
    - year: Filter by release year
    """
    try:
        logger.info(f"Fetching movies: limit={limit}, offset={offset}, genre={genre}, director={director}, actor={actor}, year={year}")
        
        # Build dynamic query with filters
        base_query = """
            SELECT DISTINCT m.id, m.title, d.name as director, m.release_year, 
                   g.name as genre, m.rating, m.description, m.created_at
            FROM movies m
            JOIN directors d ON m.director_id = d.id
            JOIN genres g ON m.genre_id = g.id
        """
        
        conditions = []
        params = []
        
        # Add actor join if filtering by actor
        if actor:
            base_query += """
                JOIN movie_actors ma ON m.id = ma.movie_id
                JOIN actors a ON ma.actor_id = a.id
            """
            conditions.append("a.name ILIKE %s")
            params.append(actor)
        
        # Add filter conditions
        if genre:
            conditions.append("g.name ILIKE %s")
            params.append(genre)
        
        if director:
            conditions.append("d.name ILIKE %s")
            params.append(director)
        
        if year:
            conditions.append("m.release_year = %s")
            params.append(year)
        
        # Combine query
        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)
        
        base_query += " ORDER BY m.created_at DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        
        movies = db.execute_query(base_query, tuple(params))
        
        logger.info(f"Retrieved {len(movies)} movies")
        return {"movies": movies, "count": len(movies)}
        
    except psycopg2.Error as e:
        logger.error(f"Database error in get_movies: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error in get_movies: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{movie_id}", response_model=dict)
def get_movie(movie_id: int):
    """
    Get a single movie by ID with full details
    
    Returns movie details including cast (actors), director, genres, and reviews
    """
    try:
        logger.info(f"Fetching movie with id={movie_id}")
        
        query = """
            SELECT m.id, m.title, d.name as director, d.id as director_id, m.release_year, 
                   g.name as genre, m.rating, m.description, m.created_at
            FROM movies m
            JOIN directors d ON m.director_id = d.id
            JOIN genres g ON m.genre_id = g.id
            WHERE m.id = %s
        """
        movie = db.execute_query(query, (movie_id,), fetch_one=True)
        
        if not movie:
            logger.warning(f"Movie not found: id={movie_id}")
            raise HTTPException(status_code=404, detail="Movie not found")
        
        # Get actors/cast for this movie
        actors_query = """
            SELECT a.id, a.name, ma.role, a.birth_year
            FROM actors a
            JOIN movie_actors ma ON a.id = ma.actor_id
            WHERE ma.movie_id = %s
            ORDER BY a.name
        """
        actors = db.execute_query(actors_query, (movie_id,))
        
        # Get reviews for this movie
        reviews_query = """
            SELECT id, reviewer_name, rating, comment, created_at
            FROM reviews
            WHERE movie_id = %s
            ORDER BY created_at DESC
        """
        reviews = db.execute_query(reviews_query, (movie_id,))
        
        logger.info(f"Retrieved movie: {movie['title']} with {len(actors)} actors and {len(reviews)} reviews")
        return {
            **movie,
            "cast": actors,
            "reviews": reviews
        }
        
    except HTTPException:
        raise
    except psycopg2.Error as e:
        logger.error(f"Database error in get_movie: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error in get_movie: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("", response_model=dict, status_code=201)
def create_movie(movie: MovieCreate):
    """Create a new movie"""
    try:
        logger.info(f"Creating movie: {movie.title}")
        
        # Get or create director and genre
        director_id = db.get_or_create("directors", "name", movie.director_name)
        genre_id = db.get_or_create("genres", "name", movie.genre_name)
        
        query = """
            INSERT INTO movies (title, director_id, genre_id, release_year, rating, description)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        result = db.execute_insert(query, (
            movie.title,
            director_id,
            genre_id,
            movie.release_year,
            movie.rating,
            movie.description
        ))
        
        movie_id = result['id']
        logger.info(f"Movie created successfully: id={movie_id}")
        
        # Return the created movie
        return get_movie(movie_id)
        
    except psycopg2.IntegrityError as e:
        logger.error(f"Integrity error in create_movie: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid data provided")
    except psycopg2.Error as e:
        logger.error(f"Database error in create_movie: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error in create_movie: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{movie_id}", response_model=dict)
def update_movie(movie_id: int, movie: MovieUpdate):
    """Update an existing movie"""
    try:
        logger.info(f"Updating movie: id={movie_id}")
        
        # Check if movie exists
        existing = db.execute_query(
            "SELECT id FROM movies WHERE id = %s",
            (movie_id,),
            fetch_one=True
        )
        if not existing:
            logger.warning(f"Movie not found for update: id={movie_id}")
            raise HTTPException(status_code=404, detail="Movie not found")
        
        # Build dynamic update
        update_fields = []
        values = []
        
        if movie.title is not None:
            update_fields.append("title = %s")
            values.append(movie.title)
        
        if movie.director_name is not None:
            director_id = db.get_or_create("directors", "name", movie.director_name)
            update_fields.append("director_id = %s")
            values.append(director_id)
        
        if movie.genre_name is not None:
            genre_id = db.get_or_create("genres", "name", movie.genre_name)
            update_fields.append("genre_id = %s")
            values.append(genre_id)
        
        if movie.release_year is not None:
            update_fields.append("release_year = %s")
            values.append(movie.release_year)
        
        if movie.rating is not None:
            update_fields.append("rating = %s")
            values.append(movie.rating)
        
        if movie.description is not None:
            update_fields.append("description = %s")
            values.append(movie.description)
        
        if not update_fields:
            logger.info(f"No fields to update for movie: id={movie_id}")
            return get_movie(movie_id)
        
        values.append(movie_id)
        query = f"""
            UPDATE movies
            SET {', '.join(update_fields)}
            WHERE id = %s
            RETURNING id
        """
        db.execute_update(query, tuple(values))
        
        logger.info(f"Movie updated successfully: id={movie_id}")
        return get_movie(movie_id)
        
    except HTTPException:
        raise
    except psycopg2.Error as e:
        logger.error(f"Database error in update_movie: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error in update_movie: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{movie_id}", response_model=dict)
def delete_movie(movie_id: int):
    """Delete a movie"""
    try:
        logger.info(f"Deleting movie: id={movie_id}")
        
        query = "DELETE FROM movies WHERE id = %s"
        deleted = db.execute_delete(query, (movie_id,))
        
        if not deleted:
            logger.warning(f"Movie not found for deletion: id={movie_id}")
            raise HTTPException(status_code=404, detail="Movie not found")
        
        logger.info(f"Movie deleted successfully: id={movie_id}")
        return {"message": "Movie deleted successfully"}
        
    except HTTPException:
        raise
    except psycopg2.Error as e:
        logger.error(f"Database error in delete_movie: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error in delete_movie: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/search/{search_term}", response_model=dict)
def search_movies(search_term: str):
    """Search movies by title, director, or description"""
    try:
        logger.info(f"Searching movies: term='{search_term}'")
        
        # Sanitize search term
        search_term = search_term.strip()
        if not search_term:
            logger.warning("Empty search term provided")
            raise HTTPException(status_code=400, detail="Search term cannot be empty")
        
        query = """
            SELECT m.id, m.title, d.name as director, m.release_year, 
                   g.name as genre, m.rating, m.description, m.created_at
            FROM movies m
            JOIN directors d ON m.director_id = d.id
            JOIN genres g ON m.genre_id = g.id
            WHERE m.title ILIKE %s OR d.name ILIKE %s OR m.description ILIKE %s
            ORDER BY m.created_at DESC
        """
        search_pattern = f"%{search_term}%"
        movies = db.execute_query(query, (search_pattern, search_pattern, search_pattern))
        
        logger.info(f"Search returned {len(movies)} results")
        return {"movies": movies, "count": len(movies)}
        
    except HTTPException:
        raise
    except psycopg2.Error as e:
        logger.error(f"Database error in search_movies: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error in search_movies: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
