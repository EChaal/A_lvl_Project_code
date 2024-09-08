import tkinter as tk
import database as db

def create_main_window(root):
    # Set up the main window layout
    label = tk.Label(root, text="Welcome to Personal Finance Tracker!")
    label.pack(pady=20)

    # Set up the entry fields for transaction
    description_label = tk.Label(root, text='Description: ')
    description_label.pack()
    description_entry = tk.Entry(root)
    description_entry.pack()

    amount_label = tk.Label(root, text='Amount: ')
    amount_label.pack()
    amount_entry = tk.Entry(root)
    amount_entry.pack()

    date_label = tk.Label(root, text='Date (YYYY-MM-DD): ')
    date_label.pack()
    date_entry = tk.Entry(root)
    date_entry.pack()

    def add_transaction():
        desc = description_entry.get()
        amount = float(amount_entry.get())
        date = date_entry.get()
        db.add_transaction(desc, amount, date)
        display_transactions()
    
    add_button = tk.Button(root, text='Add transaction', command=add_transaction)
    add_button.pack(pady=10)

    transactions_txt = tk.Text(root, width=40, height=10)
    transactions_txt.pack(pady=20)

    def display_transactions():
        transactions_txt.delete(1.0, tk.END)
        transactions = db.get_transactions()
        for transaction in transactions:
            transactions_txt.insert(tk.END, f'{transaction}\n')
    
    display_transactions() # Shpws all existing transactions