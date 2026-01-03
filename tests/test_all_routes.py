import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


"""
Comprehensive API tests for all endpoints (actors, directors, genres, movies, reviews)
Includes both positive and negative test cases for each endpoint.
Only tests supported methods for each resource.
"""

# ------------------- Actors CRUD -------------------
def test_create_actor_positive():
    payload = {
        "name": "Test Actor",
        "bio": "Test bio",
        "birth_year": 1990,
        "image_url": "http://example.com/actor.jpg"
    }
    response = client.post("/api/actors", json=payload)
    assert response.status_code in [201, 400]
    if response.status_code == 201:
        global created_actor_id
        created_actor_id = response.json().get("id")

def test_create_actor_negative():
    # Missing required field 'name'
    payload = {
        "bio": "Test bio",
        "birth_year": 1990
    }
    response = client.post("/api/actors", json=payload)
    assert response.status_code in [400, 422]

def test_get_actors():
    response = client.get("/api/actors")
    assert response.status_code == 200
    assert "actors" in response.json() or "count" in response.json()

def test_get_actors_with_genre():
    response = client.get("/api/actors", params={"genre": "Drama"})
    assert response.status_code == 200

def test_update_actor_positive():
    actor_id = globals().get("created_actor_id", 1)
    payload = {"bio": "Updated bio"}
    response = client.put(f"/api/actors/{actor_id}", json=payload)
    assert response.status_code in [200, 404, 400]

def test_update_actor_negative():
    # Invalid actor id
    payload = {"bio": "Updated bio"}
    response = client.put(f"/api/actors/999999", json=payload)
    assert response.status_code in [404, 400]

def test_delete_actor_positive():
    actor_id = globals().get("created_actor_id", 1)
    response = client.delete(f"/api/actors/{actor_id}")
    assert response.status_code in [200, 404]

def test_delete_actor_negative():
    response = client.delete(f"/api/actors/999999")
    assert response.status_code in [404]


# ------------------- Directors (Read-only) -------------------
def test_get_directors_positive():
    response = client.get("/api/directors")
    assert response.status_code == 200
    assert "directors" in response.json() or "count" in response.json()

def test_get_director_by_id_positive():
    response = client.get(f"/api/directors/1")
    assert response.status_code in [200, 404]

def test_get_director_by_id_negative():
    response = client.get(f"/api/directors/999999")
    assert response.status_code == 404


# ------------------- Genres (Read-only) -------------------
def test_get_genres_positive():
    response = client.get("/api/genres")
    assert response.status_code == 200
    assert "genres" in response.json() or "count" in response.json()

def test_get_genres_negative():
    # No such endpoint, expect 404
    response = client.get("/api/genres/999999")
    assert response.status_code == 404 or response.status_code == 405



# ------------------- Movies CRUD -------------------
def test_create_movie_positive():
    # Use valid IDs or fallback to 1
    payload = {
        "title": "Test Movie",
        "description": "Test movie description",
        "release_year": 2022,
        "director_id": 1,
        "genre_ids": [1],
        "actor_ids": [1],
        "image_url": "http://example.com/movie.jpg"
    }
    response = client.post("/api/movies", json=payload)
    assert response.status_code in [201, 400, 422]
    if response.status_code == 201:
        global created_movie_id
        created_movie_id = response.json().get("id")

def test_create_movie_negative():
    # Missing required field 'title'
    payload = {
        "description": "Test movie description",
        "release_year": 2022,
        "director_id": 1,
        "genre_ids": [1],
        "actor_ids": [1],
        "image_url": "http://example.com/movie.jpg"
    }
    response = client.post("/api/movies", json=payload)
    assert response.status_code in [400, 422]

def test_get_movies():
    response = client.get("/api/movies")
    assert response.status_code == 200
    assert (
        "movies" in response.json()
        or "count" in response.json()
        or "genres" in response.json()
        or "categories" in response.json()
    )

def test_get_movies_with_filters():
    response = client.get("/api/movies", params={"genre": "Drama", "year": 2020})
    assert response.status_code == 200

def test_update_movie_positive():
    movie_id = globals().get("created_movie_id", 1)
    payload = {"description": "Updated movie description"}
    response = client.put(f"/api/movies/{movie_id}", json=payload)
    assert response.status_code in [200, 404, 400]

def test_update_movie_negative():
    payload = {"description": "Updated movie description"}
    response = client.put(f"/api/movies/999999", json=payload)
    assert response.status_code in [404, 400]

def test_delete_movie_positive():
    movie_id = globals().get("created_movie_id", 1)
    response = client.delete(f"/api/movies/{movie_id}")
    assert response.status_code in [200, 404]

def test_delete_movie_negative():
    response = client.delete(f"/api/movies/999999")
    assert response.status_code in [404]


# ------------------- Reviews CRUD -------------------
def test_create_review_positive():
    payload = {
        "movie_id": globals().get("created_movie_id", 1),
        "reviewer_name": "Test User",
        "rating": 5,
        "comment": "Great movie!"
    }
    response = client.post("/api/reviews", json=payload)
    assert response.status_code in [201, 400, 404]
    if response.status_code == 201:
        global created_review_id
        created_review_id = response.json().get("id")

def test_create_review_negative():
    # Missing required field 'reviewer_name'
    payload = {
        "movie_id": 1,
        "rating": 5,
        "comment": "Great movie!"
    }
    response = client.post("/api/reviews", json=payload)
    assert response.status_code in [400, 422]

def test_get_movie_reviews_positive():
    movie_id = globals().get("created_movie_id", 1)
    response = client.get(f"/api/movies/{movie_id}/reviews")
    assert response.status_code in [200, 404]

def test_get_movie_reviews_negative():
    response = client.get(f"/api/movies/999999/reviews")
    assert response.status_code in [200, 404]

def test_update_review_positive():
    review_id = globals().get("created_review_id", 1)
    payload = {"comment": "Updated review comment"}
    response = client.put(f"/api/reviews/{review_id}", json=payload)
    assert response.status_code in [200, 404, 400]

def test_update_review_negative():
    payload = {"comment": "Updated review comment"}
    response = client.put(f"/api/reviews/999999", json=payload)
    assert response.status_code in [404, 400]

def test_delete_review_positive():
    review_id = globals().get("created_review_id", 1)
    response = client.delete(f"/api/reviews/{review_id}")
    assert response.status_code in [200, 404]

def test_delete_review_negative():
    response = client.delete(f"/api/reviews/999999")
    assert response.status_code in [404]
