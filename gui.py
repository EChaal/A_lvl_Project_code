import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *
from tkcalendar import DateEntry
import database as db
import globals
from validator import DataValidator


def create_main_window(main_window, current_user_id):
    # set up the validator
    validate = DataValidator()
    # Set up the main window
    main_window.title('Personal Finance Tracker - Main Window')

    # Set up the main window layout
    label = tk.Label(main_window, text="Welcome to Personal Finance Tracker!")
    label.grid(row=0, column=0, columnspan=4, pady=20)

    # Set up the entry fields for transaction
    description_label = tk.Label(main_window, text='Description: ')
    description_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
    description_entry = tk.Entry(main_window)
    description_entry.grid(row=1, column=1, padx=10, pady=5)

    amount_label = tk.Label(main_window, text='Amount: ')
    amount_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
    amount_entry = tk.Entry(main_window)
    amount_entry.grid(row=2, column=1, padx=10, pady=5)

    # Add radio button for selecting income or expense

    transaction_type = tk.StringVar(value='expense')
    income_radio = tk.Radiobutton(main_window, text='Income', variable=transaction_type, value='income')
    expense_radio = tk.Radiobutton(main_window, text='Expense', variable=transaction_type, value='expense')

    income_radio.grid(row=2, column=2, padx=10, pady=5, sticky=tk.W)
    expense_radio.grid(row=2, column=3, padx=10, pady=5, sticky=tk.W)

    date_label = tk.Label(main_window, text='Date (MM-DD-YY): ')
    date_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
    date_entry = DateEntry(main_window, width=12, background='darkblue', foreground='white', borderwidth=2)
    date_entry.grid(row=3, column=1, padx=10, pady=5)

    def clear_entries():
        amount_entry.delete(0, END)
        description_entry.delete(0, END)
        transaction_id_entry.delete(0, END)
        date_entry.set_date(date_entry._date.today()) # Reset date to today

    def add_transaction():
        desc = description_entry.get()
        amount = amount_entry.get()
        if validate.is_non_empty_string(amount) == False:
            messagebox.showerror('Error', 'Please enter a valid amount')
            return
        amount = float(amount)
        date = date_entry.get_date().strftime('%m-%d-%Y') # Get the date in the correct format

        # Validate the data
        if validate.is_non_empty_string(desc) == False and validate.is_positive_number(amount) == False:
            messagebox.showerror('Error', 'Please enter a valid description and amount')
            return
        if validate.in_future(date):
            messagebox.showerror('Error', 'Date cannot be in the future')
            return
        if current_user_id is None:
            messagebox.showerror('Error', 'You must be logged in to add a transaction')
            return
        #Check if income or expense
        if transaction_type.get() == 'expense':
            amount = -amount # Make expenses negative

        print(f'Description: {desc}, Amount: {amount}, Date: {date}, User ID: {current_user_id}')
        # Add this to the finance table
        user_id = current_user_id
        db.add_transaction(desc, amount, date, user_id)
        display_transactions()
        update_summary()
        clear_entries()

    add_button = tk.Button(main_window, text='Add Transaction', command=add_transaction)
    add_button.grid(row=4, column=0, columnspan=4, padx=10, pady=5)



    ### Create a treeview widget to view transactions more clearly

    columns = ('ID', 'Description', 'Amount', 'Date')
    transactions_tree = ttk.Treeview(main_window, columns=columns, show='headings')

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

    # Add a vertical scrollbar
    scrollbar = ttk.Scrollbar(main_window, orient='vertical', command=transactions_tree.yview)
    scrollbar.grid(row=5, column=3, sticky='ns')

    def display_transactions():
        # Clear the treeview
        for row in transactions_tree.get_children():
            transactions_tree.delete(row)

        # Make sure we have a user logged in
        if globals.current_user_id is None:
            messagebox.showerror('Error', 'You must be logged in to view transactions')
            return

        # Insert existing transactions into treeview
        if search_entry.get() == search_placeholder:
            transactions = db.get_transactions(globals.current_user_id)
            for transaction in transactions:
                transactions_tree.insert('', tk.END, values=transaction)
        else:
            filtered_transactions = db.transaction_query_description(globals.current_user_id, search_entry.get())
            for transaction in filtered_transactions:
                transactions_tree.insert('', tk.END, values=transaction)

    # Adding the search entry here to make sure it is defined before calling display_transactions

    #Define placeholders
    search_placeholder = 'Search by description'
    placeholder_color = 'grey'
    normal_color = 'black'

    # Setting up search entry
    search_entry = tk.Entry(main_window)
    search_entry.grid(row=4, column=2, columnspan=2, padx=10, pady=5)

    # Filtering variables
    a_zchecked = tk.BooleanVar()
    z_achecked = tk.BooleanVar()
    latest_checked = tk.BooleanVar()
    earliest_checked = tk.BooleanVar()
    income_checked = tk.BooleanVar()
    expense_checked = tk.BooleanVar()

    # Handler functions for the checkbuttons

    def a_zchecked_handler():
        if a_zchecked.get():
            z_achecked.set(0)

    def z_achecked_handler():
        if z_achecked.get():
            a_zchecked.set(0)

    def latest_checked_handler():
        if latest_checked.get():
            earliest_checked.set(0)

    def earliest_checked_handler():
        if earliest_checked.get():
            latest_checked.set(0)

    # Setting up a filter search menu button
    sort_menu = tk.Menu(main_window, tearoff=0)

    # to do with description
    sort_menu.add_checkbutton(label='A-Z', onvalue=True, offvalue=False, variable=a_zchecked, command=a_zchecked_handler) # Later add a command to sort A-Z
    sort_menu.add_checkbutton(label='Z-A', onvalue=True, offvalue=False, variable=z_achecked, command=z_achecked_handler) # Later add a command to sort Z-A
    # Add separator
    sort_menu.add_separator()
    # To do with date
    sort_menu.add_checkbutton(label='Latest', onvalue=True, offvalue=False, variable=latest_checked, command=latest_checked_handler) # Later add a command to filter by date
    sort_menu.add_checkbutton(label='Earliest', onvalue=True, offvalue=False, variable=earliest_checked, command=earliest_checked_handler) # Later add a command to filter by date
    # add separator
    sort_menu.add_separator()
    # to do with income and expense
    sort_menu.add_checkbutton(label='Income', onvalue=True, offvalue=False) # Later add a command to filter by income
    sort_menu.add_checkbutton(label='Expense', onvalue=True, offvalue=False) # Later add a command to filter by expense

    sort_button = tk.Button(main_window, text='Filter', command=lambda: sort_menu.post(sort_button.winfo_rootx(), sort_button.winfo_rooty() + sort_button.winfo_height()))
    sort_button.grid(row=4, column=0, padx=10, pady=5)
    sort_button.bind('<Button-1>', lambda event: sort_menu.post(event.x_root, event.y_root))



    # Bind the search entry to the key release event
    #search_entry.bind('<KeyRelease>', display_transactions())

    # Function to add the placeholder text
    def add_placeholder(event=None):
        if not search_entry.get():
            search_entry.insert(0, search_placeholder)
            search_entry.config(fg=placeholder_color)

    # Function to remove the placeholder text
    def remove_placeholder(event=None):
        if search_entry.get() == search_placeholder:
            search_entry.delete(0, tk.END)
            search_entry.config(fg=normal_color)

    # Bind events to the entry
    search_entry.bind('<FocusIn>', remove_placeholder)
    search_entry.bind('<FocusOut>', add_placeholder)
    search_entry.bind('<KeyRelease>', lambda event: display_transactions())

    add_placeholder() # Add the placeholder initially

    def delete_transaction():
        transaction_id = int(transaction_id_entry.get())
        # validate the transaction id
        if validate.is_positive_number(transaction_id) == False:
            messagebox.showerror('Error', 'Transaction ID isnt valid')
            return
        db.delete_transaction(transaction_id)
        display_transactions()
        update_summary()
        clear_entries()

    # Setting up transaction delete entry
    transaction_id_label = tk.Label(main_window, text='Transaction ID to delete: ')
    transaction_id_label.grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
    transaction_id_entry = tk.Entry(main_window)
    transaction_id_entry.grid(row=6, column=1, padx=10, pady=5)
    # Setting up delete button
    delete_button = tk.Button(main_window, text='Delete Transaction', command=delete_transaction)
    delete_button.grid(row=6, column=2, columnspan=2, pady=10)


    ### Summary section ###
    summary_label = tk.Label(main_window, text='Transaction summary', font=('Helvetica', 14))
    summary_label.grid(row=7, column=0, columnspan=4, pady=10)

    summary_txt = tk.Text(main_window, width=40, height=5)
    summary_txt.grid(row=8, column=0, columnspan=4, pady=20)

    def update_summary():
        transactions = db.get_transactions(current_user_id)
        total_income = 0
        total_expenses = 0

        for transaction in transactions:
            amount = transaction[2]
            if amount > 0:
                total_income += amount
            else:
                total_expenses += -amount # Minus because we need to make expenses positive for display
        # Work out balance
        balance = total_income - total_expenses

        summary_txt.delete(1.0, tk.END)
        summary_txt.insert(tk.END, f'Total income: {total_income} \n')
        summary_txt.insert(tk.END, f'Total expenses: {total_expenses} \n')
        summary_txt.insert(tk.END, f'Balance: {balance}')

    display_transactions() # Shpws all existing transactions

    update_summary() # Update the summary initially

if __name__ == '__main__':
    root = tk.Tk()
    create_main_window(root, 1)
    root.mainloop()