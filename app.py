import secrets
import sqlite3
import math
import re
from flask import Flask
from flask import abort, flash, redirect, render_template, request, session, make_response
import markupsafe
import config
import items
import users
#import db

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

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.route("/")
@app.route("/<int:page>")
def index(page=1):
    page_size = 10
    book_count = items.book_count()
    page_count = math.ceil(book_count / page_size)
    page_count = max(page_count, 1)
    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect("/" + str(page_count))

    all_items = items.get_items(page, page_size)
    return render_template("index.html", page=page, page_count=page_count, items=all_items)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    user_items = users.get_items(user_id)
    year_counts = items.books_grouped_by_year(user_id)
    return render_template("show_user.html", user=user, items=user_items, year_counts=year_counts)

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

    page = request.args.get("page", 1, type=int)
    page = max(page, 1)
    page_size = 5

    classes = items.get_classes(item_id)
    total = items.comment_count(item_id)

    page_count = max((total + page_size - 1) // page_size, 1)

    page = min(page, page_count)

    comments = items.get_comments(item_id, page, page_size)

    return render_template("show_item.html", item=item, classes=classes,
                    comments=comments, page=page, page_count=page_count)

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

    read_year = request.form["read_year"]
    if not read_year or int(read_year) < 1900 or int(read_year) > 2100:
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

    item_id = items.add_item(book_name, writer_name, pub_year,
                            description, user_id, read_year, classes)

    return redirect("/item/" + str(item_id))

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()
    item = items.get_item(item_id)
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

    return render_template("edit_item.html", item=item,
                            classes=classes, all_classes=all_classes)

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
    read_year = request.form["read_year"]
    if not read_year or int(read_year) < 1900 or int(read_year) > 2100:
        abort(403)

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

    items.update_item(item_id, book_name, writer_name, pub_year, description, read_year, classes)

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
        check_csrf()
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        return redirect("/item/" + str(item_id))

@app.route("/create_comment", methods=["POST"])
def create_comment():
    require_login()
    check_csrf()

    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(403)
    user_id = session["user_id"]
    content = request.form.get("content", "")

    if not content or len(content) > 1500:
        abort(403)
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
    if not content or len(content) > 1500:
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
        item = items.get_item(comment["book_id"])

        return render_template("remove_comment.html", comment=comment, item=item)

    if request.method == "POST":
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
    if request.method == "POST":
        check_csrf()
        file = request.files["image"]
        user_id = session["user_id"]
        if not file.filename.endswith(".jpg"):
            flash("VIRHE: väärä tiedostomuoto")
            return redirect("/user/" + str(user_id))

        image = file.read()
        if len(image) > 100 * 1024:
            flash("VIRHE: liian suuri kuva")
            return redirect("/user/" + str(user_id))

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

@app.route("/remove_image", methods=["POST"])
def remove_image():
    require_login()
    check_csrf()

    user_id = session["user_id"]
    if "remove" in request.form:
        items.remove_image(user_id)
        flash("Profiilikuva poistettu")
    return redirect("/user/" + str(user_id))

@app.route("/register")
def register():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)
    return render_template("register.html")
@app.route("/create", methods=["POST"])
def create():
    check_csrf()

    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if not username or len(username) > 30:
        flash("VIRHE: liian pitkä käyttäjänimi")
        return redirect("/register")
    if not password1 or len(password1) < 4 or len(password1) > 30:
        flash("VIRHE: liian lyhyt/pitkä salasana")

    if password1 != password2:
        flash("VIRHE: salasanat eivät ole samat")
        return redirect("/register")

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu")
        return redirect("/register")

    session["csrf_token"] = secrets.token_hex(16)

    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if "csrf_token" not in session:
            session["csrf_token"] = secrets.token_hex(16)
        return render_template("login.html")

    if request.method == "POST":
        check_csrf()
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"]= user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("VIRHE: väärä tunnus tai salasana")
            return redirect("/login")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")
