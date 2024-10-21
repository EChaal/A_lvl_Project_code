import tkinter as tk
from tkinter import messagebox
import database as db
import gui
import globals
from validator import DataValidator
from security import hash_password
import otp
import random
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
    # hide the root window
    root.withdraw()
    global current_user_id
    validate = DataValidator()
    # Create a separate window for login
    login_window = tk.Toplevel(root)
    login_window.title('Login')
    login_window.resizable(False, False)

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

            gui.create_main_window(tk.Toplevel(root), globals.current_user_id, root)  # Pass the root to create_main_window
        else:
            messagebox.showerror('Error', 'Invalid username or password')

    login_button = tk.Button(login_window, text='Login', command=login)
    login_button.grid(row=2, column=0, columnspan=2, pady=10)

    def back_to_welcome(login_window, root):
        login_window.destroy()
        root.deiconify()

    back_button = tk.Button(login_window, text='Back', command=lambda:back_to_welcome(login_window, root))
    back_button.grid(row=3, column=0, columnspan=2, pady=10)

    def forgot_password():
        login_window.destroy()
        create_forgot_password_window(root)

    forgot_password_button = tk.Button(login_window, text='Forgot Password/Username', command=forgot_password)
    forgot_password_button.grid(row=4, column=0, columnspan=2, pady=10)

    # handle the close event
    login_window.protocol('WM_DELETE_WINDOW', lambda:back_to_welcome(login_window, root))

def create_forgot_password_window(root):
    root.withdraw()
    validate = DataValidator()
    forgot_password_window = tk.Toplevel(root)
    forgot_password_window.title('Forgot Password')
    forgot_password_window.resizable(False, False)

    email_label = tk.Label(forgot_password_window, text='Email: ')
    email_label.grid(row=0, column=0, padx=10, pady=5)

    email_entry = tk.Entry(forgot_password_window)
    email_entry.grid(row=0, column=1, padx=10, pady=5)

    def send_otp():
        email = email_entry.get()
        globals.current_user = db.get_username(email)
        if validate.is_valid_email(email) == False:
            messagebox.showerror('Error', 'Please enter a valid email')
            return
        # Send the OTP
        one_time_password = random.randint(100000, 999999)
        globals.otp = one_time_password
        otp.send_otp(email, one_time_password)

    send_otp_button = tk.Button(forgot_password_window, text='Send OTP', command=send_otp)
    send_otp_button.grid(row=1, column=0, columnspan=2, pady=10)

    otp_label = tk.Label(forgot_password_window, text='Enter OTP: ')
    otp_label.grid(row=2, column=0, padx=10, pady=5)

    otp_entry = tk.Entry(forgot_password_window)
    otp_entry.grid(row=2, column=1, padx=10, pady=5)

    def check_otp():
        entered_otp = int(otp_entry.get()) # integer to check against the OTP
        print(globals.otp)
        if entered_otp == globals.otp:
            messagebox.showinfo('OTP Verified', 'OTP is correct')
            forgot_password_window.destroy()
            create_reset_password_window(root)
        else:
            messagebox.showerror('Error', 'Invalid OTP')

    check_otp_button = tk.Button(forgot_password_window, text='Check OTP', command=check_otp)
    check_otp_button.grid(row=3, column=0, columnspan=2, pady=10)

    def back_to_login(forgot_password_window, root):
        forgot_password_window.destroy()
        create_login_window(root)

    back_button = tk.Button(forgot_password_window, text='Back to login', command=lambda:back_to_login(forgot_password_window, root))
    back_button.grid(row=4, column=0, columnspan=2, pady=10)

    # handle the close event
    forgot_password_window.protocol('WM_DELETE_WINDOW', lambda:back_to_login(forgot_password_window, root))

def create_reset_password_window(root):
    root.withdraw()
    validate = DataValidator()
    reset_password_window = tk.Toplevel(root)
    reset_password_window.title('Reset Password')
    reset_password_window.resizable(False, False)
    # Email should be sent to the user with username
    username_label = tk.Label(reset_password_window, text='Username: ' + globals.current_user)
    username_label.grid(row=0, column=0, padx=10, pady=5)

    new_password_label = tk.Label(reset_password_window, text='New Password: ')
    new_password_label.grid(row=1, column=0, padx=10, pady=5)
    new_password_entry = tk.Entry(reset_password_window, show='*')
    new_password_entry.grid(row=1, column=1, padx=10, pady=5)

    confirm_password_label = tk.Label(reset_password_window, text='Confirm Password: ')
    confirm_password_label.grid(row=2, column=0, padx=10, pady=5)
    confirm_password_entry = tk.Entry(reset_password_window, show='*')
    confirm_password_entry.grid(row=2, column=1, padx=10, pady=5)

    # function to reset the password
    def reset_password():
        new_password = new_password_entry.get()
        confirm_password = confirm_password_entry.get()

        # Check the password
        if new_password != confirm_password:
            messagebox.showerror('Error', 'Passwords do not match')
            return

        # Validate the password
        if validate.is_non_empty_string(new_password) == False or validate.length_check(new_password, 8, 'min') == False:
            messagebox.showerror('Error', 'Please enter a valid password (minimum 8 characters)')
            return

        # hash the password and update it in the database
        hashed_password = hash_password(new_password)
        db.update_password(globals.current_user, hashed_password)
        messagebox.showinfo('Password Reset', 'Password has been reset successfully')
        reset_password_window.destroy()
        root.deiconify()

    reset_password_button = tk.Button(reset_password_window, text='Reset Password', command=reset_password)
    reset_password_button.grid(row=3, column=0, columnspan=2, pady=10)

    def back_to_login(reset_password_window, root):
        reset_password_window.destroy()
        create_login_window(root)

    # Back button to go back to the welcome window
    back_button = tk.Button(reset_password_window, text='Back to login', command=lambda:back_to_login(reset_password_window, root))
    back_button.grid(row=4, column=0, columnspan=2, pady=10)

    # handle the close event
    reset_password_window.protocol('WM_DELETE_WINDOW', lambda:back_to_login(reset_password_window, root))


def create_registration_window(root):
    # hide the root window
    root.withdraw()
    validate = DataValidator()
    # Create a separate window for registration
    registration_window = tk.Toplevel(root)
    registration_window.title('Register')
    registration_window.resizable(False, False)

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

        # Check if email is already in use
        if db.email_exists(email):
            messagebox.showerror('Error', 'Email already in use')
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

    def back_to_welcome(registration_window, root):
        registration_window.destroy()
        root.deiconify()

    back_button = tk.Button(registration_window, text='Back', command=lambda:back_to_welcome(registration_window, root))
    back_button.grid(row=7, column=0, columnspan=2, pady=10)

    # handle the close event
    registration_window.protocol('WM_DELETE_WINDOW', lambda:back_to_welcome(registration_window, root))