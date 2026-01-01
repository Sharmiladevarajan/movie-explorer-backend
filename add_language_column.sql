-- Add language column to movies table
ALTER TABLE movies ADD COLUMN IF NOT EXISTS language VARCHAR(50) DEFAULT 'English';

-- Update existing movies with default language
UPDATE movies SET language = 'English' WHERE language IS NULL;

-- Add index for language searches
CREATE INDEX IF NOT EXISTS idx_movies_language ON movies(language);

-- Update demo movies with appropriate languages
UPDATE movies SET language = 'English' WHERE title IN (
    'Inception', 'The Dark Knight', 'Pulp Fiction', 'The Wolf of Wall Street',
    'Fight Club', 'Gladiator', 'Avatar', 'Gravity', 'La La Land'
);

UPDATE movies SET language = 'Japanese' WHERE title = 'Spirited Away';
UPDATE movies SET language = 'English' WHERE title IN ('The Grand Budapest Hotel', 'The Godfather');
UPDATE movies SET language = 'English' WHERE title LIKE 'The Lord of the Rings%';
UPDATE movies SET language = 'English' WHERE title IN ('Blade Runner 2049', 'Dune');

SELECT 'Language column added successfully!' as status;
