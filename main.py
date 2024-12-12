import tkinter as tk
from login_gui import create_login_window
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
    create_login_window(root)

    # Start the Tkinter main loop
    root.resizable(False, False)
    root.mainloop()



if __name__ == "__main__":
    Main()

    # Log in only
    # main window
    # first 3 users are admin
    # admin can add new users
    # admin can delete users
