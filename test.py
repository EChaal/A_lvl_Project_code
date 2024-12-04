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
        self.setup_menu()
        self.setup_layout()
        self.update_summary()

        # Make root window show again when this window is closed
        self.main_window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_menu(self):
        menubar = tk.Menu(self.main_window)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label='Add Transaction') # Add a command to open the add transaction window
        file_menu.add_command(label='Edit Transaction') # Add a command to open the edit transaction window
        file_menu.add_command(label='Export Transactions') # Add a command to export transactions to a CSV file
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.main_window.quit)
        menubar.add_cascade(label='File', menu=file_menu)

        # Summary menu - Acts as a button that opens a new window with a better summary of transactions
        menubar.add_command(label='Summary', command=print('Summary clicked'))

        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label='Change Password')
        settings_menu.add_command(label='Change Email')
        settings_menu.add_command(label='Set a goal')
        settings_menu.add_command(label='Add another user')

        # submenu for changing theme
        theme_menu = tk.Menu(settings_menu, tearoff=0)
        theme_menu.add_radiobutton(label='Light Theme')
        theme_menu.add_radiobutton(label='Dark Theme')
        theme_menu.add_radiobutton(label='Contrast Theme')
        settings_menu.add_cascade(label='Change Theme', menu=theme_menu)

        # submenu for changing font size
        font_menu = tk.Menu(settings_menu, tearoff=0)
        font_menu.add_radiobutton(label='Small')
        font_menu.add_radiobutton(label='Medium')
        font_menu.add_radiobutton(label='Large')

        # Logout menu button
        menubar.add_command(label='Logout', command=self.on_closing)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label='About')
        menubar.add_cascade(label='Help', menu=help_menu)

        self.main_window.config(menu=menubar)


    def setup_layout(self):
        # Welcome label
        self.welcome_label = tk.Label(self.main_window, text="Welcome to Personal Finance Tracker!")
        self.welcome_label.grid(row=0, column=0, columnspan=4, pady=20)

        self.balance_label = tk.Label(self.main_window, text="Your balance")
        self.balance_label.grid(row=1, column=0, columnspan=4, pady=20)

        self.summary_txt = tk.Text(self.main_window, height=5, width=30)
        self.summary_txt.grid(row=2, column=0, columnspan=4, pady=20)


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

    def dark_mode(self):
        pass
        self.main_window.config(bg="black")

    def on_closing(self):
        self.main_window.withdraw()
        self.root.deiconify()

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    main_window = MainWindow(tk.Toplevel(root), current_user_id=1, root=root)
    root.mainloop()