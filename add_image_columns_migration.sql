-- Combined migration: Add image support for both actors and directors
-- Migration: Add image_url columns to actors and directors tables

BEGIN;

-- Add image_url column to actors table
ALTER TABLE actors 
ADD COLUMN IF NOT EXISTS image_url TEXT;

-- Add image_url column to directors table
ALTER TABLE directors 
ADD COLUMN IF NOT EXISTS image_url TEXT;

-- Add comments for documentation
COMMENT ON COLUMN actors.image_url IS 'URL to actor profile image or photo';
COMMENT ON COLUMN directors.image_url IS 'URL to director profile image or photo';

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_actors_has_image ON actors(image_url) WHERE image_url IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_directors_has_image ON directors(image_url) WHERE image_url IS NOT NULL;

-- Update existing actors with sample image URLs
UPDATE actors SET image_url = CASE
    WHEN name = 'Leonardo DiCaprio' THEN 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&crop=face'
    WHEN name = 'Christian Bale' THEN 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&h=400&fit=crop&crop=face'
    WHEN name = 'Margot Robbie' THEN 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=400&h=400&fit=crop&crop=face'
    WHEN name = 'Tom Hanks' THEN 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop&crop=face'
    WHEN name = 'Meryl Streep' THEN 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=400&h=400&fit=crop&crop=face'
    WHEN name = 'Ryan Gosling' THEN 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&h=400&fit=crop&crop=face'
    WHEN name = 'Scarlett Johansson' THEN 'https://images.unsplash.com/photo-1489424731084-a5d8b219a5bb?w=400&h=400&fit=crop&crop=face'
    WHEN name = 'Robert De Niro' THEN 'https://images.unsplash.com/photo-1507591064344-4c6ce005b128?w=400&h=400&fit=crop&crop=face'
    ELSE NULL
END
WHERE name IN (
    'Leonardo DiCaprio', 'Christian Bale', 'Margot Robbie', 'Tom Hanks', 
    'Meryl Streep', 'Ryan Gosling', 'Scarlett Johansson', 'Robert De Niro'
);

-- Update existing directors with sample image URLs
UPDATE directors SET image_url = CASE
    WHEN name = 'Christopher Nolan' THEN 'https://images.unsplash.com/photo-1560250097-0b93528c311a?w=400&h=400&fit=crop&crop=face'
    WHEN name = 'Quentin Tarantino' THEN 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400&h=400&fit=crop&crop=face'
    WHEN name = 'Steven Spielberg' THEN 'https://images.unsplash.com/photo-1566492031773-4f4e44671d66?w=400&h=400&fit=crop&crop=face'
    WHEN name = 'Martin Scorsese' THEN 'https://images.unsplash.com/photo-1582750433449-648ed127bb54?w=400&h=400&fit=crop&crop=face'
    WHEN name = 'Greta Gerwig' THEN 'https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?w=400&h=400&fit=crop&crop=face'
    ELSE NULL
END
WHERE name IN (
    'Christopher Nolan', 'Quentin Tarantino', 'Steven Spielberg', 
    'Martin Scorsese', 'Greta Gerwig'
);

COMMIT;

-- Verification queries (optional - run these to verify the migration)
-- SELECT COUNT(*) as actors_with_images FROM actors WHERE image_url IS NOT NULL;
-- SELECT COUNT(*) as directors_with_images FROM directors WHERE image_url IS NOT NULL;
-- SELECT name, image_url FROM actors WHERE image_url IS NOT NULL LIMIT 5;
-- SELECT name, image_url FROM directors WHERE image_url IS NOT NULL LIMIT 5;