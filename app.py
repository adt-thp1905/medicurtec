from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("updates.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db()
    updates = conn.execute("SELECT * FROM updates ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html", updates=updates)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        conn = get_db()
        conn.execute("INSERT INTO updates (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add.html")

if __name__ == "__main__":
    conn = sqlite3.connect("updates.db")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS updates (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT)"
    )
    conn.close()

    app.run(debug=True)