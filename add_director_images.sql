-- Add image_url column to directors table
-- Migration: Add image support for directors

ALTER TABLE directors 
ADD COLUMN IF NOT EXISTS image_url TEXT;

-- Add comment for documentation
COMMENT ON COLUMN directors.image_url IS 'URL to director profile image or photo';

-- Create index for better performance when filtering by image presence
CREATE INDEX IF NOT EXISTS idx_directors_has_image ON directors(image_url) WHERE image_url IS NOT NULL;

-- Update sample directors with image URLs (using placeholder images)
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