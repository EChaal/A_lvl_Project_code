import tkinter as tk
from tkinter import ttk
import database as db

def create_main_window(root):
    # Set up the main window layout
    label = tk.Label(root, text="Welcome to Personal Finance Tracker!")
    label.grid(row=0, column=0, columnspan=4, pady=20)

    # Set up the entry fields for transaction
    description_label = tk.Label(root, text='Description: ')
    description_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
    description_entry = tk.Entry(root)
    description_entry.grid(row=1, column=1, padx=10, pady=5)

    amount_label = tk.Label(root, text='Amount: ')
    amount_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5) 
    amount_entry = tk.Entry(root)
    amount_entry.grid(row=2, column=1, padx=10, pady=5)

    # Add radio button for selecting income or expense

    transaction_type = tk.StringVar(value='expense')
    income_radio = tk.Radiobutton(root, text='Income', variable=transaction_type, value='income')
    expense_radio = tk.Radiobutton(root, text='Expense', variable=transaction_type, value='expense')
    
    income_radio.grid(row=2, column=2, padx=10, pady=5, sticky=tk.W)
    expense_radio.grid(row=2, column=3, padx=10, pady=5, sticky=tk.W)

    date_label = tk.Label(root, text='Date (YYYY-MM-DD): ')
    date_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
    date_entry = tk.Entry(root)
    date_entry.grid(row=3, column=1, padx=10, pady=5)



    def add_transaction():
        desc = description_entry.get()
        amount = float(amount_entry.get())
        date = date_entry.get()

        #Check if income or expense 
        if transaction_type.get() == 'expense':
            amount = -amount # Make expenses negative
        
        db.add_transaction(desc, amount, date)
        display_transactions()
        update_summary()
    
    add_button = tk.Button(root, text='Add Transaction', command=add_transaction)
    add_button.grid(row=4, column=0, columnspan=4, padx=10, pady=5)


    ### Create a treeview widget to view transactions more clearly

    columns = ('ID', 'Description', 'Amount', 'Date')
    transactions_tree = ttk.Treeview(root, columns=columns, show='headings')

    # Define headings

    transactions_tree.heading('ID', text='ID')
    transactions_tree.heading('Description', text='Description')
    transactions_tree.heading('Amount', text='Amount')
    transactions_tree.heading('Date', text='Date')

    # Define column widths

    transactions_tree.column('ID', width=50)
    transactions_tree.column('Description', width=150)
    transactions_tree.column('Amount', width=100)
    transactions_tree.column('Date', width=100)

    transactions_tree.grid(row=5, column=0, columnspan=4, padx=10, pady=5)

    def display_transactions():
        # Clear the treeview
        for row in transactions_tree.get_children():
            transactions_tree.delete(row)
        # Insert existing transactions into treeview
        transactions = db.get_transactions()
        for transaction in transactions:
            transactions_tree.insert('', tk.END, values=transaction)
        
    
    def delete_transaction():
        transaction_id = int(transaction_id_entry.get())
        db.delete_transaction(transaction_id)
        display_transactions()
        update_summary()
    

    transaction_id_label = tk.Label(root, text='Transaction ID to delete: ')
    transaction_id_label.grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
    transaction_id_entry = tk.Entry(root)
    transaction_id_entry.grid(row=6, column=1, padx=10, pady=5)

    delete_button = tk.Button(root, text='Delete Transaction', command=delete_transaction)
    delete_button.grid(row=6, column=2, columnspan=2, pady=10)

    summary_label = tk.Label(root, text='Transaction summary', font=('Helvetica', 14))
    summary_label.grid(row=7, column=0, columnspan=4, pady=10)

    summary_txt = tk.Text(root, width=40, height=5)
    summary_txt.grid(row=8, column=0, columnspan=4, pady=20)

    def update_summary():
        transactions = db.get_transactions()
        total_income = 0
        total_expenses = 0

        for transaction in transactions:
            amount = transaction[2]
            if amount > 0:
                total_income += amount
            else:
                total_expenses += -amount # Minus because we need to make expenses positive for display
        
        balance = total_income - total_expenses

        summary_txt.delete(1.0, tk.END)
        summary_txt.insert(tk.END, f'Total income: {total_income} \n')
        summary_txt.insert(tk.END, f'Total expenses: {total_expenses} \n')
        summary_txt.insert(tk.END, f'Balance: {balance}')
        

    
    display_transactions() # Shpws all existing transactions

    update_summary() # Update the summary initially

