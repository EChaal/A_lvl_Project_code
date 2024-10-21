import csv
import os
import database as db  # Assuming your `get_transactions` function is in database.py
import globals  # To get current_user_id
from tkinter import filedialog, messagebox


def export_transactions_to_csv():
    # Get the transactions for the current user
    user_id = 1 # globals.current_user_id for when in actual application
    transactions = db.get_transactions(user_id)

    if not transactions:
        messagebox.showerror('Error', 'No transactions to export.')
        return

    # Ask the user where they want to save the file
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        title="Save Transactions"
    )

    if not file_path:
        return  # User cancelled the save dialog

    try:
        # Write transactions to CSV
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write headers (adjust the headers based on your transactions' structure)
            writer.writerow(['ID', 'Description', 'Amount', 'Date'])

            # Write the transaction data
            for transaction in transactions:
                writer.writerow(transaction[:-1])

        messagebox.showinfo('Success', f'Transactions exported successfully to {os.path.basename(file_path)}')

    except Exception as e:
        messagebox.showerror('Error', f'An error occurred while exporting: {str(e)}')


export_transactions_to_csv()