import os
from flask import Flask, request, redirect, url_for, session, render_template
import psycopg2

app = Flask(__name__)
app.secret_key = "dev-secret-key"

DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = "appdb"
DB_USER = "appuser"
DB_PASSWORD = "apppass"

FILES_DIR = "/files"

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            session["username"] = username
            return redirect(url_for("dashboard"))

        return "Invalid username or password", 401

    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]
    user_dir = os.path.join(FILES_DIR, username)
    os.makedirs(user_dir, exist_ok=True)

    if request.method == "POST":
        file = request.files["file"]
        if file:
            file.save(os.path.join(user_dir, file.filename))

    files = os.listdir(user_dir)
    return render_template("dashboard.html", username=username, files=files)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
