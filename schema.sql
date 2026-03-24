CREATE TABLE users (
	id INTEGER PRIMARY KEY, 
	username TEXT UNIQUE,
	password_hash TEXT
)

CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    book_name TEXT,
    writer_name TEXT,    --change to references writers, use id here
    pub_year INTEGER,
    description TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE book_classes (
    id INTEGER PRIMARY KEY,
    book_id INTEGER REFERENCES books,
    title TEXT,
    value TEXT
);

