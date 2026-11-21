"""Prosta aplikacja Flask: książki, logowanie i panel administratora.

Widoki:
    /            - lista książek (tylko dla zalogowanych), dodawanie książek
    /login       - logowanie
    /logout      - wylogowanie
    /users       - lista użytkowników + dodawanie (tylko admin)
    /user/<x>    - dane użytkownika wskazanego przez id lub nazwę (tylko admin)

Uruchomienie:  python app.py
Przy pierwszym uruchomieniu wejdź na http://127.0.0.1:5000/init_db - powstanie
baza z kontem  admin / admin. Potem przejdź na http://127.0.0.1:5000/
"""
import sqlite3
from functools import wraps

from flask import Flask, abort, g, redirect, render_template, request, session, url_for
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"  # sesje trzymane przez serwer w plikach
Session(app)
DATABASE = "database.db"


# ---------------------------------------------------------------- baza danych

def get_db():
    """Zwraca połączenie z bazą (jedno na zapytanie)."""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # wiersze działają jak słowniki
    return g.db


@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.route("/init_db")
def init_db():
    """Endpoint uruchamiany raz: tworzy tabele i konto administratora."""
    db = sqlite3.connect(DATABASE)
    db.execute(
        """CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT UNIQUE NOT NULL,
               password TEXT NOT NULL,
               is_admin INTEGER NOT NULL DEFAULT 0)"""
    )
    db.execute(
        """CREATE TABLE IF NOT EXISTS books (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               title TEXT NOT NULL,
               author TEXT NOT NULL)"""
    )
    if db.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        db.execute(
            "INSERT INTO users (name, password, is_admin) VALUES (?, ?, 1)",
            ("admin", "admin"),
        )
    db.commit()
    db.close()
    return 'Baza utworzona (konto admin / admin). <a href="/login">Zaloguj się</a>'


# ------------------------------------------------------- kontrola dostępu

def login_required(view):
    """Niezalogowanych przekierowuje na stronę logowania."""
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


def admin_required(view):
    """Wpuszcza tylko administratora (reszta dostaje 403)."""
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if not session["is_admin"]:
            abort(403)
        return view(*args, **kwargs)
    return wrapped


# ------------------------------------------------------------------- widoki

@app.route("/")
@login_required
def index():
    books = get_db().execute("SELECT * FROM books").fetchall()
    return render_template("index.html", books=books)


@app.route("/books", methods=["POST"])
@login_required
def add_book():
    title = request.form["title"].strip()
    author = request.form["author"].strip()
    if title and author:
        db = get_db()
        db.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
        db.commit()
    return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        user = get_db().execute("SELECT * FROM users WHERE name = ?", (name,)).fetchone()
        if user and user["password"] == password:
            session["user"] = user["name"]
            session["is_admin"] = bool(user["is_admin"])
            return redirect(url_for("index"))
        error = "Błędna nazwa użytkownika lub hasło"
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/users", methods=["GET", "POST"])
@admin_required
def users():
    db = get_db()
    error = None
    if request.method == "POST":
        name = request.form["name"].strip()
        password = request.form["password"]
        is_admin = 1 if "is_admin" in request.form else 0  # checkbox
        if not name or not password:
            error = "Podaj nazwę i hasło"
        elif db.execute("SELECT 1 FROM users WHERE name = ?", (name,)).fetchone():
            error = "Taki użytkownik już istnieje"
        else:
            db.execute(
                "INSERT INTO users (name, password, is_admin) VALUES (?, ?, ?)",
                (name, password, is_admin),
            )
            db.commit()
    all_users = db.execute("SELECT * FROM users").fetchall()
    return render_template("users.html", users=all_users, error=error)


@app.route("/user/<identifier>")
@admin_required
def user(identifier):
    """identifier to id (same cyfry) albo nazwa użytkownika."""
    db = get_db()
    if identifier.isdigit():
        found = db.execute("SELECT * FROM users WHERE id = ?", (identifier,)).fetchone()
    else:
        found = db.execute("SELECT * FROM users WHERE name = ?", (identifier,)).fetchone()
    if found is None:
        abort(404)
    return render_template("user.html", user=found)


if __name__ == "__main__":
    app.run(debug=True)
