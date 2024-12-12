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
        self.main_window.geometry('500x600')
        self.main_window.maxsize(500, 600)
        self.main_window.minsize(300, 350)
        #self.main_window.resizable(False, False)

        self.a_zchecked = tk.BooleanVar()
        self.z_achecked = tk.BooleanVar()
        self.latestchecked = tk.BooleanVar()
        self.oldestchecked = tk.BooleanVar()
        self.incomechecked = tk.BooleanVar()
        self.expensechecked = tk.BooleanVar()

        # Call setup functions for the layout and functionality
        self.setup_menu()
        self.setup_layout()
        self.medium_font()
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
        theme_menu.add_radiobutton(label='Light Theme', command=self.light_mode)
        theme_menu.add_radiobutton(label='Dark Theme', command=self.dark_mode)
        theme_menu.add_radiobutton(label='Contrast Theme', command=self.contrast_mode)
        settings_menu.add_cascade(label='Change Theme', menu=theme_menu)

        # submenu for changing font size
        font_menu = tk.Menu(settings_menu, tearoff=0)
        font_menu.add_radiobutton(label='Small', command=self.small_font)
        font_menu.add_radiobutton(label='Medium', command=self.medium_font)
        font_menu.add_radiobutton(label='Large', command=self.large_font)
        settings_menu.add_cascade(label='Change Font Size', menu=font_menu)
        menubar.add_cascade(label='Settings', menu=settings_menu)

        # Logout menu button
        menubar.add_command(label='Logout', command=self.on_closing)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label='About')
        menubar.add_cascade(label='Help', menu=help_menu)

        self.main_window.config(menu=menubar)


    def setup_layout(self):
        # Welcome label
        self.welcome_label = tk.Label(self.main_window, text="Welcome to Personal Finance Tracker!", anchor='center')
        self.welcome_label.grid(row=0, column=0, columnspan=4, pady=20, sticky='ew')

        # Balance label
        self.balance_label = tk.Label(self.main_window, text="Your balance", anchor='center')
        self.balance_label.grid(row=1, column=0, columnspan=4, pady=20, sticky='ew')

        # Summary balance
        self.summary_txt = tk.Text(self.main_window, height=5, width=30)
        self.summary_txt.grid(row=2, column=0, columnspan=4, pady=20, sticky='ew')

        # Configure column weights to make widgets expand with window resize
        for i in range(4):
            self.main_window.grid_columnconfigure(i, weight=1)


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
        self.main_window.config(bg="black")
        self.welcome_label.config(bg="black", fg="white")
        self.balance_label.config(bg="black", fg="white")
        self.summary_txt.config(bg="black", fg="white")

    def light_mode(self):
        self.main_window.config(bg="white")
        self.welcome_label.config(bg="white", fg="black")
        self.balance_label.config(bg="white", fg="black")
        self.summary_txt.config(bg="white", fg="black")

    def contrast_mode(self):
        # Blue background, yellow writing
        self.main_window.config(bg="blue")
        self.welcome_label.config(bg="blue", fg="yellow")
        self.balance_label.config(bg="blue", fg="yellow")
        self.summary_txt.config(bg="blue", fg="yellow")

    def small_font(self):
        self.welcome_label.config(font=("Arial", 8))
        self.balance_label.config(font=("Arial", 8))
        self.summary_txt.config(font=("Arial", 8))

    def medium_font(self):
        self.welcome_label.config(font=("Arial", 12))
        self.balance_label.config(font=("Arial", 12))
        self.summary_txt.config(font=("Arial", 12))

    def large_font(self):
        self.welcome_label.config(font=("Arial", 16))
        self.balance_label.config(font=("Arial", 16))
        self.summary_txt.config(font=("Arial", 16))

    def on_closing(self):
        self.main_window.withdraw()
        self.root.deiconify()

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    main_window = MainWindow(tk.Toplevel(root), current_user_id=2, root=root)
    root.mainloop()