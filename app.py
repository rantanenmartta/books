import secrets
import sqlite3
import re
from flask import Flask
from flask import abort, redirect, render_template, request, session, make_response
import config
import items
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/")
def index():
    all_items = items.get_items()
    return render_template("index.html", items=all_items)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    items = users.get_items(user_id)
    return render_template("show_user.html", user=user, items=items)

@app.route("/find_item")
def find_item():
    query = request.args.get("query")
    if query:
        results = items.find_items(query)
    else:
        query = ""
        results = []
    return render_template("find_item.html", query=query, results=results)

@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    classes = items.get_classes(item_id)
    comments = items.get_comments(item_id)
    return render_template("show_item.html", item=item, classes=classes, comments=comments)

@app.route("/new_item")
def new_item():
    require_login()
    classes = items.get_all_classes()

    return render_template("new_item.html", classes=classes)

@app.route("/create_item", methods=["POST"])
def create_item():
    require_login()
    check_csrf()

    book_name = request.form["book_name"]
    if not book_name or len(book_name) > 50:
        abort(403)
    writer_name = request.form["writer_name"]
    if not writer_name or len(writer_name) > 50:
        abort(403)
    pub_year = request.form["pub_year"]

    if not re.search("^[1-9][0-9]{0,4}$", pub_year):
        abort(403)
    description = request.form.get("description", "")
    if not description or len(description) > 1500:
        abort(403)

    user_id = session["user_id"]

    all_classes = items.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))

    items.add_item(book_name, writer_name, pub_year, description, user_id, classes)

    return redirect("/")

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()
    item = items.get_item(item_id)
    books = items.get_items()
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    all_classes = items.get_all_classes()

    classes = {}
    for my_class in all_classes:
        classes[my_class] = ""
    for entry in items.get_classes(item_id):
        classes[entry["title"]] = entry["value"]

    return render_template("edit_item.html", item=item, books=books, classes=classes, all_classes=all_classes)

@app.route("/update_item", methods=["POST"])
def update_item():
    require_login()
    check_csrf()

    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    book_name = request.form["book_name"]
    if not book_name or len(book_name) > 50:
        abort(403)
    writer_name = request.form["writer_name"]
    if not writer_name or len(writer_name) > 50:
        abort(403)
    pub_year = request.form["pub_year"]
    if not re.search("^[1-9][0-9]{0,4}$", pub_year):
        abort(403)
    description = request.form.get("description", "")
    if not description or len(description) > 1500:
        abort(403)

    all_classes = items.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            title, value = entry.split(":")
            if title not in all_classes:
                abort(403)
            if value not in all_classes[title]:
                abort(403)
            classes.append((title, value))

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))

    items.update_item(item_id, book_name, writer_name, pub_year, description, classes)

    return redirect("/item/" + str(item_id))

@app.route("/remove_item/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    require_login()

    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    if request.method == "GET":
        item = items.get_item(item_id)
        return render_template("remove_item.html", item=item)

    elif request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))

@app.route("/create_comment", methods=["POST"])
def create_comment():
    require_login()

    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(403)
    user_id = session["user_id"]
    content = request.form.get("content", "")

    items.add_comment(item_id, user_id, content)

    return redirect("/item/" + str(item_id))

@app.route("/edit_comment/<int:comment_id>", methods=["GET"])
def edit_comment(comment_id):
    require_login()

    comment_all = items.get_comment(comment_id)
    if not comment_all:
        abort(404)
    comment = comment_all[0]
    if comment["user_id"] != session["user_id"]:
        abort(403)
    item = items.get_item(comment["book_id"])
    return render_template("edit_comment.html", item=item, comment=comment)

@app.route("/update_comment", methods=["POST"])
def update_comment():
    require_login()
    check_csrf()

    comment_id = request.form["comment_id"]
    item_id = request.form["item_id"]

    comment_all = items.get_comment(comment_id)
    if not comment_all:
        abort(404)
    comment = comment_all[0]

    if comment["user_id"] != session["user_id"]:
        abort(403)

    content = request.form.get("content", "")
    if not content or len(content) > 3000:
        abort(403)

    items.update_comment(comment_id, content)

    return redirect("/item/" + str(item_id))

@app.route("/remove_comment/<int:comment_id>", methods=["GET", "POST"])
def remove_comment(comment_id):
    require_login()

    comment_all = items.get_comment(comment_id)

    if not comment_all:
        abort(404)
    comment = comment_all[0]
    item_id = comment["book_id"]

    if comment["user_id"] != session["user_id"]:
        abort(403)
    if request.method == "GET":
        comment_all = items.get_comment(comment_id)
        comment = comment_all[0]

        return render_template("remove_comment.html", comment=comment)

    elif request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            items.remove_comment(comment_id)
            return redirect("/item/" + str(item_id))
        return redirect("/item/" + str(item_id))

@app.route("/add_image", methods=["GET", "POST"])
def add_image():
    require_login()

    if request.method == "GET":
        return render_template("add_image.html")
    elif request.method == "POST":
        check_csrf()
        file = request.files["image"]
        if not file.filename.endswith(".jpg"):
            return "VIRHE: väärä tiedostomuoto"

        image = file.read()
        if len(image) > 100 * 1024:
            return "VIRHE: liian suuri kuva"

        user_id = session["user_id"]
        users.update_image(user_id, image)
        return redirect("/user/" + str(user_id))

@app.route("/image/<int:user_id>")
def show_image(user_id):
    image = users.get_image(user_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "VIRHE: Tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"]= user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")
