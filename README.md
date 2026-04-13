# Read books

## Sovelluksen toiminnot

  * Sovelluksessa käyttäjät pystyvät tallentamaan lukemansa kirjat. Kirjan yhteydessä lukee kirjan nimi, kirjoittaja ja julkaisuvuosi sekä kuvaus kirjasta.
  * Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
  * Käyttäjä pystyy lisäämään lukemiaan kirjoja ja muokkaamaan ja poistamaan niitä.
  * Käyttäjä näkee sovellukseen lisätyt kirjat.
  * Käyttäjä pystyy etsimään kirjoja hakusanalla, esim. kirjan nimellä, kirjailijan nimellä tai sanalla, joka löytyy kirjan kuvauksesta.
  * Käyttäjäsivu näyttää, montako kirjaa käyttäjä on lukenut ja listan käyttäjän lisäämistä kirjoista.
  * Käyttäjä pystyy valitsemaan kirjalle kirjallisuuslajin/genren (esim. kaunokirjallisuus, dekkari, skifi)
  * Käyttäjät pystyvät keskustelemaan kirjasta kommenttiosiossa. Kirjasta annetut kommentit on koottu yhteen.
  * Käyttäjä pystyy tarkastelemaan toisen käyttäjän käyttäjäsivua.

## Sovelluksen asennus

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

    
