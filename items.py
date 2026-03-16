import db

def add_item(book_name, writer_name, pub_year, description, user_id):
    sql = """INSERT INTO books (book_name, writer_name, pub_year, description, user_id)
             VALUES (?, ?, ?, ?, ?)"""

    try:
        db.execute(sql, [book_name, writer_name, pub_year, description, user_id])
    except Exception as e:
       print("DB Error:", e)
       return "Database error", 400

def get_items():
    sql = "SELECT id, book_name FROM books ORDER BY id DESC"

    return db.query(sql)

def get_item(item_id):
    sql = """SELECT b.book_name,
                    b.writer_name,
                    b.pub_year,
                    b.description,
                    u.username
             FROM books b, users u
             WHERE b.user_id = u.id AND
                   b.id = ?"""
    return db.query(sql, [item_id])[0]
