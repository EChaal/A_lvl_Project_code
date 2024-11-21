import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import database as db
from validator import DataValidator
import export

class MainWindow:
    def __init__(self, main_window, current_user_id, root):
        self.main_window = main_window
        self.current_user_id = current_user_id
        self.root = root
        self.validate = DataValidator()

        # Set up main window properties
        self.main_window.title('Personal Finance Tracker - Main Window')
        self.main_window.resizable(False, False)

        self.a_zchecked = tk.BooleanVar()
        self.z_achecked = tk.BooleanVar()
        self.latestchecked = tk.BooleanVar()
        self.oldestchecked = tk.BooleanVar()
        self.incomechecked = tk.BooleanVar()
        self.expensechecked = tk.BooleanVar()

        # Call setup functions for the layout and functionality
        self.setup_layout()
        self.setup_transactions_tree()
        self.display_transactions()
        self.update_summary()
        self.add_placeholder()

        # Make root window show again when this window is closed
        self.main_window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_layout(self):
        tk.Label(self.main_window, text="Welcome to Personal Finance Tracker!").grid(row=0, column=0, columnspan=4, pady=20)

        # Description and Amount fields
        tk.Label(self.main_window, text='Description: ').grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.description_entry = tk.Entry(self.main_window)
        self.description_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.main_window, text='Amount: ').grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        self.amount_entry = tk.Entry(self.main_window)
        self.amount_entry.grid(row=2, column=1, padx=10, pady=5)

        # Radio buttons for transaction type
        self.transaction_type = tk.StringVar(value='expense')
        tk.Radiobutton(self.main_window, text='Income', variable=self.transaction_type, value='income').grid(row=2, column=2, padx=10, pady=5, sticky=tk.W)
        tk.Radiobutton(self.main_window, text='Expense', variable=self.transaction_type, value='expense').grid(row=2, column=3, padx=10, pady=5, sticky=tk.W)

        # Date entry
        tk.Label(self.main_window, text='Date (YY-MM-DD): ').grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.date_entry = DateEntry(self.main_window, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yy-mm-dd')
        self.date_entry.grid(row=3, column=1, padx=10, pady=5)

        # Buttons
        self.add_transaction_buitton = tk.Button(self.main_window, text='Add Transaction', command=self.add_transaction).grid(row=3, column=2, columnspan=2, padx=10, pady=5)
        self.reset_filter_button = tk.Button(self.main_window, text='Reset Filter', command=self.reset_filter).grid(row=4, column=1, padx=10, pady=5)
        self.delete_transaction_button = tk.Button(self.main_window, text='Delete Transaction', command=self.delete_transaction).grid(row=6, column=2, columnspan=2, pady=10)
        self.export_transactions_button = tk.Button(self.main_window, text='Export All Transactions', command=export.export_transactions_to_csv).grid(row=7, column=0, columnspan=4, pady=10)

        # Summary label
        self.summary_label = tk.Label(self.main_window, text='Transaction summary', font=('Helvetica', 14)).grid(row=8, column=0, columnspan=4, pady=10)
        self.summary_txt = tk.Text(self.main_window, width=40, height=5)
        self.summary_txt.grid(row=9, column=0, columnspan=4, pady=20)

        # Transaction ID field for deletion
        self.transaction_delete_label = tk.Label(self.main_window, text='Transaction ID to delete: ').grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
        self.transaction_id_entry = tk.Entry(self.main_window)
        self.transaction_id_entry.grid(row=6, column=1, padx=10, pady=5)

        # Define placeholders and colors for search entry
        self.search_placeholder = 'Search by description'
        self.placeholder_color = 'grey'
        self.normal_color = 'black'

        # Search entry
        self.search_entry = tk.Entry(self.main_window)
        self.search_entry.grid(row=4, column=2, columnspan=2, padx=10, pady=5)

        # bind search entry to placeholder functions
        # Bind events to the entry
        self.search_entry.bind('<FocusIn>', self.remove_placeholder)
        self.search_entry.bind('<FocusOut>', self.add_placeholder)
        self.search_entry.bind('<KeyRelease>', lambda event: self.display_transactions())

        # Set up sort menu
        self.sort_menu = tk.Menu(self.main_window)

        self.sort_menu.add_checkbutton(label='A-Z', onvalue=True, offvalue=False, variable=self.a_zchecked, command=self.a_zchecked_handler) # Later add a command to sort A-Z
        self.sort_menu.add_checkbutton(label='Z-A', onvalue=True, offvalue=False, variable=self.z_achecked, command=self.z_achecked_handler) # Later add a command to sort Z-A

        self.sort_menu.add_checkbutton(label='Latest', onvalue=True, offvalue=False, variable=self.latestchecked, command=self.latest_checked_handler) # Later add a command to filter by date
        self.sort_menu.add_checkbutton(label='Oldest', onvalue=True, offvalue=False, variable=self.oldestchecked, command=self.oldest_checked_handler) # Later add a command to filter by date

        self.sort_menu.add_separator()

        self.sort_menu.add_checkbutton(label='Income', onvalue=True, offvalue=False, variable=self.incomechecked, command=self.income_checked_handler)
        self.sort_menu.add_checkbutton(label='Expense', onvalue=True, offvalue=False, variable=self.expensechecked, command=self.expense_checked_handler)

        # Filter button that will have the sort menu as a dropdown
        self.filter_button = tk.Button(self.main_window, text='Filter', command=lambda: self.sort_menu.post(self.filter_button.winfo_rootx(), self.filter_button.winfo_rooty() + self.filter_button.winfo_height()))
        self.filter_button.grid(row=4, column=0, padx=10, pady=5)
        self.filter_button.bind('<Button-1>', lambda event: self.sort_menu.post(event.x_root, event.y_root))

    def setup_transactions_tree(self):
        columns = ('ID', 'Description', 'Amount', 'Date')
        self.transactions_tree = ttk.Treeview(self.main_window, columns=columns, show='headings')

        # Define headings and column widths
        self.transactions_tree.heading('ID', text='ID')
        self.transactions_tree.heading('Description', text='Description')
        self.transactions_tree.heading('Amount', text='Amount')
        self.transactions_tree.heading('Date', text='Date')
        self.transactions_tree.column('ID', width=50)
        self.transactions_tree.column('Description', width=150)
        self.transactions_tree.column('Amount', width=100)
        self.transactions_tree.column('Date', width=100)

        # Add Treeview and scrollbar to layout
        self.transactions_tree.grid(row=5, column=0, columnspan=4, padx=10, pady=5)
        scrollbar = ttk.Scrollbar(self.main_window, orient='vertical', command=self.transactions_tree.yview)
        scrollbar.grid(row=5, column=3, sticky='ns')

    def clear_entries(self):
        self.amount_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.transaction_id_entry.delete(0, tk.END)
        self.date_entry.set_date(self.date_entry._date.today())

    def validate_transaction(self):
        # Check if user is logged in
        if self.current_user_id is None:
            messagebox.showerror('Error', 'Please log in to add a transaction')
            return

        # Validate transaction data
        desc = self.description_entry.get()
        amount = self.amount_entry.get()
        date = self.date_entry.get_date().strftime('%Y-%m-%d') # Get the date in the correct format

        # Validate description
        if self.validate.is_non_empty_string(desc) == False:
            messagebox.showerror('Error', 'Please enter a valid description')
            return

        # Validate amount
        if self.validate.is_non_empty_string(amount) == False or self.validate.is_positive_number(float(amount)) == False:
            messagebox.showerror('Error', 'Please enter a valid amount')
            return

        if self.validate.max_number(float(amount), 999999999) == False:
            messagebox.showerror('Error', 'Please enter a reasonable amount')
            return

        # Validate date
        if self.validate.in_future(date):
            messagebox.showerror('Error', 'Cannot enter date in the future')
            return

        # Return validated data in neccesary format
        desc = desc.capitalize()
        amount = float(amount)
        date = date # Already in correct format

        return desc, amount, date


    def add_transaction(self):
        # Transaction logic here, including validation
        validated_desc, validated_amount, validated_date = self.validate_transaction() # splits the validated data into separate variables
        user_id = self.current_user_id
        db.add_transaction(validated_desc, validated_amount, validated_date, user_id) # Add transaction to database
        self.display_transactions() # Displays transactions in tree view
        self.update_summary()
        self.clear_entries()

    def display_transactions(self):
        # Make sure a user is logged in
        if self.current_user_id is None:
            messagebox.showerror('Error', 'Please log in to view transactions')
            return

        # Delete all transactions from the tree view
        for row in self.transactions_tree.get_children():
            self.transactions_tree.delete(row)

        # Display transactions in tree view

        def apply_sort():
            query = ''
            if self.a_zchecked.get():
                query += ' ORDER BY description ASC'
            elif self.z_achecked.get():
                query += ' ORDER BY description DESC'
            elif self.latestchecked.get():
                query += ' ORDER BY date DESC'
            elif self.oldestchecked.get():
                query += ' ORDER BY date ASC'
            return db.sort_data(self.current_user_id, query)

        transactions = apply_sort() # Sorted transactions (if there was any sorting)
        if self.incomechecked.get():
            transactions = db.income_only(transactions) # shows only income transactions
        elif self.expensechecked.get():
            transactions = db.expense_only(transactions) # shows only expense transactions

        # Insert transactions into the tree view
        # If nothing in placeholder
        if self.search_entry.get() == self.search_placeholder:
            for transaction in transactions:
                self.transactions_tree.insert('', tk.END, values=transaction)
        else:
            # Apply filter based on search text
            search_text = self.search_entry.get().capitalize()
            transactions = db.transaction_search_description(search_text, transactions) # returns transactions that match the search text
            for transaction in transactions:
                self.transactions_tree.insert('', tk.END, values=transaction)

    def delete_transaction(self):
        # Delete transaction logic here, including validation
        transaction_id = self.transaction_id_entry.get()

        try:
            transaction_id = int(transaction_id)
        except ValueError:
            messagebox.showerror('Error', 'Please enter a valid transaction ID')
            return

        # Validate transaction ID
        if self.validate.is_positive_number(transaction_id) == False:
            messagebox.showerror('Error', 'Please enter a valid transaction ID')
            return

        # Check if transaction exists

        if db.transaction_exists(transaction_id) == False:
            messagebox.showerror('Error', 'Transaction does not exist')
            return

        # Check if transaction belongs to user
        if db.belongs_to_user(self.current_user_id, transaction_id) == False:
            messagebox.showerror('Error', 'Transaction does not belong to user')
            return

        # Remove transaction from database and refresh view
        db.delete_transaction(transaction_id)
        self.display_transactions()
        self.update_summary()
        self.clear_entries()

    def reset_filter(self):
        # Reset sorting and filters
        self.a_zchecked.set(0)
        self.z_achecked.set(0)
        self.latestchecked.set(0)
        self.oldestchecked.set(0)
        self.incomechecked.set(0)
        self.expensechecked.set(0)
        self.display_transactions()


    def update_summary(self):
        # Fetch transactions from the database and calculate totals
        transactions = db.get_transactions(self.current_user_id) # Second item in tuple is the amount
        self.total_income = 0
        self.total_expense = 0
        self.balance = 0

        for transaction in transactions:
            if transaction[2] > 0: # If the amount is greater than 0, it is income
                self.total_income += transaction[2]
            else:
                self.total_expense += transaction[2]

        self.balance = self.total_income + self.total_expense
        # Update summary text widget with totals and balance
        self.summary_txt.delete(1.0, tk.END)
        self.summary_txt.insert(tk.END, f'Total Income: £{self.total_income:.2f}\n')
        self.summary_txt.insert(tk.END, f'Total Expense: £{self.total_expense:.2f}\n')
        self.summary_txt.insert(tk.END, f'Balance: £{self.balance:.2f}')

    def add_placeholder(self, event=None):
        if not self.search_entry.get():
            self.search_entry.insert(0, self.search_placeholder)
            self.search_entry.config(fg=self.placeholder_color)

    def remove_placeholder(self, event=None):
        if self.search_entry.get() == self.search_placeholder:
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg=self.normal_color)

    def a_zchecked_handler(self):
        if self.a_zchecked.get():
            self.z_achecked.set(0)
            self.latestchecked.set(0)
            self.oldestchecked.set(0)
            self.display_transactions()

    def z_achecked_handler(self):
        if self.z_achecked.get():
            self.a_zchecked.set(0)
            self.latestchecked.set(0)
            self.oldestchecked.set(0)
            self.display_transactions()

    def latest_checked_handler(self):
        if self.latestchecked.get():
            self.oldestchecked.set(0)
            self.a_zchecked.set(0)
            self.z_achecked.set(0)
            self.display_transactions()

    def oldest_checked_handler(self):
        if self.oldestchecked.get():
            self.latestchecked.set(0)
            self.a_zchecked.set(0)
            self.z_achecked.set(0)
            self.display_transactions()

    def income_checked_handler(self):
        if self.incomechecked.get():
            self.expensechecked.set(0)
            self.display_transactions()

    def expense_checked_handler(self):
        if self.expensechecked.get():
            self.incomechecked.set(0)
            self.display_transactions()

    def on_closing(self):
        self.main_window.withdraw()
        self.root.deiconify()

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    main_window = MainWindow(tk.Toplevel(root), current_user_id=1, root=root)
    root.mainloop()