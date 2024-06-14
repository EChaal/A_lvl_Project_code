from validation import DataValidator
import tkinter as tk

### Creates login screen ###
def login_screen():
    login_window = tk.Tk()
    login_window.title('Login screen')
    login_window.geometry('800x500+200+100') # set size of the window

    ### USERNAME STUFF ###
    user_label = tk.Label(login_window, text='Enter username') # Label above where i will input name
    user_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

    user_entry = tk.Entry(login_window, width = 15) # Where I will be inputting username
    user_entry.grid(row=1, column=0, padx=10, pady=5)

    ### PASSWORD STUFF ###
    pass_label = tk.Label(login_window, text='Enter Password')
    pass_label.grid(row=3, column=0, columnspan=2, pady=10, padx=10)

    pass_entry = tk.Entry(login_window, width = 15) # Where I will be inputting password
    pass_entry.grid(row=4, column=0, padx=10, pady=5)

    ### Submit button ###
    def Submit():
        user_input = user_entry.get()
        user_label.config(text = f'You entered: {user_input}')
        pass_input = pass_entry.get()
        pass_label.config(text = f'You entered: {pass_input}')
    
    submit = tk.Button(login_window, text='Submit', command=Submit)
    submit.grid(row=4, column=1, padx=10, pady=5)


    login_window.mainloop()



validate = DataValidator()
login_screen()
