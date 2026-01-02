-- Demo Data for Netflix-Style UI
-- Run this to add more movies for better horizontal scrolling demo

-- Add more diverse genres
INSERT INTO genres (name, description) VALUES
('Crime', 'Films about criminal activities and law enforcement'),
('Mystery', 'Films involving solving puzzles or crimes'),
('Biography', 'Films based on real people''s lives'),
('Animation', 'Animated films and cartoons'),
('Musical', 'Films featuring songs and dance sequences')
ON CONFLICT (name) DO NOTHING;

-- Add more directors
INSERT INTO directors (name, bio, birth_year) VALUES
('Denis Villeneuve', 'Canadian filmmaker known for sci-fi and thriller films', 1967),
('Wes Anderson', 'American filmmaker known for distinctive visual style', 1969),
('James Cameron', 'Canadian filmmaker known for epic science fiction films', 1954),
('David Fincher', 'American filmmaker known for psychological thrillers', 1962),
('Ridley Scott', 'British filmmaker known for sci-fi and historical epics', 1937),
('Francis Ford Coppola', 'American film director and producer', 1939),
('Peter Jackson', 'New Zealand filmmaker', 1961),
('Alfonso Cuarón', 'Mexican filmmaker', 1961),
('Hayao Miyazaki', 'Japanese animator and filmmaker', 1941),
('Damien Chazelle', 'American film director', 1985);

-- Add more actors
INSERT INTO actors (name, bio, birth_year) VALUES
('Timothée Chalamet', 'American-French actor', 1995),
('Zendaya', 'American actress and singer', 1996),
('Brad Pitt', 'American actor and film producer', 1963),
('Natalie Portman', 'Israeli-American actress', 1981),
('Denzel Washington', 'American actor and filmmaker', 1954),
('Cate Blanchett', 'Australian actress', 1969),
('Morgan Freeman', 'American actor and narrator', 1937),
('Emma Stone', 'American actress', 1988),
('Al Pacino', 'American actor and filmmaker', 1940),
('Elijah Wood', 'American actor', 1981),
('Ian McKellen', 'English actor', 1939),
('Sandra Bullock', 'American actress and producer', 1964);

-- Add comprehensive movie collection for better UI demo
-- Sci-Fi Movies
INSERT INTO movies (title, director_id, genre_id, release_year, rating, description, image_url)
SELECT 
    'Dune', 
    d.id, 
    g.id, 
    2021, 
    8.1, 
    'A noble family becomes embroiled in a war for control over the galaxy''s most valuable asset while the heir becomes troubled by visions of a dark future',
    'https://m.media-amazon.com/images/M/MV5BMDQ0NjgyN2YtNWViNS00YjA3LTkxNDktYzFkZTExZGMxZDkxXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_SX300.jpg'
FROM directors d 
CROSS JOIN genres g 
WHERE d.name = 'Denis Villeneuve' AND g.name = 'Sci-Fi'
ON CONFLICT DO NOTHING;

INSERT INTO movies (title, director_id, genre_id, release_year, rating, description, image_url)
SELECT 
    'Avatar', 
    d.id, 
    g.id, 
    2009, 
    7.9, 
    'A paraplegic Marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home',
    'https://m.media-amazon.com/images/M/MV5BZDA0OGQxNTItMDZkMC00N2UyLTg3MzMtYTJmNjg3Nzk5MzRiXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_SX300.jpg'
FROM directors d 
CROSS JOIN genres g 
WHERE d.name = 'James Cameron' AND g.name = 'Sci-Fi'
ON CONFLICT DO NOTHING;

INSERT INTO movies (title, director_id, genre_id, release_year, rating, description, image_url)
SELECT 
    'Blade Runner 2049', 
    d.id, 
    g.id, 
    2017, 
    8.0, 
    'A young blade runner''s discovery of a long-buried secret leads him to track down former blade runner Rick Deckard',
    'https://m.media-amazon.com/images/M/MV5BNzA1Njg4NzYxOV5BMl5BanBnXkFtZTgwODk5NjU3MzI@._V1_SX300.jpg'
FROM directors d 
CROSS JOIN genres g 
WHERE d.name = 'Denis Villeneuve' AND g.name = 'Sci-Fi'
ON CONFLICT DO NOTHING;

-- Drama Movies
INSERT INTO movies (title, director_id, genre_id, release_year, rating, description, image_url)
SELECT 
    'Fight Club', 
    d.id, 
    g.id, 
    1999, 
    8.8, 
    'An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into much more',
    'https://m.media-amazon.com/images/M/MV5BOTgyOGQ1NDItNGU3Ny00MjU3LTg2YWEtNmEyYjBiMjI1Y2M5XkEyXkFqcGc@._V1_SX300.jpg'
FROM directors d 
CROSS JOIN genres g 
WHERE d.name = 'David Fincher' AND g.name = 'Drama'
ON CONFLICT DO NOTHING;

INSERT INTO movies (title, director_id, genre_id, release_year, rating, description, image_url)
SELECT 
    'The Godfather', 
    d.id, 
    g.id, 
    1972, 
    9.2, 
    'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son',
    'https://m.media-amazon.com/images/M/MV5BYTJkNGQyZDgtZDQ0NC00MDM0LWEzZWQtYzUzZDEwMDljZWNjXkEyXkFqcGc@._V1_SX300.jpg'
FROM directors d 
CROSS JOIN genres g 
WHERE d.name = 'Francis Ford Coppola' AND g.name = 'Drama'
ON CONFLICT DO NOTHING;

INSERT INTO movies (title, director_id, genre_id, release_year, rating, description, image_url)
SELECT 
    'Gravity', 
    d.id, 
    g.id, 
    2013, 
    7.7, 
    'Two astronauts work together to survive after an accident leaves them stranded in space',
    'https://m.media-amazon.com/images/M/MV5BNjE5MzYwMzYxMF5BMl5BanBnXkFtZTcwOTk4MTk0OQ@@._V1_SX300.jpg'
FROM directors d 
CROSS JOIN genres g 
WHERE d.name = 'Alfonso Cuarón' AND g.name = 'Drama'
ON CONFLICT DO NOTHING;

-- Comedy Movies
INSERT INTO movies (title, director_id, genre_id, release_year, rating, description, image_url)
SELECT 
    'The Grand Budapest Hotel', 
    d.id, 
    g.id, 
    2014, 
    8.1, 
    'A writer encounters the owner of an aging high-class hotel, who tells him of his early years serving as a lobby boy in the hotel''s glorious years under an exceptional concierge',
    'https://m.media-amazon.com/images/M/MV5BMzM5NjUxOTEyMl5BMl5BanBnXkFtZTgwNjEyMDM0MDE@._V1_SX300.jpg'
FROM directors d 
CROSS JOIN genres g 
WHERE d.name = 'Wes Anderson' AND g.name = 'Comedy'
ON CONFLICT DO NOTHING;

-- Action Movies
INSERT INTO movies (title, director_id, genre_id, release_year, rating, description, image_url)
SELECT 
    'Gladiator', 
    d.id, 
    g.id, 
    2000, 
    8.5, 
    'A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery',
    'https://m.media-amazon.com/images/M/MV5BYWQ4YmNjYjEtOWE1Zi00Y2U4LWI4NTAtMTU0MjkxNWQ1ZmJiXkEyXkFqcGc@._V1_SX300.jpg'
FROM directors d 
CROSS JOIN genres g 
WHERE d.name = 'Ridley Scott' AND g.name = 'Action'
ON CONFLICT DO NOTHING;

-- Adventure Movies
INSERT INTO movies (title, director_id, genre_id, release_year, rating, description, image_url)
SELECT 
    'The Lord of the Rings: The Fellowship of the Ring', 
    d.id, 
    g.id, 
    2001, 
    8.8, 
    'A meek Hobbit and eight companions set out on a journey to destroy the One Ring and the dark lord Sauron',
    'https://m.media-amazon.com/images/M/MV5BNzIxMDQ2YTctNDY4MC00ZTRhLTk4ODQtMTVlOWY4NTdiYmMwXkEyXkFqcGc@._V1_SX300.jpg'
FROM directors d 
CROSS JOIN genres g 
WHERE d.name = 'Peter Jackson' AND g.name = 'Adventure'
ON CONFLICT DO NOTHING;

-- Animation Movies
INSERT INTO movies (title, director_id, genre_id, release_year, rating, description, image_url)
SELECT 
    'Spirited Away', 
    d.id, 
    g.id, 
    2001, 
    8.6, 
    'During her family''s move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits',
    'https://m.media-amazon.com/images/M/MV5BMjlmZmI5MDctNDE2YS00YWE0LWE5ZWItZDBhYWQ0NTcxNWRhXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg'
FROM directors d 
CROSS JOIN genres g 
WHERE d.name = 'Hayao Miyazaki' AND g.name = 'Animation'
ON CONFLICT DO NOTHING;

-- Musical Movies
INSERT INTO movies (title, director_id, genre_id, release_year, rating, description, image_url)
SELECT 
    'La La Land', 
    d.id, 
    g.id, 
    2016, 
    8.0, 
    'While navigating their careers in Los Angeles, a pianist and an actress fall in love while attempting to reconcile their aspirations for the future',
    'https://m.media-amazon.com/images/M/MV5BMzUzNDM2NzM2MV5BMl5BanBnXkFtZTgwNTM3NTg4OTE@._V1_SX300.jpg'
FROM directors d 
CROSS JOIN genres g 
WHERE d.name = 'Damien Chazelle' AND g.name = 'Musical'
ON CONFLICT DO NOTHING;

-- Link actors to new movies
-- Dune cast
INSERT INTO movie_actors (movie_id, actor_id, role)
SELECT m.id, a.id, 'Paul Atreides'
FROM movies m 
CROSS JOIN actors a
WHERE m.title = 'Dune' AND a.name = 'Timothée Chalamet'
ON CONFLICT DO NOTHING;

INSERT INTO movie_actors (movie_id, actor_id, role)
SELECT m.id, a.id, 'Chani'
FROM movies m 
CROSS JOIN actors a
WHERE m.title = 'Dune' AND a.name = 'Zendaya'
ON CONFLICT DO NOTHING;

-- Fight Club cast
INSERT INTO movie_actors (movie_id, actor_id, role)
SELECT m.id, a.id, 'Tyler Durden'
FROM movies m 
CROSS JOIN actors a
WHERE m.title = 'Fight Club' AND a.name = 'Brad Pitt'
ON CONFLICT DO NOTHING;

-- Godfather cast
INSERT INTO movie_actors (movie_id, actor_id, role)
SELECT m.id, a.id, 'Michael Corleone'
FROM movies m 
CROSS JOIN actors a
WHERE m.title = 'The Godfather' AND a.name = 'Al Pacino'
ON CONFLICT DO NOTHING;

-- LOTR cast
INSERT INTO movie_actors (movie_id, actor_id, role)
SELECT m.id, a.id, 'Frodo Baggins'
FROM movies m 
CROSS JOIN actors a
WHERE m.title LIKE 'The Lord of the Rings%' AND a.name = 'Elijah Wood'
ON CONFLICT DO NOTHING;

INSERT INTO movie_actors (movie_id, actor_id, role)
SELECT m.id, a.id, 'Gandalf'
FROM movies m 
CROSS JOIN actors a
WHERE m.title LIKE 'The Lord of the Rings%' AND a.name = 'Ian McKellen'
ON CONFLICT DO NOTHING;

-- Gravity cast
INSERT INTO movie_actors (movie_id, actor_id, role)
SELECT m.id, a.id, 'Dr. Ryan Stone'
FROM movies m 
CROSS JOIN actors a
WHERE m.title = 'Gravity' AND a.name = 'Sandra Bullock'
ON CONFLICT DO NOTHING;

-- La La Land cast
INSERT INTO movie_actors (movie_id, actor_id, role)
SELECT m.id, a.id, 'Mia'
FROM movies m 
CROSS JOIN actors a
WHERE m.title = 'La La Land' AND a.name = 'Emma Stone'
ON CONFLICT DO NOTHING;

-- Add more reviews for engagement
INSERT INTO reviews (movie_id, reviewer_name, rating, comment)
SELECT m.id, 'Michael Chen', 9.5, 'Stunning visuals and epic storytelling. A sci-fi masterpiece that stays true to the book!'
FROM movies m WHERE m.title = 'Dune'
ON CONFLICT DO NOTHING;

INSERT INTO reviews (movie_id, reviewer_name, rating, comment)
SELECT m.id, 'Sarah Parker', 8.0, 'Quirky, delightful, and visually stunning. Vintage Wes Anderson at his best!'
FROM movies m WHERE m.title = 'The Grand Budapest Hotel'
ON CONFLICT DO NOTHING;

INSERT INTO reviews (movie_id, reviewer_name, rating, comment)
SELECT m.id, 'David Miller', 9.0, 'Mind-blowing twist. One of the best endings in cinema history!'
FROM movies m WHERE m.title = 'Fight Club'
ON CONFLICT DO NOTHING;

INSERT INTO reviews (movie_id, reviewer_name, rating, comment)
SELECT m.id, 'Emily Rodriguez', 9.5, 'The greatest film ever made. A masterclass in storytelling and cinematography.'
FROM movies m WHERE m.title = 'The Godfather'
ON CONFLICT DO NOTHING;

INSERT INTO reviews (movie_id, reviewer_name, rating, comment)
SELECT m.id, 'James Wilson', 9.0, 'Epic fantasy adventure. The beginning of an unforgettable trilogy!'
FROM movies m WHERE m.title LIKE 'The Lord of the Rings%'
ON CONFLICT DO NOTHING;

INSERT INTO reviews (movie_id, reviewer_name, rating, comment)
SELECT m.id, 'Lisa Thompson', 8.5, 'Breathtaking animation and heartwarming story. Miyazaki''s finest work!'
FROM movies m WHERE m.title = 'Spirited Away'
ON CONFLICT DO NOTHING;

INSERT INTO reviews (movie_id, reviewer_name, rating, comment)
SELECT m.id, 'Tom Anderson', 8.0, 'A love letter to Hollywood musicals. Beautiful cinematography and music!'
FROM movies m WHERE m.title = 'La La Land'
ON CONFLICT DO NOTHING;

-- Performance check
SELECT 'Data population complete!' as status;
SELECT COUNT(*) as total_movies FROM movies;
SELECT COUNT(*) as total_actors FROM actors;
SELECT COUNT(*) as total_directors FROM directors;
SELECT COUNT(*) as total_genres FROM genres;
SELECT COUNT(*) as total_reviews FROM reviews;
