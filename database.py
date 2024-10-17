import sqlite3
import random
from security import hash_password



def connect_db():
    # Connect to the SQLite database
    conn = sqlite3.connect('finance_tracker.db')

    # Enable foreign key support
    conn.execute('PRAGMA foreign_keys = ON')
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
            date TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(userid) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()

def add_transaction(description, amount, date, user_id):
    print(f'Adding transaction: {description}, {amount}, {date}, {user_id}')
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (description, amount, date, user_id)
        VALUES (?,?,?,?)
    ''',(description, amount, date, user_id))
    conn.commit()
    conn.close()

def get_transactions(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')
    cursor.execute('SELECT * FROM transactions WHERE user_id = ?', (user_id,))
    transactions = cursor.fetchall()
    conn.close()
    return transactions

def delete_transaction(transaction_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
    conn.commit()
    conn.close()

def transaction_search_description(search_text, transactions):
    # Filter the transactions based on the description
    filtered_transactions = []
    for transaction in transactions:
        if search_text.lower() in transaction[1].lower():
            filtered_transactions.append(transaction)
    return filtered_transactions

def sort_data(user_id, query):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')
    og_query = 'SELECT * FROM transactions WHERE user_id = ? '
    query = (og_query + query)
    cursor.execute(query, (user_id,))
    transactions = cursor.fetchall()
    conn.close()
    return transactions

def belongs_to_user(user_id, transaction_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions WHERE id = ? AND user_id = ?', (transaction_id, user_id))
    transaction = cursor.fetchone()
    conn.close()
    return transaction is not None

def transaction_exists(transaction_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions WHERE id = ?', (transaction_id,))
    transaction = cursor.fetchone()
    conn.close()
    return transaction is not None

def create_user_table():
    # Create a table for users if it doesn't exist
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            userid INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Generate a unique user name

def generate_username(first_name, last_name):
    username_base = f'{first_name[0].upper()}{last_name[:4].lower()}'
    while True:
        random_number = random.randint(10, 99) # generate a random 2 digit number
        username = f'{username_base}{random_number}'
        if not username_exists(username):
            return username


def username_exists(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE username = ?
    ''', (username,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def add_user(first_name, last_name, password, email, phone):
    username = generate_username(first_name, last_name)
    # Add hashing later
    # hashed_password = hash_password(password)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (username, firstname, lastname, email, phone, password)
        VALUES (?,?,?,?,?,?)
    ''', (username, first_name, last_name, email, phone, password))
    conn.commit()
    conn.close()
    return username # Return the generated username to show the user

def check_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')
    cursor.execute('''
        SELECT * FROM users WHERE username = ? AND password = ?
    ''', (username, password ))
    user = cursor.fetchone()
    conn.close()
    if user:
        return user[0]
    else:
        return None

def email_exists(email):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE email = ?
    ''', (email,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def get_id_using_email(email):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE email = ?
    ''', (email,))
    user = cursor.fetchone()
    conn.close()
    return user[0]