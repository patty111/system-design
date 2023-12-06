CREATE TABLE urls (
    short_url TEXT PRIMARY KEY,
    long_url TEXT NOT NULL,
    redirects INTEGER DEFAULT 0,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    expire_time DATETIME,
    is_active BOOLEAN DEFAULT 1
);