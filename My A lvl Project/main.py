import tkinter as tk
import gui
#from gui import create_main_window
#from database import create_table

if __name__ == "__main__":
    #create_table() # Set up a table in database
    root = tk.Tk()
    root.title("Personal Finance Tracker")
    gui.create_main_window(root)
    root.mainloop()
