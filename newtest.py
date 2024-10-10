import tkinter as tk
from tkinter import ttk
import sqlite3

def create_main_window():
    root = tk.Tk()
    root.title("Live Checkbutton Filtering and Sorting in Treeview")

    # Connect to the database
    conn = sqlite3.connect('finance_tracker.db')
    cur = conn.cursor()

    # Create a frame for the Treeview and Scrollbar
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

    # Filtering variables
    az_checked = tk.BooleanVar()
    za_checked = tk.BooleanVar()
    amount_checked = tk.BooleanVar()
    date_checked = tk.BooleanVar()

    # Exclusive check function to ensure A-Z and Z-A can't both be checked
    def az_checked_handler():
        if az_checked.get():
            za_checked.set(0)  # Uncheck Z-A if A-Z is checked
        filter_data()

    def za_checked_handler():
        if za_checked.get():
            az_checked.set(0)  # Uncheck A-Z if Z-A is checked
        filter_data()

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

    # Function to show the filter menu next to the Treeview
    def show_filter_menu(event):
        filter_menu.post(event.x_root, event.y_root)

    # Create a popup filter menu
    filter_menu = tk.Menu(root, tearoff=0)

    # Add Checkbutton menu items to the menu
    filter_menu.add_checkbutton(label="Sort A-Z", onvalue=True, offvalue=False, variable=az_checked, command=az_checked_handler)
    filter_menu.add_checkbutton(label="Sort Z-A", onvalue=True, offvalue=False, variable=za_checked, command=za_checked_handler)
    filter_menu.add_checkbutton(label="Filter by Amount", onvalue=True, offvalue=False, variable=amount_checked, command=filter_data)
    filter_menu.add_checkbutton(label="Filter by Date", onvalue=True, offvalue=False, variable=date_checked, command=filter_data)

    # Button to show filter menu next to Treeview
    filter_button = ttk.Button(root, text="Show Filters", command=lambda: show_filter_menu(tree))
    filter_button.pack()

    # Bind the button to show the menu at the correct position
    filter_button.bind("<Button-1>", show_filter_menu)

    # Load the initial data
    load_data()

    root.mainloop()

# Call the function to create the window
create_main_window()
