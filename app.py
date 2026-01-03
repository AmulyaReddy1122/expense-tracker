from flask import Flask, render_template, request
import sqlite3
from datetime import date

app = Flask(__name__)

DB_NAME = "expenses.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        amount = float(request.form["amount"])
        category = request.form["category"]
        note = request.form.get("note", "")
        today = date.today().isoformat()

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO expenses (date, amount, category, note) VALUES (?, ?, ?, ?)",
            (today, amount, category, note)
        )
        conn.commit()

    conn = get_db_connection()

    expenses = conn.execute("SELECT * FROM expenses").fetchall()

    total = conn.execute(
        "SELECT SUM(amount) FROM expenses"
    ).fetchone()[0] or 0

    category_summary = conn.execute(
        "SELECT category, SUM(amount) as total FROM expenses GROUP BY category"
    ).fetchall()

    monthly_total = None
    monthly_summary = []

    month = request.args.get("month")
    year = request.args.get("year")

    if month and year:
        monthly_total = conn.execute(
            """
            SELECT SUM(amount) FROM expenses
            WHERE strftime('%Y', date) = ?
            AND strftime('%m', date) = ?
            """,
            (year, month.zfill(2))
        ).fetchone()[0] or 0

        monthly_summary = conn.execute(
            """
            SELECT category, SUM(amount)
            FROM expenses
            WHERE strftime('%Y', date) = ?
            AND strftime('%m', date) = ?
            GROUP BY category
            """,
            (year, month.zfill(2))
        ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        category_summary=category_summary,
        monthly_total=monthly_total,
        monthly_summary=monthly_summary
    )


if __name__ == "__main__":
    app.run(debug=True)
