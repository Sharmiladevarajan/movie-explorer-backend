from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.models import ActorCreate, ActorUpdate, ActorResponse, ErrorResponse
from app.database import db
from app.utils.logger import logger
import psycopg2

router = APIRouter(prefix="/api/actors", tags=["actors"])


@router.get("", response_model=dict)
def get_actors(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    genre: Optional[str] = None
):
    """
    Get all actors with optional filters
    
    Query Parameters:
    - limit: Maximum number of actors to return
    - offset: Number of actors to skip
    - genre: Filter actors by genre they've acted in
    """
    try:
        logger.info(f"Fetching actors: limit={limit}, offset={offset}, genre={genre}")
        
        if genre:
            # Filter actors by genre
            query = """
                SELECT DISTINCT a.id, a.name, a.bio, a.birth_year, a.image_url, a.created_at
                FROM actors a
                JOIN movie_actors ma ON a.id = ma.actor_id
                JOIN movies m ON ma.movie_id = m.id
                JOIN movie_genres mg ON m.id = mg.movie_id
                JOIN genres g ON mg.genre_id = g.id
                WHERE g.name ILIKE %s
                ORDER BY a.name
                LIMIT %s OFFSET %s
            """
            actors = db.execute_query(query, (genre, limit, offset))
        else:
            query = """
                SELECT id, name, bio, birth_year, image_url, created_at
                FROM actors
                ORDER BY name
                LIMIT %s OFFSET %s
            """
            actors = db.execute_query(query, (limit, offset))
        
        logger.info(f"Retrieved {len(actors)} actors")
        return {"actors": actors, "count": len(actors)}
        
    except psycopg2.Error as e:
        logger.error(f"Database error in get_actors: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error in get_actors: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{actor_id}", response_model=dict)
def get_actor(actor_id: int):
    """
    Get a single actor by ID with their filmography
    
    Returns actor details along with all movies they've appeared in
    """
    try:
        logger.info(f"Fetching actor with id={actor_id}")
        
        # Get actor details
        actor_query = """
            SELECT id, name, bio, birth_year, image_url, created_at
            FROM actors
            WHERE id = %s
        """
        actor = db.execute_query(actor_query, (actor_id,), fetch_one=True)
        
        if not actor:
            logger.warning(f"Actor not found: id={actor_id}")
            raise HTTPException(status_code=404, detail="Actor not found")
        
        # Get actor's movies
        movies_query = """
            SELECT m.id, m.title, d.name as director, m.release_year, 
                   g.name as genre, m.rating, m.description, m.language, 
                   m.image_url, ma.role
            FROM movies m
            JOIN directors d ON m.director_id = d.id
            JOIN genres g ON m.genre_id = g.id
            JOIN movie_actors ma ON m.id = ma.movie_id
            WHERE ma.actor_id = %s
            ORDER BY m.release_year DESC
        """
        movies = db.execute_query(movies_query, (actor_id,))
        
        logger.info(f"Retrieved actor: {actor['name']} with {len(movies)} movies")
        return {
            **actor,
            "movies": movies,
            "movie_count": len(movies)
        }
        
    except HTTPException:
        raise
    except psycopg2.Error as e:
        logger.error(f"Database error in get_actor: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error in get_actor: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("", response_model=dict, status_code=201)
def create_actor(actor: ActorCreate):
    """Create a new actor"""
    try:
        logger.info(f"Creating actor: {actor.name}")
        
        query = """
            INSERT INTO actors (name, bio, birth_year)
            VALUES (%s, %s, %s)
            RETURNING id
        """
        result = db.execute_insert(query, (
            actor.name,
            actor.bio,
            actor.birth_year
        ))
        
        actor_id = result['id']
        logger.info(f"Actor created successfully: id={actor_id}")
        
        return get_actor(actor_id)
        
    except psycopg2.IntegrityError as e:
        logger.error(f"Integrity error in create_actor: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid data provided")
    except psycopg2.Error as e:
        logger.error(f"Database error in create_actor: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error in create_actor: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{actor_id}", response_model=dict)
def update_actor(actor_id: int, actor: ActorUpdate):
    """Update an existing actor"""
    try:
        logger.info(f"Updating actor: id={actor_id}")
        
        # Check if actor exists
        existing = db.execute_query(
            "SELECT id FROM actors WHERE id = %s",
            (actor_id,),
            fetch_one=True
        )
        if not existing:
            logger.warning(f"Actor not found for update: id={actor_id}")
            raise HTTPException(status_code=404, detail="Actor not found")
        
        # Build dynamic update
        update_fields = []
        values = []
        
        if actor.name is not None:
            update_fields.append("name = %s")
            values.append(actor.name)
        
        if actor.bio is not None:
            update_fields.append("bio = %s")
            values.append(actor.bio)
        
        if actor.birth_year is not None:
            update_fields.append("birth_year = %s")
            values.append(actor.birth_year)
        
        if not update_fields:
            logger.info(f"No fields to update for actor: id={actor_id}")
            return get_actor(actor_id)
        
        values.append(actor_id)
        query = f"""
            UPDATE actors
            SET {', '.join(update_fields)}
            WHERE id = %s
            RETURNING id
        """
        db.execute_update(query, tuple(values))
        
        logger.info(f"Actor updated successfully: id={actor_id}")
        return get_actor(actor_id)
        
    except HTTPException:
        raise
    except psycopg2.Error as e:
        logger.error(f"Database error in update_actor: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error in update_actor: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{actor_id}", response_model=dict)
def delete_actor(actor_id: int):
    """Delete an actor"""
    try:
        logger.info(f"Deleting actor: id={actor_id}")
        
        query = "DELETE FROM actors WHERE id = %s"
        deleted = db.execute_delete(query, (actor_id,))
        
        if not deleted:
            logger.warning(f"Actor not found for deletion: id={actor_id}")
            raise HTTPException(status_code=404, detail="Actor not found")
        
        logger.info(f"Actor deleted successfully: id={actor_id}")
        return {"message": "Actor deleted successfully"}
        
    except HTTPException:
        raise
    except psycopg2.Error as e:
        logger.error(f"Database error in delete_actor: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error in delete_actor: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/{actor_id}/movies/{movie_id}", response_model=dict, status_code=201)
def add_actor_to_movie(actor_id: int, movie_id: int, role: Optional[str] = None):
    """
    Add an actor to a movie
    
    Creates a relationship between an actor and a movie with an optional role/character name
    """
    try:
        logger.info(f"Adding actor {actor_id} to movie {movie_id}")
        
        # Check if actor and movie exist
        actor = db.execute_query("SELECT id FROM actors WHERE id = %s", (actor_id,), fetch_one=True)
        movie = db.execute_query("SELECT id FROM movies WHERE id = %s", (movie_id,), fetch_one=True)
        
        if not actor:
            raise HTTPException(status_code=404, detail="Actor not found")
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        
        query = """
            INSERT INTO movie_actors (movie_id, actor_id, role)
            VALUES (%s, %s, %s)
            ON CONFLICT (movie_id, actor_id) DO UPDATE SET role = EXCLUDED.role
            RETURNING id
        """
        result = db.execute_insert(query, (movie_id, actor_id, role))
        
        logger.info(f"Actor added to movie successfully")
        return {"message": "Actor added to movie successfully", "id": result['id']}
        
    except HTTPException:
        raise
    except psycopg2.Error as e:
        logger.error(f"Database error in add_actor_to_movie: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error in add_actor_to_movie: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
