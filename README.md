# Expense Tracker (Flask + SQLite)

A simple expense tracking web application built using Flask and SQLite.  
The project demonstrates backend evolution from CSV-based storage to a
database-driven architecture with SQL analytics.

## Features
- Add daily expenses (amount, category, note, date)
- Persistent storage using SQLite
- View all expenses
- Total expense calculation
- Category-wise expense summary
- Monthly expense filtering
- Clean project structure with version history

## Tech Stack
- Python
- Flask
- SQLite
- HTML, CSS
- Git

## Project Levels
### Level 1
- CSV-based data storage
- Manual aggregation using Python loops

### Level 2
- Migrated to SQLite database
- Used SQL queries (`SUM`, `GROUP BY`, `WHERE`)
- Improved backend performance and structure

## How to Run
1. Create database:
   python db_setup.py
2. Start server:
   python app.py
3. Open browser:
   http://127.0.0.1:5000
   
## Notes
- Database file (expenses.db) is ignored from Git using .gitignore
- CSV version is preserved for learning and reference

## Author
Amulya Reddy Ramidi

