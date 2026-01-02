-- Add image_url column to actors table
-- Migration: Add image support for actors

ALTER TABLE actors 
ADD COLUMN IF NOT EXISTS image_url TEXT;

-- Add comment for documentation
COMMENT ON COLUMN actors.image_url IS 'URL to actor profile image or photo';

-- Create index for better performance when filtering by image presence
CREATE INDEX IF NOT EXISTS idx_actors_has_image ON actors(image_url) WHERE image_url IS NOT NULL;

-- Update sample actors with image URLs (using placeholder images)
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