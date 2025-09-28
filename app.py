from flask import Flask, render_template, request, redirect, session, flash, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

DB_NAME = "users.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
    print("Database initialized!")

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Fields cannot be empty!", "danger")
            return redirect(url_for("register"))

        if len(username) > 30 or len(password) > 50:
            flash("Input too long!", "danger")
            return redirect(url_for("register"))

        try:
            with sqlite3.connect(DB_NAME) as conn:
                conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
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

        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = cur.fetchone()

        if user:
            session["user"] = username
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password!", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        flash("Please log in first!", "warning")
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["user"])

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully!", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    if not os.path.exists(DB_NAME):
        init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)





#------------------------------OLD VERSION------------------------------------------------


# from flask import Flask, render_template, request, redirect, session, flash, url_for
# import sqlite3
# import os

# app = Flask(__name__)
# app.secret_key = "your_secret_key"  # Needed for sessions

# DB_NAME = "users.db"

# # ✅ Initialize DB
# def init_db():
#     with sqlite3.connect(DB_NAME) as conn:
#         conn.execute("""
#             CREATE TABLE IF NOT EXISTS users (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 username TEXT UNIQUE NOT NULL,
#                 password TEXT NOT NULL
#             )
#         """)
#     print("Database initialized!")


# # ✅ Home route → redirect to login
# @app.route("/")
# def home():
#     return redirect(url_for("login"))


# # ✅ Register Page
# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         username = request.form.get("username", "").strip()
#         password = request.form.get("password", "").strip()

#         # 🔍 Validation
#         if not username or not password:
#             flash("Fields cannot be empty!", "danger")
#             return redirect(url_for("register"))

#         if len(username) > 30 or len(password) > 50:
#             flash("Input too long!", "danger")
#             return redirect(url_for("register"))

#         try:
#             with sqlite3.connect(DB_NAME) as conn:
#                 conn.execute(
#                     "INSERT INTO users (username, password) VALUES (?, ?)",
#                     (username, password),
#                 )
#                 conn.commit()
#             flash("Registration successful! Please log in.", "success")
#             return redirect(url_for("login"))
#         except sqlite3.IntegrityError:
#             flash("Username already exists!", "danger")
#             return redirect(url_for("register"))

#     return render_template("register.html")


# # ✅ Login Page
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"].strip()
#         password = request.form["password"].strip()

#         with sqlite3.connect(DB_NAME) as conn:
#             cur = conn.cursor()
#             cur.execute(
#                 "SELECT * FROM users WHERE username=? AND password=?",
#                 (username, password),
#             )
#             user = cur.fetchone()

#         if user:
#             session["user"] = username
#             return redirect(url_for("dashboard"))
#         else:
#             flash("Invalid username or password!", "danger")

#     return render_template("login.html")


# # ✅ Dashboard (protected)
# @app.route("/dashboard")
# def dashboard():
#     if "user" not in session:  # 🚨 Block direct access
#         flash("Please log in first!", "warning")
#         return redirect(url_for("login"))
#     return render_template("dashboard.html", username=session["user"])


# # ✅ Logout
# @app.route("/logout")
# def logout():
#     session.pop("user", None)
#     flash("Logged out successfully!", "info")
#     return redirect(url_for("login"))


# if __name__ == "__main__":
#     if not os.path.exists(DB_NAME):
#         init_db()
#     app.run(debug=True)
