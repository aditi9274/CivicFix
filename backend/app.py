from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)

# 👇 THIS LINE FIXES YOUR ERROR
CORS(app, resources={r"/*": {"origins": "*"}})

# ---------- DATABASE ----------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------- HOME ----------
@app.route("/")
def home():
    return "CivicFix Backend Running"

# ---------- INIT DATABASE ----------
@app.route("/init")
def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            description TEXT,
            location TEXT,
            status TEXT
        )
    """)
    conn.commit()
    return "Database initialized"

# ---------- REPORT ISSUE ----------
@app.route("/report", methods=["POST"])
def report_issue():
    data = request.get_json()
    print("RECEIVED DATA:", data)

    if not data:
        return jsonify({"error": "No data received"}), 400

    conn = get_db()
    conn.execute(
        "INSERT INTO issues (category, description, location, status) VALUES (?, ?, ?, ?)",
        (
            data.get("category"),
            data.get("description"),
            data.get("location"),
            "Reported"
        )
    )
    conn.commit()

    return jsonify({"message": "Issue reported successfully"})

# ---------- GET ALL ISSUES ----------
@app.route("/issues")
def get_issues():
    conn = get_db()
    issues = conn.execute("SELECT * FROM issues").fetchall()
    return jsonify([dict(issue) for issue in issues])

# ---------- START SERVER ----------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
