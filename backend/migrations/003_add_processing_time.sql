-- Migration: Add processing_time column to analyses table
-- Date: 2025-01-13

-- Add processing_time column if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'analyses' 
        AND column_name = 'processing_time'
    ) THEN
        ALTER TABLE analyses ADD COLUMN processing_time FLOAT;
    END IF;
END $$; 