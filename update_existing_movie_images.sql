-- Update existing movies with image URLs
-- Run this after adding the image_url column

UPDATE movies 
SET image_url = 'https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_SX300.jpg'
WHERE title = 'Inception';

UPDATE movies 
SET image_url = 'https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_SX300.jpg'
WHERE title = 'The Dark Knight';

UPDATE movies 
SET image_url = 'https://m.media-amazon.com/images/M/MV5BNGNhMDIzZTUtNTBlZi00MTRlLWFjM2ItYzViMjE3YzI5MjljXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg'
WHERE title = 'Pulp Fiction';

UPDATE movies 
SET image_url = 'https://m.media-amazon.com/images/M/MV5BNDE4OTMxMTctNmRhYy00NWE2LTg3YzItYTk3M2UwOTU5Njg4XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg'
WHERE title = 'Schindler''s List';

UPDATE movies 
SET image_url = 'https://m.media-amazon.com/images/M/MV5BMjIxMjgxNTk0MF5BMl5BanBnXkFtZTgwNjIyOTg2MDE@._V1_SX300.jpg'
WHERE title = 'The Wolf of Wall Street';

UPDATE movies 
SET image_url = 'https://m.media-amazon.com/images/M/MV5BYzExYmRiNGItMWMwZC00MTgzLTkyOTYtZmZhZTdmODNjMjZkXkEyXkFqcGc@._V1_SX300.jpg'
WHERE title = 'Barbie';

-- Check results
SELECT id, title, 
       CASE 
           WHEN image_url IS NULL THEN 'NO IMAGE'
           ELSE 'HAS IMAGE'
       END as status,
       LEFT(image_url, 50) as image_preview
FROM movies
ORDER BY id;
