CREATE TABLE links (
    short_url TEXT PRIMARY KEY,
    long_url TEXT NOT NULL,
    redirects INTEGER DEFAULT 0,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    expire_time DATETIME,
    created_by VARCHAR(50) DEFAULT NULL,
    last_redirect DATETIME DEFAULT NULL,
    is_active BOOLEAN DEFAULT TRUE
    FOREIGN KEY(created_by) REFERENCES users(username)
);

CREATE INDEX idx_links_long_url ON links (long_url);

CREATE TABLE users (
    username VARCHAR(50) PRIMARY KEY,
    password_hash VARCHAR(32) NOT NULL,
    salt VARCHAR(20) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- CREATE TABLE Tokens (
--     token TEXT PRIMARY KEY,
--     user TEXT Not Null,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     expires_at TIMESTAMP Not Null,
--     FOREIGN KEY(user) REFERENCES users(username)
-- );