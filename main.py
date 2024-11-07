import tkinter as tk
from gui import create_main_window
from login_gui import create_welcome_window, create_login_window, create_registration_window
from database import create_table, create_user_table

def Main():
    # Create the neccesary tables
    try:
        create_user_table() # user table
        create_table() # transaction table
    except Exception as e:
        print(f'Error creating tables: {e}')

    # Create the root window (invisible until login)
    root = tk.Tk()
    root.title("Personal Finance Tracker - Welcome")

    # Create a welcome window
    create_welcome_window(root)

    # Start the Tkinter main loop
    root.resizable(False, False)
    root.mainloop()



if __name__ == "__main__":
    Main()

    # Add a toolbar on main window with buttons for settings, logout, and help
    # Add 2FA to the application
    # Add a way to view a summary of transactions
