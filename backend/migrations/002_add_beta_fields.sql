-- Migration: Add beta user fields
-- Date: 2024-01-10

-- Add beta user fields to users table
ALTER TABLE users 
ADD COLUMN is_beta_user BOOLEAN DEFAULT FALSE,
ADD COLUMN beta_company VARCHAR(255),
ADD COLUMN beta_role VARCHAR(255);

-- Create index for beta users
CREATE INDEX idx_users_beta ON users(is_beta_user) WHERE is_beta_user = TRUE; 