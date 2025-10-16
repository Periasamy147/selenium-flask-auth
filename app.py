from flask import Flask, render_template, request, redirect, session, flash, url_for
import os
import re
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Secret key for sessions
app.secret_key = os.getenv("FLASK_SECRET_KEY", "super_secret_key")

# PostgreSQL connection string
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:thegourmet@localhost:5432/flask_db"
)

# --- Database helpers ---
def get_db_connection():
    # ✅ CI-safe (GitHub Actions)
    if os.getenv("CI") == "true":
        return psycopg2.connect(DATABASE_URL)
    return psycopg2.connect(DATABASE_URL)


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    # ✅ Add name & age columns if not exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name VARCHAR(100),
            age INT
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Database initialized")


# --- Routes ---
@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if len(username) > 50:
            flash("Username must be under 50 characters!", "danger")
            return redirect(url_for("register"))\

        if not username or not password:
            flash("Fields cannot be empty!", "danger")
            return redirect(url_for("register"))
        

        hashed_pw = generate_password_hash(password)

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (username, password, name, age) VALUES (%s, %s, %s, %s)",
                (username, hashed_pw, None, None)
            )
            conn.commit()
            cur.close()
            conn.close()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))
        except psycopg2.IntegrityError:
            conn.rollback()
            cur.close()
            conn.close()
            flash("Username already exists!", "danger")
            return redirect(url_for("register"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Fields cannot be empty!", "danger")
            return redirect(url_for("login"))

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT password FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user[0], password):
            session["user"] = username
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password!", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        flash("Please log in first!", "warning")
        return redirect(url_for("login"))

    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch current user info
    cur.execute("SELECT name, age FROM users WHERE username = %s", (session["user"],))
    user_data = cur.fetchone()
    name = user_data[0] if user_data and user_data[0] else "N/A"
    age = user_data[1] if user_data and user_data[1] else "N/A"

    # Handle POST (edit)
    if request.method == "POST":
        new_name = request.form.get("name", "").strip()
        new_age = request.form.get("age", "").strip()

        if not new_name or not new_age:
            flash("Name and Age cannot be empty!", "danger")
            return redirect(url_for("dashboard"))
        
        if not re.match(r"^[A-Za-z ]+$", new_name):
            flash("Name can only contain letters and spaces!", "danger")
            return redirect(url_for("dashboard"))

        try:
            new_age = int(new_age)
        except ValueError:
            flash("Age must be a number!", "danger")
            return redirect(url_for("dashboard"))

        if new_age < 18 or new_age > 100:
            flash("Age must be between 18 and 100!", "danger")
            return redirect(url_for("dashboard"))

        cur.execute(
            "UPDATE users SET name = %s, age = %s WHERE username = %s",
            (new_name, new_age, session["user"])
        )
        conn.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("dashboard"))

    cur.close()
    conn.close()

    return render_template(
        "dashboard.html",
        username=session["user"],
        name=name,
        age=age
    )


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully!", "info")
    return redirect(url_for("login"))


# --- Entry point ---
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
