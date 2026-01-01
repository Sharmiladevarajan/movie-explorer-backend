import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)


class TestMoviesAPI:
    """Test cases for Movies API endpoints"""
    
    def test_get_movies(self, client):
        """Test getting list of movies"""
        response = client.get("/api/movies")
        assert response.status_code == 200
        data = response.json()
        assert "movies" in data
        assert "count" in data
        assert isinstance(data["movies"], list)
    
    def test_get_movies_with_filters(self, client):
        """Test getting movies with filters"""
        response = client.get("/api/movies?limit=10&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert len(data["movies"]) <= 10
    
    def test_search_movies(self, client):
        """Test movie search"""
        response = client.get("/api/movies/search/test")
        assert response.status_code == 200
        data = response.json()
        assert "movies" in data
        assert "count" in data
    
    def test_search_movies_empty_term(self, client):
        """Test movie search with empty term"""
        response = client.get("/api/movies/search/ ")
        assert response.status_code == 400


class TestDirectorsAPI:
    """Test cases for Directors API endpoints"""
    
    def test_get_directors(self, client):
        """Test getting list of directors"""
        response = client.get("/api/directors")
        assert response.status_code == 200
        data = response.json()
        assert "directors" in data
        assert "count" in data
        assert isinstance(data["directors"], list)


class TestGenresAPI:
    """Test cases for Genres API endpoints"""
    
    def test_get_genres(self, client):
        """Test getting list of genres"""
        response = client.get("/api/genres")
        assert response.status_code == 200
        data = response.json()
        assert "genres" in data
        assert "count" in data
        assert isinstance(data["genres"], list)


class TestActorsAPI:
    """Test cases for Actors API endpoints"""
    
    def test_get_actors(self, client):
        """Test getting list of actors"""
        response = client.get("/api/actors")
        assert response.status_code == 200
        data = response.json()
        assert "actors" in data
        assert "count" in data
        assert isinstance(data["actors"], list)
    
    def test_get_actors_with_genre_filter(self, client):
        """Test getting actors filtered by genre"""
        response = client.get("/api/actors?genre=Action")
        assert response.status_code == 200
        data = response.json()
        assert "actors" in data
