"""
Unit tests for Genres API endpoints
"""
import pytest
import psycopg2


class TestGetGenres:
    """Test cases for GET /api/genres"""
    
    def test_get_genres_success(self, client, mock_db, sample_genre):
        """Test successful retrieval of genres"""
        mock_db.execute_query.return_value = [sample_genre]
        
        response = client.get("/api/genres")
        
        assert response.status_code == 200
        data = response.json()
        assert "genres" in data
        assert "count" in data
        assert len(data["genres"]) == 1
        assert data["genres"][0]["name"] == "Drama"
    
    def test_get_genres_pagination(self, client, mock_db):
        """Test genres pagination"""
        mock_db.execute_query.return_value = []
        
        response = client.get("/api/genres?limit=20&offset=0")
        
        assert response.status_code == 200
    
    def test_get_genres_empty(self, client, mock_db):
        """Test when no genres found"""
        mock_db.execute_query.return_value = []
        
        response = client.get("/api/genres")
        
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 0
        assert data["genres"] == []
    
    def test_get_genres_database_error(self, client, mock_db):
        """Test database error handling"""
        mock_db.execute_query.side_effect = psycopg2.Error("Database error")
        
        response = client.get("/api/genres")
        
        assert response.status_code == 500


@pytest.mark.parametrize("limit,offset", [
    (10, 0),
    (20, 5),
    (50, 0),
])
def test_genres_pagination_params(client, mock_db, limit, offset):
    """Test various pagination parameters"""
    mock_db.execute_query.return_value = []
    
    response = client.get(f"/api/genres?limit={limit}&offset={offset}")
    
    assert response.status_code == 200
