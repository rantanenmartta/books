import db

def add_item(book_name, writer_name, pub_year, description, user_id):
    sql = """INSERT INTO books (book_name, writer_name, pub_year, description, user_id)
             VALUES (?, ?, ?, ?, ?)"""

    try:
        db.execute(sql, [book_name, writer_name, pub_year, description, user_id])
    except Exception as e:
       print("DB Error:", e)
       return "Database error", 400
