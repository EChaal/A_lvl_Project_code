import tkinter as tk
from tkinter import messagebox
import database as db
import gui
import globals
from validator import DataValidator
from security import hash_password

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
    # hide the root window
    root.withdraw()
    global current_user_id
    validate = DataValidator()
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
        # Validate the data
        if validate.is_non_empty_string(username) == False and validate.is_non_empty_string(password) == False and validate.is_valid_username(username) == False:
            messagebox.showerror('Error', 'Please enter a valid username and password')
            return
        # hashed password
        hashed_password = hash_password(password)
        # Get the userID from the database if login is successful
        user_id = db.check_user(username, hashed_password)

        if user_id:
            globals.current_user_id = user_id  # Set the current_user_id
            login_window.destroy()  # Close login window

            gui.create_main_window(tk.Toplevel(root), globals.current_user_id)  # Pass the root to create_main_window
        else:
            messagebox.showerror('Error', 'Invalid username or password')

    login_button = tk.Button(login_window, text='Login', command=login)
    login_button.grid(row=2, column=0, columnspan=2, pady=10)

def create_registration_window(root):
    # hide the root window
    root.withdraw()
    validate = DataValidator()
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

    email_label = tk.Label(registration_window, text='Email: ')
    email_label.grid(row=2, column=0, padx=10, pady=5)
    email_entry = tk.Entry(registration_window)
    email_entry.grid(row=2, column=1, padx=10, pady=5)

    phone_number_label = tk.Label(registration_window, text='Phone Number: ')
    phone_number_label.grid(row=3, column=0, padx=10, pady=5)
    phone_number_entry = tk.Entry(registration_window)
    phone_number_entry.grid(row=3, column=1, padx=10, pady=5)

    password_label = tk.Label(registration_window, text='Password: ')
    password_label.grid(row=4, column=0, padx=10, pady=5)
    password_entry = tk.Entry(registration_window, show='*')
    password_entry.grid(row=4, column=1, padx=10, pady=5)

    confirm_password_label = tk.Label(registration_window, text='Confirm Password: ')
    confirm_password_label.grid(row=5, column=0, padx=10, pady=5)
    confirm_password_entry = tk.Entry(registration_window, show='*')
    confirm_password_entry.grid(row=5, column=1, padx=10, pady=5)


    def register():
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        email = email_entry.get()
        phone_number = phone_number_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()
        if password != confirm_password:
            messagebox.showerror('Error', 'Passwords do not match')
            return
        # Validate the data
        if validate.is_non_empty_string(first_name) == False and validate.is_non_empty_string(last_name) == False:
            messagebox.showerror('Error', 'Please enter a valid first name, last name')
            return
        if validate.is_valid_email(email) == False:
            messagebox.showerror('Error', 'Please enter a valid email')
            return
        if validate.is_valid_phone_number(phone_number_entry.get()) == False:
            messagebox.showerror('Error', 'Please enter a valid phone number')
            return
        if validate.is_non_empty_string(password) == False or validate.length_check(password, 8, 'min') == False:
            messagebox.showerror('Error', 'Please enter a valid password (minimum 8 characters)')
            return
        # hashed password
        hashed_password = hash_password(password)
        # Add the user to the database
        username = db.add_user(first_name, last_name, hashed_password, email, phone_number)
        registration_window.destroy()

        # Display the username
        messagebox.showinfo('Registration Successful', f'Your username is: {username}')
        # show the root window
        root.deiconify()

    register_button = tk.Button(registration_window, text='Register', command=register)
    register_button.grid(row=6, column=0, columnspan=2, pady=10)
