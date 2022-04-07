from . import app
from flask import render_template, request, redirect, url_for, session, flash
import functools
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

dbfile="databaze.sqlite"
con=sqlite3.connect("databaze.sqlite", isolation_level=None)

# from werkzeug.security import check_password_hash

slova = ("Super", "Perfekt", "Úža", "Flask")


def prihlasit(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if "user" in session:
            return function(*args, **kwargs)
        else:
            return redirect(url_for("login", url=request.path))

    return wrapper


@app.route("/", methods=["GET"])
def index():
    return render_template("base.html.j2")


@app.route("/login/")
def login():
    return render_template("login.html.j2")

@app.route("/login/", methods=['POST'])
def login_post():
    nick=request.form.get('nick')
    passwd=request.form.get('passwd1')
    if nick and passwd:
        with sqlite3.connect(dbfile) as con:
            tabulka=list(con.execute("SELECT passwd FROM uzivatel WHERE nick=?",[nick]))
        if tabulka and check_password_hash(tabulka[0][0], passwd):
            flash("Anoo")
        else:
            flash("Nee")
    return redirect(url_for("index"))


@app.route("/registrate/")
def registrate():
    return render_template("registrate.html.j2", slova=slova)

@app.route("/registrate/", methods=["POST"])
def registrate_post():
    nick=request.form.get('nick')
    print(nick)
    passwd1=request.form.get('passwd1')
    passwd2=request.form.get('passwd2')
    if nick and passwd1 and passwd1==passwd2:
        hashpasswd=generate_password_hash('passwd1')
        with sqlite3.connect(dbfile) as con:
            try:
                con.execute('INSERT INTO uzivatel (nick,passwd) VALUES(?,?)',[nick, hashpasswd])
                flash("Uživatel vytvořen")
            except sqlite3.IntegrityError:
                flash("Uživatel již existuje!")
    else:
        flash("Chyba, zkus to znovu :( ")
        return redirect(url_for("registrate"))
    return redirect(url_for("index"))

@app.route("/text/")
def text():
    return """

<h1>Text</h1>

<p>toto je text</p>

"""
