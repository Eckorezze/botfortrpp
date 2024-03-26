CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    user_name VARCHAR(255),
    user_username VARCHAR(255),
    language VARCHAR(255)
);

CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    note TEXT,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
