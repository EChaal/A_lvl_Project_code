import tkinter as tk
from tkinter import ttk
import sqlite3

def create_main_window():
    root = tk.Tk()
    root.title("Live Checkbutton Filtering and Sorting in Treeview")

    # Connect to the database
    conn = sqlite3.connect('finance_tracker.db')
    cur = conn.cursor()

    # Create a frame for the filtering options
    filter_frame = tk.Frame(root)
    filter_frame.pack(pady=10)

    # Sorting Checkbuttons (A-Z and Z-A)
    az_checked = tk.IntVar(value=0)
    za_checked = tk.IntVar(value=0)

    def az_checked_handler():
        if az_checked.get():
            za_checked.set(0)  # Ensure Z-A is unchecked
        filter_data()

    def za_checked_handler():
        if za_checked.get():
            az_checked.set(0)  # Ensure A-Z is unchecked
        filter_data()

    tk.Label(filter_frame, text="Sort by Description:").grid(row=2, column=0, pady=10)
    tk.Checkbutton(filter_frame, text="A-Z", variable=az_checked, command=az_checked_handler).grid(row=2, column=1)
    tk.Checkbutton(filter_frame, text="Z-A", variable=za_checked, command=za_checked_handler).grid(row=2, column=2)

    # Frame for the Treeview and Scrollbar
    tree_frame = tk.Frame(root)
    tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    # Add a vertical scrollbar
    scrollbar = ttk.Scrollbar(tree_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Treeview widget
    columns = ('ID', 'Description', 'Amount', 'Date')
    tree = ttk.Treeview(tree_frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
    tree.heading('ID', text='ID')
    tree.heading('Description', text='Description')
    tree.heading('Amount', text='Amount')
    tree.heading('Date', text='Date')
    tree.pack(pady=10, fill=tk.BOTH, expand=True)

    # Configure the scrollbar to work with the Treeview
    scrollbar.config(command=tree.yview)

    # Function to load all data into the Treeview
    def load_data():
        tree.delete(*tree.get_children())  # Clear the Treeview first
        cur.execute("SELECT ID, Description, Amount, Date FROM transactions")
        rows = cur.fetchall()
        for row in rows:
            tree.insert("", tk.END, values=row)

    # Function to filter data based on the checkbuttons and sorting options
    def filter_data():
        tree.delete(*tree.get_children())  # Clear the Treeview

        # Base query
        query = "SELECT ID, Description, Amount, Date FROM transactions WHERE 1=1"
        params = []

        # Apply sorting based on selected checkbutton
        if az_checked.get():  # Sort A-Z
            query += " ORDER BY Description ASC"
        elif za_checked.get():  # Sort Z-A
            query += " ORDER BY Description DESC"

        # Execute the query with the filters and sorting applied
        cur.execute(query, params)
        filtered_rows = cur.fetchall()

        # Insert the filtered rows back into the Treeview
        for row in filtered_rows:
            tree.insert("", tk.END, values=row)

    # Load the initial data
    load_data()

    root.mainloop()

# Call the function to create the window
create_main_window()
