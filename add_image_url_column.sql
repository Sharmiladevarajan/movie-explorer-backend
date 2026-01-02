-- Add image_url column to movies table
ALTER TABLE movies ADD COLUMN IF NOT EXISTS image_url VARCHAR(500);

-- Add comment to document the column
COMMENT ON COLUMN movies.image_url IS 'URL to the movie poster/cover image';
