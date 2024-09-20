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
    root.mainloop()


if __name__ == "__main__":
    Main()

    # Add back button to login and registration to go back to the welcome window
    # Add 2FA to the application
    # Add a way such that there is a type to search feature in the application
    # Add a way to sort the transactions by date
    # Add a way to sort the transactions by amount
    # Add a way to sort the transactions by the type of transaction
