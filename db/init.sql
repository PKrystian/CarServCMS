CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);

INSERT INTO users (username, email, is_active) VALUES
('alice', 'alice@example.com', true),
('bob', 'bob@example.com', true),
('charlie', 'charlie@example.com', false)
ON CONFLICT (username) DO NOTHING;
