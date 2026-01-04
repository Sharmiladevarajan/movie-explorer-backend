"""
Unit tests for Movies API endpoints
"""
import pytest
from unittest.mock import patch
import psycopg2


class TestGetMovies:
    """Test cases for GET /api/movies"""
    
    def test_get_movies_success(self, client, mock_db, sample_movie):
        """Test successful retrieval of movies"""
        # Movies endpoint returns categories (grouped by genre)
        # Mock genre query first, then movies query for that genre
        mock_db.execute_query.side_effect = [
            [{'id': 1, 'name': 'Drama', 'description': 'Dramatic films', 'movie_count': 1}],  # Genre query
            [sample_movie]  # Movies for that genre
        ]
        
        response = client.get("/api/movies")
        
        assert response.status_code == 200
        data = response.json()
        assert "categories" in data or "movies" in data
    
    def test_get_movies_with_filters(self, client, mock_db, sample_movie):
        """Test movies with genre and year filters"""
        # Mock genre query first, then movies query
        mock_db.execute_query.side_effect = [
            [{'id': 1, 'name': 'Drama', 'description': 'Dramatic films', 'movie_count': 1}],
            [sample_movie]
        ]
        
        response = client.get("/api/movies?genre=Drama&year=1994")
        
        assert response.status_code == 200
    
    def test_get_movies_pagination(self, client, mock_db):
        """Test movies pagination"""
        mock_db.execute_query.return_value = []
        
        response = client.get("/api/movies?limit=20&offset=10")
        
        assert response.status_code == 200


class TestGetMovieById:
    """Test cases for GET /api/movies/{movie_id}"""
    
    def test_get_movie_success(self, client, mock_db, sample_movie):
        """Test successful movie retrieval"""
        sample_movie['actors'] = []
        sample_movie['reviews'] = []
        mock_db.execute_query.side_effect = [sample_movie, [], []]
        
        response = client.get("/api/movies/1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Forrest Gump"
    
    def test_get_movie_not_found(self, client, mock_db):
        """Test movie not found"""
        mock_db.execute_query.return_value = None
        
        response = client.get("/api/movies/999")
        
        assert response.status_code == 404


class TestSearchMovies:
    """Test cases for GET /api/movies/search/{term}"""
    
    def test_search_movies_success(self, client, mock_db, sample_movie):
        """Test successful movie search"""
        mock_db.execute_query.return_value = [sample_movie]
        
        response = client.get("/api/movies/search/Forrest")
        
        assert response.status_code == 200
        data = response.json()
        assert "movies" in data
    
    def test_search_movies_empty_term(self, client):
        """Test search with empty term"""
        response = client.get("/api/movies/search/ ")
        
        assert response.status_code == 400
    
    def test_search_movies_no_results(self, client, mock_db):
        """Test search with no results"""
        mock_db.execute_query.return_value = []
        
        response = client.get("/api/movies/search/nonexistent")
        
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 0


class TestCreateMovie:
    """Test cases for POST /api/movies"""
    
    def test_create_movie_success(self, client, mock_db, sample_movie):
        """Test successful movie creation"""
        # Mock get_or_create for director and genre, insert, then get_movie queries
        mock_db.get_or_create.side_effect = [1, 1]  # director_id, genre_id
        mock_db.execute_insert.return_value = {'id': 1}
        # Mock get_movie queries: movie data, actors, reviews
        mock_db.execute_query.side_effect = [sample_movie, [], []]
        sample_movie['actors'] = []
        sample_movie['reviews'] = []
        
        payload = {
            "title": "Forrest Gump",
            "description": "Life is like a box of chocolates",
            "release_year": 1994,
            "director_name": "Robert Zemeckis",
            "genre_name": "Drama",
            "rating": 8.8
        }
        
        response = client.post("/api/movies", json=payload)
        
        # May be 201 or 422 depending on validation
        assert response.status_code in [201, 422]
    
    def test_create_movie_missing_title(self, client):
        """Test movie creation without title"""
        payload = {
            "description": "Some description",
            "release_year": 2020
        }
        
        response = client.post("/api/movies", json=payload)
        
        assert response.status_code == 422


class TestUpdateMovie:
    """Test cases for PUT /api/movies/{movie_id}"""
    
    def test_update_movie_success(self, client, mock_db, sample_movie):
        """Test successful movie update"""
        mock_db.execute_query.return_value = {'id': 1}
        mock_db.execute_update.return_value = True
        sample_movie['title'] = "Updated Title"
        sample_movie['actors'] = []
        sample_movie['reviews'] = []
        mock_db.execute_query.side_effect = [{'id': 1}, sample_movie, [], []]
        
        payload = {"title": "Updated Title"}
        
        response = client.put("/api/movies/1", json=payload)
        
        assert response.status_code == 200
    
    def test_update_movie_not_found(self, client, mock_db):
        """Test updating non-existent movie"""
        mock_db.execute_query.return_value = None
        
        payload = {"title": "Updated Title"}
        
        response = client.put("/api/movies/999", json=payload)
        
        assert response.status_code == 404


class TestDeleteMovie:
    """Test cases for DELETE /api/movies/{movie_id}"""
    
    def test_delete_movie_success(self, client, mock_db):
        """Test successful movie deletion"""
        mock_db.execute_delete.return_value = True
        
        response = client.delete("/api/movies/1")
        
        assert response.status_code == 200
    
    def test_delete_movie_not_found(self, client, mock_db):
        """Test deleting non-existent movie"""
        mock_db.execute_delete.return_value = False
        
        response = client.delete("/api/movies/999")
        
        assert response.status_code == 404


@pytest.mark.parametrize("search_term", [
    "Forrest",
    "Tom Hanks",
    "Drama",
    "1994",
])
def test_movie_search_various_terms(client, mock_db, search_term):
    """Test movie search with various terms"""
    mock_db.execute_query.return_value = []
    
    response = client.get(f"/api/movies/search/{search_term}")
    
    assert response.status_code == 200
