import db

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)

    return classes

def add_item(book_name, writer_name, pub_year, description, user_id, classes):
    sql = """INSERT INTO books (book_name, writer_name, pub_year, description, user_id)
             VALUES (?, ?, ?, ?, ?)"""
    try:
        db.execute(sql, [book_name, writer_name, pub_year, description, user_id])
    except Exception as e:
        print("DB Error:", e)
        return "Database error", 400

    item_id = db.last_insert_id()

    sql = "INSERT INTO book_classes (book_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [item_id, title, value])

def add_comment(book_id, user_id, content):
    sql = """INSERT INTO comments (book_id, user_id, content, sent_at) VALUES
            (?, ?, ?, datetime('now'))"""
    db.execute(sql, [book_id, user_id, content])

def get_comments(item_id):
    sql = """SELECT comments.id, comments.content, comments.book_id,
            comments.sent_at, users.id user_id, users.username
            FROM comments, users
            WHERE comments.book_id = ? AND comments.user_id = users.id
            ORDER BY comments.id DESC"""
    return db.query(sql, [item_id])

def get_items():
    sql = """SELECT books.id, books.book_name, users.id user_id, users.username, COUNT(comments.id) com_count
             FROM books JOIN users ON books.user_id = users.id
                        LEFT JOIN comments ON books.id = comments.book_id
             GROUP BY books.id
             ORDER BY books.id DESC"""

    return db.query(sql)

def get_item(item_id):
    sql = """SELECT b.id,
                    b.book_name,
                    b.writer_name,
                    b.pub_year,
                    b.description,
                    u.id user_id,
                    u.username
            FROM books b, users u
            WHERE b.user_id = u.id AND
                b.id = ?"""
    result = db.query(sql, [item_id])
    return result[0] if result else None

def update_item(item_id, book_name, writer_name, pub_year, description, classes):
    sql = """UPDATE books SET book_name = ?,
                            writer_name = ?,
                            pub_year = ?,
                            description = ?
                        WHERE id = ?"""
    db.execute(sql, [book_name, writer_name, pub_year, description, item_id])

    sql = "DELETE FROM book_classes WHERE book_id = ?"
    db.execute(sql, [item_id])

    sql = "INSERT INTO book_classes (book_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [item_id, title, value])

def remove_item(item_id):
    sql = "DELETE FROM comments WHERE book_id = ?"
    db.execute(sql, [item_id])

    sql = "DELETE FROM book_classes WHERE book_id = ?"
    db.execute(sql, [item_id])

    sql = "DELETE FROM books WHERE id = ?"
    db.execute(sql, [item_id])


def find_items(query):
    sql = """SELECT id, book_name
             FROM books
             WHERE book_name LIKE ? or writer_name LIKE ? or pub_year LIKE ? or description LIKE ?
             ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like, like, like])


def update_comment(comment_id, content):
    sql = "UPDATE comments SET content = ? WHERE id = ?"
    db.execute(sql, [content, comment_id])

def get_comment(comment_id):
    sql = """SELECT comments.id, comments.content, comments.book_id, 
            comments.sent_at, comments.user_id, users.id user_id, users.username
            FROM comments, users
            WHERE comments.id = ? and comments.user_id = users.id"""
    return db.query(sql, [comment_id])

def remove_comment(comment_id):
    sql = "DELETE FROM comments WHERE id = ?"
    db.execute(sql, [comment_id])

def get_classes(item_id):
    sql = "SELECT title, value FROM book_classes WHERE book_id = ?"
    return db.query(sql, [item_id])
