import datetime
import db

def add_item(book_name, writer_name, pub_year, description, user_id, read_year, classes):
    sql = """INSERT INTO books (book_name, writer_name, pub_year, description, user_id, read_year)
            VALUES (?, ?, ?, ?, ?, ?)"""

    db.execute(sql, [book_name, writer_name, pub_year, description, user_id, read_year])

    item_id = db.last_insert_id()

    sql = "INSERT INTO book_classes (book_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [item_id, title, value])

    return item_id

def get_items(page, page_size):
    sql = """SELECT books.id, books.book_name, users.id user_id,
            users.username, COUNT(comments.id) com_count
            FROM books JOIN users ON books.user_id = users.id
            LEFT JOIN comments ON books.id = comments.book_id
            GROUP BY books.id
            ORDER BY books.id DESC
            LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)

    return db.query(sql, [limit, offset])

def get_item(item_id):
    sql = """SELECT b.id,
                    b.book_name,
                    b.writer_name,
                    b.pub_year,
                    b.description,
                    b.read_year,
                    u.id user_id,
                    u.username
            FROM books b, users u
            WHERE b.user_id = u.id AND b.id = ?"""
    result = db.query(sql, [item_id])
    return result[0] if result else None

def update_item(item_id, book_name, writer_name, pub_year, description, read_year, classes):
    sql = """UPDATE books SET book_name = ?,
                        writer_name = ?,
                        pub_year = ?,
                        description = ?,
                        read_year = ?
                        WHERE id = ?"""
    db.execute(sql, [book_name, writer_name, pub_year, description, read_year, item_id])

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

def find_items(query, page, page_size):
    sql = """SELECT b.id, b.book_name, u.username, u.id AS user_id
            FROM books b JOIN users u ON b.user_id = u.id
            WHERE b.book_name LIKE ? or b.writer_name LIKE ? 
            or b.pub_year LIKE ? or b.description LIKE ?
            or b.read_year LIKE ?
            ORDER BY b.id DESC
            LIMIT ? OFFSET ?"""
    like = "%" + query + "%"
    limit = page_size
    offset = page_size * (page - 1)

    return db.query(sql, [like, like, like, like, like, limit, offset])

def count_items(query):
    sql = """SELECT COUNT(*)
             FROM books b
             WHERE b.book_name LIKE ? or b.writer_name LIKE ?
             or b.pub_year LIKE ? or b.description LIKE ?
             or b.read_year LIKE ?"""
    like = "%" + query + "%"
    return db.query(sql, [like, like, like, like, like])[0][0]
def add_comment(book_id, user_id, content):
    sql = """INSERT INTO comments (book_id, user_id, content, sent_at)
            VALUES (?, ?, ?, datetime('now'))"""
    db.execute(sql, [book_id, user_id, content])

def get_comments(item_id, page, page_size):
    sql = """SELECT comments.id, comments.content, comments.book_id,
            comments.sent_at, users.id user_id, users.username
            FROM comments, users
            WHERE comments.book_id = ? AND comments.user_id = users.id
            ORDER BY comments.id DESC
            LIMIT ? OFFSET ? """
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [item_id, limit, offset])

def get_comment(comment_id):
    sql = """SELECT comments.id, comments.content, comments.book_id,
            comments.sent_at, comments.user_id, users.id user_id, users.username
            FROM comments, users
            WHERE comments.id = ? and comments.user_id = users.id"""
    return db.query(sql, [comment_id])

def update_comment(comment_id, content):
    sql = "UPDATE comments SET content = ? WHERE id = ?"
    db.execute(sql, [content, comment_id])

def remove_comment(comment_id):
    sql = "DELETE FROM comments WHERE id = ?"
    db.execute(sql, [comment_id])

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)

    return classes

def get_classes(item_id):
    sql = "SELECT title, value FROM book_classes WHERE book_id = ?"
    return db.query(sql, [item_id])

def remove_image(user_id):
    sql = "UPDATE users SET IMAGE = NULL WHERE id = ?"
    db.execute(sql, [user_id])

def book_count():
    sql = "SELECT COUNT(*) FROM books"
    return db.query(sql)[0][0]

def comment_count(item_id):
    sql = "SELECT IFNULL(COUNT(*),0) FROM comments WHERE book_id = ?"
    return db.query(sql, [item_id])[0][0]

def count_books_by_year(user_id, year):
    sql = "SELECT COUNT(*) FROM books WHERE user_id = ? AND read_year = ?"
    return db.query(sql, [user_id, year])[0][0]

def books_grouped_by_year(user_id):
    current_year = datetime.date.today().year
    start_year = current_year - 9
    sql = """SELECT read_year, COUNT(*) AS count
            FROM books
            WHERE user_id = ? AND read_year IS NOT NULL
            AND read_year >= ?
            GROUP BY read_year
            ORDER BY read_year DESC"""
    return db.query(sql, [user_id, start_year])
