CREATE TABLE short_urls (
    slug VARCHAR(12) PRIMARY KEY,
    origin VARCHAR(400),
    created_at TIMESTAMP DEFAULT NOW()
);