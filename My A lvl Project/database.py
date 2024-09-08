import sqlite3

def connect_db():
    # Connect to the SQLite database
    conn = sqlite3.connect('finance_tracker.db')
    return conn

def create_table():
    # Create a table for transactions if it doesn't exist
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
