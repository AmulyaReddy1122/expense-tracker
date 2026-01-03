import csv
import matplotlib.pyplot as plt
from datetime import date

FILE_NAME = "expenses.csv"


def add_expense():
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("❌ Invalid amount")
        return

    category = input("Enter category: ").strip()
    note = input("Enter note (optional): ").strip()
    today = date.today()

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([today, amount, category, note])

    print("✅ Expense added successfully!")


def view_expenses():
    print("\n--- All Expenses ---")

    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            empty = True
            for row in reader:
                empty = False
                print(
                    f"Date: {row[0]} | Amount: {row[1]} | Category: {row[2]} | Note: {row[3]}"
                )

            if empty:
                print("No expenses found.")
    except FileNotFoundError:
        print("No expenses file found.")


def total_expense():
    total = 0.0

    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                total += float(row[1])
    except FileNotFoundError:
        print("No data found.")
        return

    print(f"\n💰 Total Expense: ₹{total}")


def category_summary():
    summary = {}

    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                category = row[2]
                amount = float(row[1])
                summary[category] = summary.get(category, 0) + amount
    except FileNotFoundError:
        print("No data found.")
        return

    print("\n📊 Category-wise Summary:")
    for category, amount in summary.items():
        print(f"{category}: ₹{amount}")

def show_category_pie():
    summary = {}

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            category = row[2]
            amount = float(row[1])
            summary[category] = summary.get(category, 0) + amount

    if not summary:
        print("No data to plot.")
        return

    labels = summary.keys()
    values = summary.values()

    plt.figure()
    plt.pie(values, labels=labels, autopct="%1.1f%%")
    plt.title("Category-wise Expense Distribution")
    plt.show()

def show_monthly_bar():
    monthly_totals = {}

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            date_str = row[0]  # YYYY-MM-DD
            amount = float(row[1])

            year, month, _ = date_str.split("-")
            key = f"{month}-{year}"

            monthly_totals[key] = monthly_totals.get(key, 0) + amount

    if not monthly_totals:
        print("No data to plot.")
        return

    months = list(monthly_totals.keys())
    totals = list(monthly_totals.values())

    plt.figure()
    plt.bar(months, totals)
    plt.xlabel("Month")
    plt.ylabel("Total Expense")
    plt.title("Monthly Expense Trend")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def monthly_summary():
    month = input("Enter month (MM): ").strip()
    year = input("Enter year (YYYY): ").strip()

    total = 0.0
    summary = {}

    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                date_str = row[0]          # YYYY-MM-DD
                amount = float(row[1])
                category = row[2]

                row_year, row_month, _ = date_str.split("-")

                if row_year == year and row_month == month:
                    total += amount
                    summary[category] = summary.get(category, 0) + amount
    except FileNotFoundError:
        print("No data found.")
        return

    print(f"\n📅 Monthly Summary for {month}-{year}")
    print(f"Total Expense: ₹{total}")

    for cat, amt in summary.items():
        print(f"{cat}: ₹{amt}")


def main_menu():
    while True:
        print("\n===== Expense Tracker =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Total Expense")
        print("4. Category Summary")
        print("5. Monthly Summary")
        print("6. Exit")
        print("7. Show Category Pie Chart")
        print("8. Show Monthly Bar Chart")



        choice = input("Choose option: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            total_expense()
        elif choice == "4":
            category_summary()
        elif choice == "5":
            monthly_summary()
        elif choice == "6":
            print("Bye 👋")
            break
        elif choice == "7":
            show_category_pie()
        elif choice == "8":
            show_monthly_bar()


        else:
            print("❌ Invalid choice")
main_menu()