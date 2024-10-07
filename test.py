import tkinter as tk
from tkinter import ttk
import sqlite3
import database as db

# Function to create the GUI and Treeview
def create_main_window():
    root = tk.Tk()
    root.title("Live Search in Treeview")

    # Entry for search bar
    search_entry = tk.Entry(root)
    search_entry.pack(pady=10)

    # Treeview widget
    columns = ('ID', 'Description', 'Amount', 'Date')
    tree = ttk.Treeview(root, columns=columns, show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Description', text='Description')
    tree.heading('Amount', text='Amount')
    tree.heading('Date', text='Date')
    tree.pack(pady=10, fill=tk.BOTH, expand=True)

    # Connect to the database and fetch initial data
    conn = sqlite3.connect('finance_tracker.db')
    cur = conn.cursor()

    # Function to load all rows in the Treeview
    def load_data():
        tree.delete(*tree.get_children())
        cur.execute("SELECT ID, Description, Amount, Date FROM transactions")
        rows = cur.fetchall()
        for row in rows:
            tree.insert("", tk.END, values=row)

    # Function to search and filter data
    def search_data(event):
        search_text = search_entry.get()
        tree.delete(*tree.get_children())  # Clear the Treeview

        # Query to search by description
        filtered_rows = db.transaction_query_description(1, search_text)

        for row in filtered_rows:
            tree.insert("", tk.END, values=row)

    # Bind the search entry to the key release event
    search_entry.bind('<KeyRelease>', search_data)

    # Load initial data
    load_data()

    root.mainloop()

# Call the function to create the window and run the app
create_main_window()
