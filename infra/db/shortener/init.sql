CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE short_urls (
    slug VARCHAR(12) PRIMARY KEY,
    origin VARCHAR(400),
    created_at TIMESTAMP DEFAULT NOW(),
    author_id INT REFERENCES users(id)
);