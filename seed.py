import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM books")
db.execute("DELETE FROM comments")

user_count = 1000
book_count = 10**5
comment_count = 10**6

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])

for i in range(1, book_count + 1):
    pub_year = random.randint(1900, 2026)
    read_year = random.randint(1950, 2026)
    user_id = random.randint(1, user_count)
    db.execute("""INSERT INTO books (book_name, writer_name, pub_year, description, user_id, read_year) VALUES (?, ?, ?, ?, ?, ?)""",
               ["thread" + str(i), "writer" + str(i), pub_year, "description" + str(i), user_id, read_year])

for i in range(1, comment_count + 1):
    user_id = random.randint(1, user_count)
    book_id = random.randint(1, book_count)
    db.execute("""INSERT INTO comments (content, sent_at, user_id, book_id)
                  VALUES (?, datetime('now'), ?, ?)""",
               ["comment" + str(i), user_id, book_id])

db.commit()
db.close()
