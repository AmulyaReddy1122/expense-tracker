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
        conn.close()

    conn = get_db_connection()
    expenses = conn.execute("SELECT * FROM expenses").fetchall()
    conn.close()

    total = 0.0
    category_summary = {}
    monthly_total = None
    monthly_summary = {}

    month = request.args.get("month")
    year = request.args.get("year")

    for exp in expenses:
        amount = exp["amount"]
        total += amount

        category = exp["category"]
        category_summary[category] = category_summary.get(category, 0) + amount

        if month and year:
            row_year, row_month, _ = exp["date"].split("-")
            if row_year == year and row_month == month:
                monthly_total = (monthly_total or 0) + amount
                monthly_summary[category] = (
                    monthly_summary.get(category, 0) + amount
                )

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
