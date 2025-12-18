-- Drop tables if they exist to ensure clean slate
DROP TABLE IF EXISTS translations CASCADE;
DROP TABLE IF EXISTS content_items CASCADE;
DROP TABLE IF EXISTS pages CASCADE;
DROP TABLE IF EXISTS settings CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Create Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    modified_by BIGINT,
    modified_at TIMESTAMP
);

-- Create Settings table
CREATE TABLE settings (
    id BIGSERIAL PRIMARY KEY,
    hash TEXT NOT NULL,
    added_by BIGINT REFERENCES users(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    modified_by BIGINT REFERENCES users(id),
    modified_at TIMESTAMP
);

-- Create Pages table
CREATE TABLE pages (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    added_by BIGINT REFERENCES users(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    modified_by BIGINT REFERENCES users(id),
    modified_at TIMESTAMP
);

-- Create ContentItem table
CREATE TABLE content_items (
    id BIGSERIAL PRIMARY KEY,
    page_id BIGINT REFERENCES pages(id),
    position INT NOT NULL,
    title VARCHAR(255),
    content TEXT,
    content_type VARCHAR(50) NOT NULL,
    added_by BIGINT REFERENCES users(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    modified_by BIGINT REFERENCES users(id),
    modified_at TIMESTAMP
);

-- Create Translations table
CREATE TABLE translations (
    id BIGSERIAL PRIMARY KEY,
    reference_key VARCHAR(255) NOT NULL,
    language VARCHAR(10) NOT NULL,
    text TEXT,
    added_by BIGINT REFERENCES users(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    modified_by BIGINT REFERENCES users(id),
    modified_at TIMESTAMP
);

-- Seed Users
INSERT INTO users (username, password_hash, role) VALUES
('admin', 'admin_hash_123', 'admin'),
('editor', 'editor_hash_456', 'editor'),
('viewer', 'viewer_hash_789', 'viewer');

-- Seed Settings
INSERT INTO settings (hash, added_by) VALUES
('site_title_hash', 1),
('theme_dark_hash', 1),
('maintenance_mode_hash', 1);

-- Seed Pages
INSERT INTO pages (name, added_by) VALUES
('Home', 1),
('About', 1),
('Contact', 1);

-- Seed ContentItems
INSERT INTO content_items (page_id, position, title, content, content_type, added_by) VALUES
(1, 1, 'Welcome', 'Welcome to our car service CMS.', 'text', 1),
(2, 1, 'Our Story', 'We started in 2020...', 'text', 2),
(3, 1, 'Contact Info', 'Email us at contact@carserv.com', 'contact_form', 1);

-- Seed Translations
INSERT INTO translations (reference_key, language, text, added_by) VALUES
('welcome_msg', 'en', 'Welcome', 1),
('welcome_msg', 'pl', 'Witamy', 1),
('contact_btn', 'en', 'Contact Us', 1);

-- Create Admin DB User (as requested previously)
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'admin') THEN

      CREATE ROLE admin LOGIN PASSWORD 'admin';
      ALTER ROLE admin WITH SUPERUSER;
   END IF;
END
$do$;
