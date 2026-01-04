"""
Shared pytest fixtures for all tests
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.main import app


@pytest.fixture
def client():
    """Create a test client for FastAPI app"""
    return TestClient(app)


@pytest.fixture
def mock_db():
    """Mock database connection - patches all route imports"""
    with patch('app.routes.actors.db') as mock_actors, \
         patch('app.routes.movies.db') as mock_movies, \
         patch('app.routes.directors.db') as mock_directors, \
         patch('app.routes.genres.db') as mock_genres, \
         patch('app.routes.reviews.db') as mock_reviews:
        
        # Make all mocks return the same instance
        mock = Mock()
        mock_actors.execute_query = mock.execute_query
        mock_actors.execute_insert = mock.execute_insert
        mock_actors.execute_update = mock.execute_update
        mock_actors.execute_delete = mock.execute_delete
        
        mock_movies.execute_query = mock.execute_query
        mock_movies.execute_insert = mock.execute_insert
        mock_movies.execute_update = mock.execute_update
        mock_movies.execute_delete = mock.execute_delete
        
        mock_directors.execute_query = mock.execute_query
        mock_genres.execute_query = mock.execute_query
        
        mock_reviews.execute_query = mock.execute_query
        mock_reviews.execute_insert = mock.execute_insert
        mock_reviews.execute_update = mock.execute_update
        mock_reviews.execute_delete = mock.execute_delete
        
        yield mock


@pytest.fixture
def sample_actor():
    """Sample actor data for testing"""
    return {
        'id': 1,
        'name': 'Tom Hanks',
        'bio': 'American actor and filmmaker',
        'birth_year': 1956,
        'image_url': 'https://example.com/tom.jpg',
        'created_at': '2024-01-01T00:00:00'
    }


@pytest.fixture
def sample_movie():
    """Sample movie data for testing"""
    return {
        'id': 1,
        'title': 'Forrest Gump',
        'description': 'Life is like a box of chocolates',
        'release_year': 1994,
        'director_id': 1,
        'director': 'Robert Zemeckis',
        'genre_id': 1,
        'genre': 'Drama',
        'rating': 8.8,
        'language': 'English',
        'image_url': 'https://example.com/forrest.jpg',
        'created_at': '2024-01-01T00:00:00'
    }


@pytest.fixture
def sample_director():
    """Sample director data for testing"""
    return {
        'id': 1,
        'name': 'Steven Spielberg',
        'bio': 'American filmmaker',
        'birth_year': 1946,
        'image_url': 'https://example.com/spielberg.jpg',
        'created_at': '2024-01-01T00:00:00'
    }


@pytest.fixture
def sample_genre():
    """Sample genre data for testing"""
    return {
        'id': 1,
        'name': 'Drama',
        'description': 'Dramatic films',
        'created_at': '2024-01-01T00:00:00'
    }


@pytest.fixture
def sample_review():
    """Sample review data for testing"""
    return {
        'id': 1,
        'movie_id': 1,
        'reviewer_name': 'John Doe',
        'rating': 5,
        'comment': 'Excellent movie!',
        'created_at': '2024-01-01T00:00:00'
    }
