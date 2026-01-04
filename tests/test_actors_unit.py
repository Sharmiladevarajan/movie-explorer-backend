"""
Unit tests for Actors API endpoints
"""
import pytest
from unittest.mock import patch, Mock
from fastapi import HTTPException
import psycopg2


class TestGetActors:
    """Test cases for GET /api/actors"""
    
    def test_get_actors_success(self, client, mock_db, sample_actor):
        """Test successful retrieval of actors list"""
        mock_db.execute_query.return_value = [sample_actor]
        
        response = client.get("/api/actors")
        
        assert response.status_code == 200
        data = response.json()
        assert "actors" in data
        assert "count" in data
        assert len(data["actors"]) == 1
        assert data["actors"][0]["name"] == "Tom Hanks"
        mock_db.execute_query.assert_called_once()
    
    def test_get_actors_with_limit_and_offset(self, client, mock_db, sample_actor):
        """Test actors pagination"""
        mock_db.execute_query.return_value = [sample_actor]
        
        response = client.get("/api/actors?limit=10&offset=5")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["actors"]) <= 10
    
    def test_get_actors_with_genre_filter(self, client, mock_db, sample_actor):
        """Test filtering actors by genre"""
        mock_db.execute_query.return_value = [sample_actor]
        
        response = client.get("/api/actors?genre=Drama")
        
        assert response.status_code == 200
        data = response.json()
        assert "actors" in data
    
    def test_get_actors_empty_result(self, client, mock_db):
        """Test when no actors are found"""
        mock_db.execute_query.return_value = []
        
        response = client.get("/api/actors")
        
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 0
        assert data["actors"] == []
    
    def test_get_actors_database_error(self, client, mock_db):
        """Test database error handling"""
        mock_db.execute_query.side_effect = psycopg2.Error("Database connection failed")
        
        response = client.get("/api/actors")
        
        assert response.status_code == 500
        assert "Database error" in response.json()["detail"]


class TestGetActorById:
    """Test cases for GET /api/actors/{actor_id}"""
    
    def test_get_actor_success(self, client, mock_db, sample_actor):
        """Test successful retrieval of single actor"""
        sample_actor['movies'] = []
        sample_actor['movie_count'] = 0
        mock_db.execute_query.return_value = sample_actor
        
        response = client.get("/api/actors/1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Tom Hanks"
        assert "movies" in data
        assert "movie_count" in data
    
    def test_get_actor_not_found(self, client, mock_db):
        """Test actor not found"""
        mock_db.execute_query.return_value = None
        
        response = client.get("/api/actors/999")
        
        assert response.status_code == 404
        assert "Actor not found" in response.json()["detail"]
    
    def test_get_actor_invalid_id(self, client):
        """Test invalid actor ID"""
        response = client.get("/api/actors/invalid")
        
        assert response.status_code == 422


class TestCreateActor:
    """Test cases for POST /api/actors"""
    
    def test_create_actor_success(self, client, mock_db, sample_actor):
        """Test successful actor creation"""
        mock_db.execute_insert.return_value = {'id': 1}
        sample_actor['movies'] = []
        sample_actor['movie_count'] = 0
        mock_db.execute_query.return_value = sample_actor
        
        payload = {
            "name": "Tom Hanks",
            "bio": "American actor",
            "birth_year": 1956
        }
        
        response = client.post("/api/actors", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Tom Hanks"
    
    def test_create_actor_missing_name(self, client):
        """Test actor creation without required name field"""
        payload = {
            "bio": "Some bio",
            "birth_year": 1980
        }
        
        response = client.post("/api/actors", json=payload)
        
        assert response.status_code == 422
    
    def test_create_actor_duplicate(self, client, mock_db):
        """Test duplicate actor creation"""
        mock_db.execute_insert.side_effect = psycopg2.IntegrityError("Duplicate entry")
        
        payload = {
            "name": "Tom Hanks",
            "bio": "American actor",
            "birth_year": 1956
        }
        
        response = client.post("/api/actors", json=payload)
        
        assert response.status_code == 400


class TestUpdateActor:
    """Test cases for PUT /api/actors/{actor_id}"""
    
    def test_update_actor_success(self, client, mock_db, sample_actor):
        """Test successful actor update"""
        sample_actor['bio'] = "Updated bio"
        sample_actor['movies'] = []
        sample_actor['movie_count'] = 0
        
        # Setup mock responses in order
        mock_db.execute_query.side_effect = [
            {'id': 1},  # Check existence
            sample_actor,  # Return updated actor from get_actor query
            []  # Empty movies list from get_actor query
        ]
        mock_db.execute_update.return_value = True
        
        payload = {"bio": "Updated bio"}
        
        response = client.put("/api/actors/1", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["bio"] == "Updated bio"
    
    def test_update_actor_not_found(self, client, mock_db):
        """Test updating non-existent actor"""
        mock_db.execute_query.return_value = None
        
        payload = {"bio": "Updated bio"}
        
        response = client.put("/api/actors/999", json=payload)
        
        assert response.status_code == 404
    
    def test_update_actor_no_fields(self, client, mock_db, sample_actor):
        """Test update with no fields provided"""
        sample_actor['movies'] = []
        sample_actor['movie_count'] = 0
        
        # Setup mock responses
        mock_db.execute_query.side_effect = [
            {'id': 1},  # Check existence
            sample_actor,  # Return actor from get_actor query
            []  # Empty movies list from get_actor query
        ]
        
        payload = {}
        
        response = client.put("/api/actors/1", json=payload)
        
        assert response.status_code == 200


class TestDeleteActor:
    """Test cases for DELETE /api/actors/{actor_id}"""
    
    def test_delete_actor_success(self, client, mock_db):
        """Test successful actor deletion"""
        mock_db.execute_delete.return_value = True
        
        response = client.delete("/api/actors/1")
        
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]
    
    def test_delete_actor_not_found(self, client, mock_db):
        """Test deleting non-existent actor"""
        mock_db.execute_delete.return_value = False
        
        response = client.delete("/api/actors/999")
        
        assert response.status_code == 404


@pytest.mark.parametrize("limit,offset", [
    (10, 0),
    (50, 10),
    (100, 50),
    (500, 0),
])
def test_actors_pagination_params(client, mock_db, limit, offset):
    """Test various pagination parameters"""
    mock_db.execute_query.return_value = []
    
    response = client.get(f"/api/actors?limit={limit}&offset={offset}")
    
    assert response.status_code == 200
