from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "my_secret_key_123"

DATABASE = "notes.db"


# ---------------- DATABASE ----------------

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


# ---------------- LOGIN ----------------

@app.route("/", methods=["GET", "POST"])
def login():

    if "user_id" in session:
        return redirect(url_for("home"))

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect(url_for("home"))

        flash("Invalid email or password.", "error")

    return render_template("login.html")


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if "user_id" in session:
        return redirect(url_for("home"))

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for("register"))

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        conn = get_db()

        try:
            conn.execute(
                """
                INSERT INTO users (username, email, password)
                VALUES (?, ?, ?)
                """,
                (username, email, hashed_password)
            )

            conn.commit()

        except sqlite3.IntegrityError:
            conn.close()
            flash("Username or email already exists.", "error")
            return redirect(url_for("register"))

        conn.close()

        flash("Registration successful. Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


# ---------------- HOME ----------------

@app.route("/home")
def home():

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    notes = conn.execute(
        """
        SELECT * FROM notes
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (session["user_id"],)
    ).fetchall()

    conn.close()

    return render_template(
        "home.html",
        notes=notes,
        username=session["username"]
    )


# ---------------- ADD NOTE ----------------

@app.route("/add_note", methods=["POST"])
def add_note():

    if "user_id" not in session:
        return redirect(url_for("login"))

    title = request.form["title"]
    content = request.form["content"]

    if title.strip() == "" or content.strip() == "":
        flash("Title and content are required.", "error")
        return redirect(url_for("home"))

    conn = get_db()

    conn.execute(
        """
        INSERT INTO notes (user_id, title, content)
        VALUES (?, ?, ?)
        """,
        (session["user_id"], title, content)
    )

    conn.commit()
    conn.close()

    flash("Note added successfully.", "success")

    return redirect(url_for("home"))


# ---------------- EDIT NOTE ----------------

@app.route("/edit_note/<int:note_id>", methods=["POST"])
def edit_note(note_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    title = request.form["title"]
    content = request.form["content"]

    conn = get_db()

    conn.execute(
        """
        UPDATE notes
        SET title = ?, content = ?
        WHERE id = ? AND user_id = ?
        """,
        (title, content, note_id, session["user_id"])
    )

    conn.commit()
    conn.close()

    flash("Note updated successfully.", "success")

    return redirect(url_for("home"))


# ---------------- DELETE NOTE ----------------

@app.route("/delete_note/<int:note_id>", methods=["POST"])
def delete_note(note_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    conn.execute(
        """
        DELETE FROM notes
        WHERE id = ? AND user_id = ?
        """,
        (note_id, session["user_id"])
    )

    conn.commit()
    conn.close()

    flash("Note deleted.", "success")

    return redirect(url_for("home"))


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ---------------- START APP ----------------

if __name__ == "__main__":
    init_db()
    app.run(debug=True)