CREATE TABLE links (
    short_url TEXT PRIMARY KEY,
    long_url TEXT NOT NULL,
    redirects INTEGER DEFAULT 0,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    expire_time DATETIME,
    created_by VARCHAR(50) DEFAULT NULL,
    is_active BOOLEAN DEFAULT TRUE
    -- FOREIGN KEY(created_by) REFERENCES users(user_name)
);

-- CREATE INDEX idx_links_long_url ON links (long_url);

-- CREATE TABLE user (
--     user_name VARCHAR(30) PRIMARY KEY,
--     password VARCHAR(100) NOT NULL
-- );

-- CREATE TABLE UserTokens (
--     token TEXT PRIMARY KEY,
--     user_name TEXT Not Null,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     expires_at TIMESTAMP Not Null,
--     FOREIGN KEY(user_name) REFERENCES Users(user_name)
-- );