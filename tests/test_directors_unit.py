"""
Unit tests for Directors API endpoints
"""
import pytest
import psycopg2


class TestGetDirectors:
    """Test cases for GET /api/directors"""
    
    def test_get_directors_success(self, client, mock_db, sample_director):
        """Test successful retrieval of directors"""
        mock_db.execute_query.return_value = [sample_director]
        
        response = client.get("/api/directors")
        
        assert response.status_code == 200
        data = response.json()
        assert "directors" in data
        assert "count" in data
        assert len(data["directors"]) == 1
    
    def test_get_directors_pagination(self, client, mock_db):
        """Test directors pagination"""
        mock_db.execute_query.return_value = []
        
        response = client.get("/api/directors?limit=50&offset=10")
        
        assert response.status_code == 200
    
    def test_get_directors_empty(self, client, mock_db):
        """Test when no directors found"""
        mock_db.execute_query.return_value = []
        
        response = client.get("/api/directors")
        
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 0


class TestGetDirectorById:
    """Test cases for GET /api/directors/{director_id}"""
    
    def test_get_director_success(self, client, mock_db, sample_director):
        """Test successful director retrieval"""
        sample_director['movies'] = []
        sample_director['movie_count'] = 0
        mock_db.execute_query.return_value = sample_director
        
        response = client.get("/api/directors/1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Steven Spielberg"
        assert "movies" in data
    
    def test_get_director_not_found(self, client, mock_db):
        """Test director not found"""
        mock_db.execute_query.return_value = None
        
        response = client.get("/api/directors/999")
        
        assert response.status_code == 404
    
    def test_get_director_database_error(self, client, mock_db):
        """Test database error handling"""
        mock_db.execute_query.side_effect = psycopg2.Error("Connection error")
        
        response = client.get("/api/directors/1")
        
        assert response.status_code == 500


@pytest.mark.parametrize("director_id", [1, 5, 10, 100])
def test_get_director_various_ids(client, mock_db, sample_director, director_id):
    """Test getting directors with various IDs"""
    sample_director['id'] = director_id
    sample_director['movies'] = []
    sample_director['movie_count'] = 0
    mock_db.execute_query.return_value = sample_director
    
    response = client.get(f"/api/directors/{director_id}")
    
    assert response.status_code == 200
    assert response.json()["id"] == director_id
