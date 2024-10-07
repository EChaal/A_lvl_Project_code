import tkinter as tk
from tkinter import ttk
import sqlite3

def create_main_window():
    root = tk.Tk()
    root.title("Advanced Filtering in Treeview")

    # Connect to the database
    conn = sqlite3.connect('finance_tracker.db')
    cur = conn.cursor()

    # Create a frame for the filtering options
    filter_frame = tk.Frame(root)
    filter_frame.pack(pady=10)

    # Combobox for alphabetical filtering (Description)
    desc_order_label = tk.Label(filter_frame, text="Description Order:")
    desc_order_label.grid(row=0, column=0, padx=10)
    desc_order = ttk.Combobox(filter_frame, values=["None", "A-Z", "Z-A"], state="readonly")
    desc_order.grid(row=0, column=1)
    desc_order.current(0)  # Set default selection to "None"

    # Combobox for filtering by Date
    date_filter_label = tk.Label(filter_frame, text="Date Filter:")
    date_filter_label.grid(row=0, column=2, padx=10)
    date_filter = ttk.Combobox(filter_frame, values=["None", "Oldest First", "Newest First"], state="readonly")
    date_filter.grid(row=0, column=3)
    date_filter.current(0)  # Set default selection to "None"

    # Combobox for filtering by Amount
    amount_filter_label = tk.Label(filter_frame, text="Amount Filter:")
    amount_filter_label.grid(row=1, column=0, padx=10)
    amount_filter = ttk.Combobox(filter_frame, values=["None", "Less than", "Equal to", "Greater than"], state="readonly")
    amount_filter.grid(row=1, column=1)
    amount_filter.current(0)  # Set default selection to "None"

    # Entry to input the value for amount comparison
    amount_value_label = tk.Label(filter_frame, text="Amount Value:")
    amount_value_label.grid(row=1, column=2, padx=10)
    amount_value = tk.Entry(filter_frame)
    amount_value.grid(row=1, column=3)

    # Treeview widget
    columns = ('ID', 'Description', 'Amount', 'Date')
    tree = ttk.Treeview(root, columns=columns, show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Description', text='Description')
    tree.heading('Amount', text='Amount')
    tree.heading('Date', text='Date')
    tree.pack(pady=10, fill=tk.BOTH, expand=True)

    # Function to load all data into the Treeview
    def load_data():
        tree.delete(*tree.get_children())  # Clear the Treeview first
        cur.execute("SELECT ID, Description, Amount, Date FROM transactions")
        rows = cur.fetchall()
        for row in rows:
            tree.insert("", tk.END, values=row)

    # Function to filter data based on the dropdown selections
    def filter_data():
        tree.delete(*tree.get_children())  # Clear the Treeview

        query = "SELECT ID, Description, Amount, Date FROM transactions WHERE 1=1"
        params = []

        # Apply description filter
        if desc_order.get() == "A-Z":
            query += " ORDER BY Description ASC"
        elif desc_order.get() == "Z-A":
            query += " ORDER BY Description DESC"

        # Apply date filter
        if date_filter.get() == "Oldest First":
            query += ", Date ASC"
        elif date_filter.get() == "Newest First":
            query += ", Date DESC"

        # Apply amount filter
        if amount_filter.get() != "None" and amount_value.get():
            if amount_filter.get() == "Less than":
                query += " AND Amount < ?"
            elif amount_filter.get() == "Equal to":
                query += " AND Amount = ?"
            elif amount_filter.get() == "Greater than":
                query += " AND Amount > ?"
            params.append(float(amount_value.get()))

        # Execute the query and fetch filtered results
        cur.execute(query, params)
        filtered_rows = cur.fetchall()

        # Insert the filtered rows back into the Treeview
        for row in filtered_rows:
            tree.insert("", tk.END, values=row)

    # Button to apply the filter
    apply_button = tk.Button(root, text="Apply Filter", command=filter_data)
    apply_button.pack(pady=10)

    # Load the initial data
    load_data()

    root.mainloop()

# Call the function to create the window
create_main_window()
