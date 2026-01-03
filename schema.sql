-- Movie Explorer Database Schema
-- PostgreSQL Schema for Movie Explorer Platform

-- Enable UUID extension (optional, for future use)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Genres Table
CREATE TABLE IF NOT EXISTS genres (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Directors Table
CREATE TABLE IF NOT EXISTS directors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    bio TEXT,
    birth_year INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Actors Table
CREATE TABLE IF NOT EXISTS actors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    bio TEXT,
    birth_year INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Movies Table
CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    director_id INTEGER REFERENCES directors(id) ON DELETE SET NULL,
    genre_id INTEGER REFERENCES genres(id) ON DELETE SET NULL,
    release_year INTEGER NOT NULL,
    rating DECIMAL(3, 1) CHECK (rating >= 0 AND rating <= 10),
    description TEXT,
    image_url TEXT
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Movie-Actor Junction Table (Many-to-Many)
CREATE TABLE IF NOT EXISTS movie_actors (
    id SERIAL PRIMARY KEY,
    movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
    actor_id INTEGER REFERENCES actors(id) ON DELETE CASCADE,
    role VARCHAR(255), -- Character name
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(movie_id, actor_id)
);

-- Movie-Genre Junction Table (Many-to-Many for multiple genres per movie)
CREATE TABLE IF NOT EXISTS movie_genres (
    id SERIAL PRIMARY KEY,
    movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
    genre_id INTEGER REFERENCES genres(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(movie_id, genre_id)
);

-- Reviews Table
CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
    reviewer_name VARCHAR(255) NOT NULL,
    rating DECIMAL(3, 1) CHECK (rating >= 0 AND rating <= 10),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for better query performance
CREATE INDEX idx_movies_director ON movies(director_id);
CREATE INDEX idx_movies_genre ON movies(genre_id);
CREATE INDEX idx_movies_release_year ON movies(release_year);
CREATE INDEX idx_movie_actors_movie ON movie_actors(movie_id);
CREATE INDEX idx_movie_actors_actor ON movie_actors(actor_id);
CREATE INDEX idx_movie_genres_movie ON movie_genres(movie_id);
CREATE INDEX idx_movie_genres_genre ON movie_genres(genre_id);
CREATE INDEX idx_reviews_movie ON reviews(movie_id);

-- Sample Data
-- Insert sample genres
INSERT INTO genres (name, description) VALUES
('Action', 'High-energy films with intense physical activity'),
('Drama', 'Serious narrative fiction'),
('Comedy', 'Films designed to elicit laughter'),
('Sci-Fi', 'Science fiction and futuristic themes'),
('Thriller', 'Suspenseful and exciting films'),
('Horror', 'Films designed to frighten and scare'),
('Romance', 'Love stories and romantic relationships'),
('Adventure', 'Exciting journeys and expeditions'),
('Fantasy', 'Magical and fantastical themes'),
('Documentary', 'Non-fiction films')
ON CONFLICT (name) DO NOTHING;

-- Insert sample directors
INSERT INTO directors (name, bio, birth_year) VALUES
('Christopher Nolan', 'British-American filmmaker known for complex narratives', 1970),
('Quentin Tarantino', 'American filmmaker known for stylized violence', 1963),
('Steven Spielberg', 'American director and producer, one of the founding pioneers', 1946),
('Martin Scorsese', 'American film director, producer, and screenwriter', 1942),
('Greta Gerwig', 'American actress, playwright, screenwriter, and director', 1983);

-- Insert sample actors
INSERT INTO actors (name, bio, birth_year) VALUES
('Leonardo DiCaprio', 'American actor and film producer', 1974),
('Christian Bale', 'English actor known for intense method acting', 1974),
('Margot Robbie', 'Australian actress and producer', 1990),
('Tom Hanks', 'American actor and filmmaker', 1956),
('Meryl Streep', 'American actress often regarded as the best of her generation', 1949),
('Ryan Gosling', 'Canadian actor and musician', 1980),
('Scarlett Johansson', 'American actress and singer', 1984),
('Robert De Niro', 'American actor, producer, and director', 1943);

-- Insert sample movies
INSERT INTO movies (title, director_id, genre_id, release_year, rating, description) VALUES
('Inception', 1, 4, 2010, 8.8, 'A thief who steals corporate secrets through dream-sharing technology'),
('The Dark Knight', 1, 1, 2008, 9.0, 'Batman faces the Joker in a battle for Gotham City''s soul'),
('Pulp Fiction', 2, 5, 1994, 8.9, 'The lives of two mob hitmen, a boxer, and a pair of diner bandits intertwine'),
('Schindler''s List', 3, 2, 1993, 9.0, 'The story of Oskar Schindler who saved over a thousand Jewish lives'),
('The Wolf of Wall Street', 4, 2, 2013, 8.2, 'Based on the true story of Jordan Belfort''s rise and fall'),
('Barbie', 5, 3, 2023, 7.0, 'Barbie and Ken have the time of their lives in Barbie Land');

-- Insert movie-actor relationships
INSERT INTO movie_actors (movie_id, actor_id, role) VALUES
(1, 1, 'Dom Cobb'),
(2, 2, 'Bruce Wayne / Batman'),
(5, 1, 'Jordan Belfort'),
(6, 3, 'Barbie'),
(6, 6, 'Ken');

-- Insert movie-genre relationships (supporting multiple genres)
INSERT INTO movie_genres (movie_id, genre_id) VALUES
(1, 4), -- Inception: Sci-Fi
(1, 5), -- Inception: Thriller
(2, 1), -- Dark Knight: Action
(2, 5), -- Dark Knight: Thriller
(3, 2), -- Pulp Fiction: Drama
(3, 5), -- Pulp Fiction: Thriller
(4, 2), -- Schindler's List: Drama
(5, 2), -- Wolf of Wall Street: Drama
(5, 3), -- Wolf of Wall Street: Comedy
(6, 3), -- Barbie: Comedy
(6, 8); -- Barbie: Adventure

-- Insert sample reviews
INSERT INTO reviews (movie_id, reviewer_name, rating, comment) VALUES
(1, 'John Smith', 9.0, 'Mind-bending masterpiece! A must-watch.'),
(1, 'Jane Doe', 8.5, 'Complex but rewarding. Great visuals.'),
(2, 'Bob Wilson', 10.0, 'Best superhero movie ever made!'),
(3, 'Alice Johnson', 9.0, 'Tarantino at his finest.'),
(6, 'Emma Brown', 7.5, 'Fun and colorful! Great for all ages.');
