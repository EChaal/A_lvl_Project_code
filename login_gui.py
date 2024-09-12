import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import database as db

def create_welcome_window():
    # Create the root window
    root = tk.Tk()
    root.title("Personal Finance Tracker")

    # Create a login and registration window first
    def open_login_window():
        create_login_window(root)

    def open_registration_window():
        create_registration_window()

    welcome_label = tk.Label(root, text="Welcome to the Personal Finance Tracker")
    welcome_label.grid(row=0, column=0, columnspan=2, pady=20)

    register_button = tk.Button(root, text="Register", command=open_registration_window)
    register_button.grid(row=1, column=0, padx=10, pady=10)

    login_button = tk.Button(root, text="Login", command=open_login_window)
    login_button.grid(row=1, column=1, padx=10, pady=10)

    root.mainloop()


    

def create_login_window(root):
    #Create a separate window for login
    login_window = tk.Toplevel()
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
        username = username_entry.get()
        password = password_entry.get()
        # Add validation here later
        # Checks if the user exists in the database
        if db.check_user(username, password):
            login_window.destroy()
            root.deiconify()
        else:
            error_label = tk.Label(login_window, text='Incorrect username or password')
            error_label.grid(row=2, column=0, columnspan=2)
    
    login_button = tk.Button(login_window, text='Login', command=login)
    login_button.grid(row=2, column=0, columnspan=2, pady=10)

def create_registration_window():
    # Create a separate window for registration
    registration_window = tk.Toplevel()
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
        # Add validation here later
        # Add the user to the database
        username = db.add_user(first_name, last_name, password)
        registration_window.destroy()

        # Display the username
        messagebox.showinfo('Registration Successful', f'Your username is: {username}')

    register_button = tk.Button(registration_window, text='Register', command=register)
    register_button.grid(row=3, column=0, columnspan=2, pady=10)