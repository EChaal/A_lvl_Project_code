import tkinter as tk
from gui import create_main_window
from login_gui import create_welcome_window, create_login_window, create_registration_window
from database import create_table, create_user_table

if __name__ == "__main__":
    # Create the neccesary tables
    create_user_table() # user table
    create_table() # transaction table
    
    # Create the root window
    root = tk.Tk()
    root.title("Personal Finance Tracker")

    # Create a welcome window
    #create_welcome_window()

    create_main_window(root)
    root.mainloop()
    