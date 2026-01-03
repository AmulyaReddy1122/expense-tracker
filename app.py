from flask import Flask, render_template, request
import csv
from datetime import date

app = Flask(__name__)

FILE_NAME = "expenses.csv"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        amount = float(request.form["amount"])
        category = request.form["category"]
        note = request.form.get("note", "")
        today = date.today()

        with open(FILE_NAME, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([today, amount, category, note])

    expenses = []
    total = 0.0
    category_summary = {}
    monthly_total = None
    monthly_summary = {}

    month = request.args.get("month")
    year = request.args.get("year")

    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                expenses.append(row)
                row_amount = float(row[1])
                total += row_amount

                category = row[2]
                category_summary[category] = category_summary.get(category, 0) + row_amount

                if month and year:
                    row_year, row_month, _ = row[0].split("-")
                    if row_year == year and row_month == month:
                        monthly_total = (monthly_total or 0) + row_amount
                        monthly_summary[category] = (
                            monthly_summary.get(category, 0) + row_amount
                        )
    except FileNotFoundError:
        pass



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
