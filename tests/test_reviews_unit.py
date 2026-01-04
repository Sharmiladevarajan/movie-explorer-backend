"""
Unit tests for Reviews API endpoints
"""
import pytest
import psycopg2


class TestCreateReview:
    """Test cases for POST /api/reviews"""
    
    def test_create_review_success(self, client, mock_db, sample_review):
        """Test successful review creation"""
        # Mock movie existence check
        mock_db.execute_query.return_value = {'id': 1}
        mock_db.execute_insert.return_value = sample_review
        
        payload = {
            "movie_id": 1,
            "reviewer_name": "John Doe",
            "rating": 5,
            "comment": "Excellent movie!"
        }
        
        response = client.post("/api/reviews", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data["reviewer_name"] == "John Doe"
    
    def test_create_review_missing_fields(self, client):
        """Test review creation with missing fields"""
        payload = {
            "movie_id": 1,
            "rating": 5
        }
        
        response = client.post("/api/reviews", json=payload)
        
        assert response.status_code == 422
    
    def test_create_review_invalid_rating(self, client):
        """Test review with invalid rating"""
        payload = {
            "movie_id": 1,
            "reviewer_name": "John",
            "rating": 11,  # Invalid rating > 10
            "comment": "Great"
        }
        
        response = client.post("/api/reviews", json=payload)
        
        assert response.status_code == 422


class TestGetMovieReviews:
    """Test cases for GET /api/movies/{movie_id}/reviews"""
    
    def test_get_movie_reviews_success(self, client, mock_db, sample_review):
        """Test successful retrieval of movie reviews"""
        mock_db.execute_query.return_value = [sample_review]
        
        response = client.get("/api/movies/1/reviews")
        
        assert response.status_code == 200
        data = response.json()
        assert "reviews" in data
        assert len(data["reviews"]) == 1
    
    def test_get_movie_reviews_empty(self, client, mock_db):
        """Test movie with no reviews"""
        mock_db.execute_query.return_value = []
        
        response = client.get("/api/movies/1/reviews")
        
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 0


class TestUpdateReview:
    """Test cases for PUT /api/reviews/{review_id}"""
    
    def test_update_review_success(self, client, mock_db, sample_review):
        """Test successful review update"""
        sample_review['comment'] = "Updated comment"
        
        mock_db.execute_query.side_effect = [
            {'id': 1},  # Review exists
            sample_review  # Return updated review
        ]
        mock_db.execute_update.return_value = True
        
        payload = {"comment": "Updated comment"}
        
        response = client.put("/api/reviews/1", json=payload)
        
        assert response.status_code == 200
    
    def test_update_review_not_found(self, client, mock_db):
        """Test updating non-existent review"""
        mock_db.execute_query.return_value = None
        
        payload = {"comment": "Updated"}
        
        response = client.put("/api/reviews/999", json=payload)
        
        assert response.status_code == 404


class TestDeleteReview:
    """Test cases for DELETE /api/reviews/{review_id}"""
    
    def test_delete_review_success(self, client, mock_db):
        """Test successful review deletion"""
        # Mock review exists check
        mock_db.execute_query.return_value = {'id': 1}
        mock_db.execute_delete.return_value = True
        
        response = client.delete("/api/reviews/1")
        
        assert response.status_code == 200
    
    def test_delete_review_not_found(self, client, mock_db):
        """Test deleting non-existent review"""
        mock_db.execute_query.return_value = None
        
        response = client.delete("/api/reviews/999")
        
        assert response.status_code == 404


@pytest.mark.parametrize("rating", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
def test_review_rating_range(client, mock_db, sample_review, rating):
    """Test reviews with valid rating range"""
    # Mock movie existence check first
    mock_db.execute_query.return_value = {'id': 1}
    sample_review['rating'] = rating
    mock_db.execute_insert.return_value = sample_review
    
    payload = {
        "movie_id": 1,
        "reviewer_name": "Test User",
        "rating": rating,
        "comment": "Test review"
    }
    
    response = client.post("/api/reviews", json=payload)
    
    assert response.status_code == 201
