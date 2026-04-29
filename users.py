from werkzeug.security import check_password_hash, generate_password_hash
import db

def get_user(user_id):
    sql = """SELECT id, username, image IS NOT NULL has_image
            FROM users
            WHERE id = ?"""
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_items(user_id, page, page_size):
    sql = "SELECT id, book_name FROM books WHERE user_id = ? ORDER BY id DESC LIMIT ? OFFSET ?"
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [user_id, limit, offset])

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None
    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]

    if check_password_hash(password_hash, password):
        return user_id
    return None

def update_image(user_id, image):
    sql = "UPDATE users SET image = ? WHERE id = ?"
    db.execute(sql, [image, user_id])

def get_image(user_id):
    sql = "SELECT image FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0][0] if result else None

def count_books_user(user_id):
    sql = "SELECT COUNT(*) FROM books WHERE user_id = ?"
    return db.query(sql, [user_id])[0][0]
