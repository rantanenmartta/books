import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db
import items
import re
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
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

    if request.method == "POST":
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
    print("Content:", content)

    items.add_comment(item_id, user_id, content)

    return redirect("/item/" + str(item_id))


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
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")

