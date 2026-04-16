CREATE TABLE users (
	id INTEGER PRIMARY KEY, 
	username TEXT UNIQUE,
	password_hash TEXT
    image BLOB
);

CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    book_name TEXT,
    writer_name TEXT,
    pub_year INTEGER,
    description TEXT,
    user_id INTEGER REFERENCES users,
    read_year INTEGER
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    book_id INTEGER REFERENCES books,
    user_id INTEGER REFERENCES users,
    content TEXT,
    sent_at TEXT
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

