# Read books

## Sovelluksen toiminnot

  * Sovelluksessa käyttäjät pystyvät tallentamaan lukemansa kirjat. Kirjan yhteydessä lukee kirjan nimi, kirjoittaja ja julkaisuvuosi sekä kuvaus kirjasta.
  * Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
  * Käyttäjä pystyy lisäämään lukemiaan kirjoja ja muokkaamaan ja poistamaan niitä.
  * Käyttäjä näkee sovellukseen lisätyt kirjat.
  * Käyttäjä pystyy etsimään kirjoja hakusanalla, esim. kirjan nimellä, kirjailijan nimellä tai sanalla, joka löytyy kirjan kuvauksesta.
  * Käyttäjäsivu näyttää, montako kirjaa käyttäjä on lukenut - eroteltuna vuosittain - ja listan käyttäjän lisäämistä kirjoista.
  * Käyttäjä pystyy valitsemaan kirjalle kirjallisuuslajin/genren (esim. kaunokirjallisuus, dekkari, skifi)
  * Käyttäjät pystyvät keskustelemaan kirjasta kommenttiosiossa. Kirjasta annetut kommentit on koottu yhteen.
  * Käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään kommentteja.
  * Käyttäjä pystyy tarkastelemaan toisen käyttäjän käyttäjäsivua.
  * Käyttäjä voi lisätä profiilikuvan käyttäjäsivulleen.

## Sovelluksen asennus

Luo virtuaaliympäristö:
```
$ python3 -m venv venv
```

Aktivoi virtuaaliympäristö:

```
$ source venv/bin/activate
```

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut ja lisää alkutiedot:

```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql

```

Voit käynnistää sovelluksen näin:

```
$ flask run
```

## Sovelluksen käyttö suurella tietomäärällä

Ajamalla seuraavan koodin voit testata sovelluksen toimivuutta suurella tietomäärällä:
```
$ python3 seed.py
```
Tiedosto lisää 1000 käyttäjää, 100 000 kirjaa ja 1 000 000 kommenttia satunnaisilla sisällöillä tietokantaan. 

Sovellus toimii tehokkaasti ilman viivästyksiä tai sivun latauksen hitautta myös suuren tietomäärän kanssa seuraavista syistä:
- Käyttäjien lisäämät kirjat on sivutettu niin, että yhdellä sivulla näkyy korkeintaan 10 kirjaa.
- Kirjaan liittyvät kommentit on sivutettu niin, että yhdellä sivulla näkyy korkeintaan 5 kommenttia.
- Haku-sivulla tulokset on sivutettu niin, että yhdellä sivulla näkyy korkeintaan 5 tulosta.
- Käyttäjäsivulla käyttäjän lukemat kirjat on sivutettu niin, että yhdellä sivulla näkyy korkeintaan 10 kirjaa.
- Lisäksi tietokantaan on lisätty kyselyjä tehostavia indeksejä:
  
```
CREATE INDEX idx_books_user_id ON books(user_id);
CREATE INDEX idx_comments_user_id ON comments(user_id);
CREATE INDEX idx_comments_book_id ON comments(book_id);
CREATE INDEX idx_book_classes_book_id ON book_classes(book_id);
```
Nämä indeksit auttavat kyselyjä löytämään halutut rivit tietokantatauluista. Esimerkiksi ensimmäisellä indeksillä, joka liittyy tauluun `books` voidaan tehokkaasti löytää kirjat, jotka kuuluvat tietyllä käyttäjälle.   
