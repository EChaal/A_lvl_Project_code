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

def add_transaction(description, amount, date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (description, amount, date)
        VALUES (?,?,?)
    ''',(description, amount, date))
    conn.commit()
    conn.close()

def get_transactions():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()
    conn.close()
    return transactions

def delete_transaction(transaction_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
    conn.commit()
    conn.close()