from flask import Flask, render_template, request, redirect
import sqlite3
from ai_engine import analyze_text
from datetime import datetime

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS journal (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT,
                    mood TEXT,
                    sentiment REAL,
                    confidence INTEGER,
                    stress INTEGER,
                    date TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    text = request.form["journal"]
    result = analyze_text(text)

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO journal (text, mood, sentiment, confidence, stress, date) VALUES (?, ?, ?, ?, ?, ?)",
              (text, result["mood"], result["sentiment"], result["confidence_score"],
               result["stress_score"], datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT mood, sentiment, confidence, stress, date FROM journal")
    data = c.fetchall()
    conn.close()

    return render_template("dashboard.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)