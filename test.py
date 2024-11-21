import tkinter as tk
from tkinter import ttk

class UserWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Test Window")

        # Create a notebook (tab control)
        self.notebook = ttk.Notebook(self.root)

        # Create the frames for each tab
        self.overview_frame = ttk.Frame(self.notebook)
        self.add_transaction_frame = ttk.Frame(self.notebook)
        self.settings_frame = ttk.Frame(self.notebook)

        # Add the frames to the notebook
        self.notebook.add(self.overview_frame, text="Overview")
        self.notebook.add(self.add_transaction_frame, text="Add Transaction")
        self.notebook.add(self.settings_frame, text="Settings")

        # Pack the notebook to make it visible
        self.notebook.pack(expand=True, fill='both')

        # Add widgets to the overview frame
        self.overview_entry = ttk.Entry(self.overview_frame)
        self.overview_entry.pack(pady=10)
        self.overview_button = ttk.Button(self.overview_frame, text="Submit")
        self.overview_button.pack(pady=10)

        # Add widgets to the add transaction frame
        self.add_transaction_entry = ttk.Entry(self.add_transaction_frame)
        self.add_transaction_entry.pack(pady=10)
        self.add_transaction_button = ttk.Button(self.add_transaction_frame, text="Add")
        self.add_transaction_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = UserWindow(root)
    root.mainloop()