CREATE TABLE links (
    short_url TEXT PRIMARY KEY,
    long_url TEXT NOT NULL,
    redirects INTEGER DEFAULT 0,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    expire_time DATETIME,
    created_by VARCHAR(50) DEFAULT NULL,
    is_active BOOLEAN DEFAULT TRUE
);

-- CREATE TABLE user (
--     user_name VARCHAR(30) PRIMARY KEY
-- );