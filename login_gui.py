import tkinter as tk
from tkinter import messagebox
import database as db
import gui
import globals

# Declare a global variable for the current user ID
current_user_id = None

def create_welcome_window(root):
    # Set up welcome window (root window)
    welcome_label = tk.Label(root, text="Welcome to the Personal Finance Tracker")
    welcome_label.grid(row=0, column=0, columnspan=2, pady=20)

    # Create a login button
    login_button = tk.Button(root, text='Login', command=lambda:create_login_window(root))
    login_button.grid(row=1, column=0, padx=10, pady=10)

    # Create a register button
    register_button = tk.Button(root, text='Register', command=lambda:create_registration_window(root))
    register_button.grid(row=1, column=1, padx=10, pady=10)

def create_login_window(root):
    global current_user_id

    # Create a separate window for login
    login_window = tk.Toplevel(root)
    login_window.title('Login')

    username_label = tk.Label(login_window, text='Username: ')
    username_label.grid(row=0, column=0, padx=10, pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.grid(row=0, column=1, padx=10, pady=5)

    password_label = tk.Label(login_window, text='Password: ')
    password_label.grid(row=1, column=0, padx=10, pady=5)
    password_entry = tk.Entry(login_window, show='*')
    password_entry.grid(row=1, column=1, padx=10, pady=5)


    def login():
        global current_user_id
        username = username_entry.get()
        password = password_entry.get()

        # Get the userID from the database if login is successful
        user_id = db.check_user(username, password)

        if user_id:
            globals.current_user_id = user_id  # Set the current_user_id
            login_window.destroy()  # Close login window

            # Show the main application window
            root.deiconify()  # Show the root window
            gui.create_main_window(tk.Toplevel(root), globals.current_user_id)  # Pass the root to create_main_window
        else:
            error_label = tk.Label(login_window, text='Incorrect username or password')
            error_label.grid(row=2, column=0, columnspan=2)

    login_button = tk.Button(login_window, text='Login', command=login)
    login_button.grid(row=2, column=0, columnspan=2, pady=10)

def create_registration_window(root):
    # Create a separate window for registration
    registration_window = tk.Toplevel(root)
    registration_window.title('Register')

    first_name_label = tk.Label(registration_window, text='First name: ')
    first_name_label.grid(row=0, column=0, padx=10, pady=5)
    first_name_entry = tk.Entry(registration_window)
    first_name_entry.grid(row=0, column=1, padx=10, pady=5)

    last_name_label = tk.Label(registration_window, text='Last name: ')
    last_name_label.grid(row=1, column=0, padx=10, pady=5)
    last_name_entry = tk.Entry(registration_window)
    last_name_entry.grid(row=1, column=1, padx=10, pady=5)

    password_label = tk.Label(registration_window, text='Password: ')
    password_label.grid(row=2, column=0, padx=10, pady=5)
    password_entry = tk.Entry(registration_window, show='*')
    password_entry.grid(row=2, column=1, padx=10, pady=5)

    def register():
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        password = password_entry.get()

        # Add the user to the database
        username = db.add_user(first_name, last_name, password)
        registration_window.destroy()

        # Display the username
        messagebox.showinfo('Registration Successful', f'Your username is: {username}')

    register_button = tk.Button(registration_window, text='Register', command=register)
    register_button.grid(row=3, column=0, columnspan=2, pady=10)
