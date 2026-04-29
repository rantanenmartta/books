Pylintin antama raportti sovelluksesta:

```
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:15:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:26:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:33:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:47:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:56:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:66:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:88:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:95:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:136:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:155:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:199:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:199:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:220:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:238:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:251:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:275:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:275:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:302:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:302:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:324:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:334:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:345:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:351:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:379:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:391:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
app.py:379:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:401:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module config
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:17:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
************* Module items
items.py:1:0: C0114: Missing module docstring (missing-module-docstring)
items.py:3:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:3:0: R0913: Too many arguments (7/5) (too-many-arguments)
items.py:17:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:30:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:44:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:44:0: R0913: Too many arguments (7/5) (too-many-arguments)
items.py:60:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:70:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:80:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:85:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:96:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:103:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:107:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:111:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:123:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:127:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:131:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:135:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:139:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:143:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module users
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:11:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:15:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:32:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:36:0: C0116: Missing function or method docstring (missing-function-docstring)

------------------------------------------------------------------
Your code has been rated at 8.50/10 (previous run: 8.50/10, +0.00)

```

Alla on käyty läpi erilaiset pylint-raportin antamat ilmoitukset ja syyt, miksi kyseistä asiaa ei ole korjattu koodissa.
Huom! Pylint-raportissa ei ole huomioitu seed.py -tiedoston huomautuksia.

# Docstring -ilmoitukset

Suurin osa ilmoituksista on huomautuksia, että funktioista puuttuu docstring-kommentit. Kurssien ohjeiden mukaisesti on päätetty jättää lisäämättä docstring-kommentit.
```
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:15:0: C0116: Missing function or method docstring (missing-function-docstring)
```

# Puuttuvat palautusarvot

Muutamia kommentteja tulee siitä, kuinka funktio saattaa olla palauttamatta arvoa:
```
app.py:199:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-r
```
Jokainen näistä kommenttien tilanteista liittyy kuitenkin funktioihin, joissa funktio käsittelee metodit `GET` ja `POST` mutta ei muita metodeja.
Esimerkiksi `remove_item()`-funktiossa:

```
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
```
Funktio palauttaa arvon, kun request.method on `GET` tai `POST`. Funktion dekoraattori vaatii, että funktion metodi on joko
`GET` tai `POST`, joten ei todellisuudessa ole riskiä, että funktio ei menisi `if`-haaraan ja palauttaisi mitään arvoa.


# Turha else-haara

Raportissa on yksi ilmoitus ylimääräisestä `else`-haarasta:

```
app.py:391:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
```
Kyseessä on `login()`-funktion koodi:
```
if user_id:
            session["user_id"]= user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
else:
            flash("VIRHE: väärä tunnus tai salasana")
            return redirect("/login")
```
Tämän voisi kirjoittaa tiiviimmin seuraavalla tavalla:
```
if user_id:
            session["user_id"]= user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
flash("VIRHE: väärä tunnus tai salasana")
return redirect("/login")
```
Kuitenkin selkeyden vuoksi olen käyttänyt `else`-haaraa, jotta koodista käy selkeämmin esiin eri tilanteet.


# Vaarallinen oletusarvo
Modulissa db.py on kaksi huomautusta vaarallisista oletusarvoista:
```
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
```
Tämä rivi viittaa seuraavaan funktioon, jossa parametrin oletusarvona on tyhjä lista:
```
def execute(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()
```
Tyhjä lista oletusarvona voisi olla ongelma, jossa tyhjä listaolio on jaettu kaikkien funktion kutsujen kesken ja jos jossakin kutsussa listan sisältöä muutettaisiin. Tällöin muutos vaikuttaisi myös muihin kutsuihin. Koodi ei kuitenkaan muuta listaoliota, joten tälläistä tilannetta ei synny.

# Liian monta muuttujaa

Items.py -modulissa on on pari huomautusta, että SQL-komennolle annetaan liian monta muuttujaa.
```
items.py:3:0: R0913: Too many arguments (7/5) (too-many-arguments)
```
Esim.
```
def add_item(book_name, writer_name, pub_year, description, user_id, read_year, classes):
    sql = """INSERT INTO books (book_name, writer_name, pub_year, description, user_id, read_year)
            VALUES (?, ?, ?, ?, ?, ?)"""

    db.execute(sql, [book_name, writer_name, pub_year, description, user_id, read_year])
```
Kuitenkin, jotta sovellus toimii halutulla tavalla, tarvitaan jokaista muuttujaa. Näin ollen muutoksia ei ole tehty ja huomautuksesta huolimatta funktio toimii oikein. Olisi voinut huomioida sovelluksen kehittämisen alussa ja luoda vähemmän muuttujia, jos olisi halunnut välttää kyseisen tilanteen.
