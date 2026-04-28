CREATE TABLE users (
    id INTEGER PRIMARY KEY, 
    username TEXT UNIQUE,
    password_hash TEXT,
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

CREATE INDEX idx_books_user_id ON books(user_id);
CREATE INDEX idx_comments_user_id ON comments(user_id);
CREATE INDEX idx_comments_book_id ON comments(book_id);
CREATE INDEX idx_book_classes_book_id ON book_classes(book_id);

