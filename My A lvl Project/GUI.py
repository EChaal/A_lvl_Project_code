import tkinter as tk
from tkinter import ttk

class GUImaker:
    def __init__(self, root, title):
        self.root = root
        self.root.title(title)
        self.root.geometry("800x500")  # Sets the initial window size

        # Create a notebook (tab control)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=1, fill="both")

        # Initial tabs
        self.tabs = {}
        self.add_tab("Settings")
        self.add_tab("Help")

        # Dictionary to store widgets
        self.widgets = {"labels": [], "buttons": []}

        # Example usage
        self.create_label(self.tabs["Settings"], "Settings Label", 0, 0)
        self.create_button(self.tabs["Settings"], "Settings Button", 1, 0)
        self.create_label(self.tabs["Help"], "Help Label", 0, 0)
        self.create_button(self.tabs["Help"], "Help Button", 1, 0)

    def add_tab(self, tab_name):
        tab_frame = ttk.Frame(self.notebook)
        tab_frame.grid_columnconfigure(0, weight=1)  # Center column
        tab_frame.grid_rowconfigure(0, weight=1)     # Center row
        self.notebook.add(tab_frame, text=tab_name)
        self.tabs[tab_name] = tab_frame

    def create_label(self, parent, text, row, column):
        label = tk.Label(parent, text=text)
        label.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
        self.widgets["labels"].append(label)
        parent.grid_columnconfigure(column, weight=1)  # Center column
        parent.grid_rowconfigure(row, weight=1)        # Center row

    def create_button(self, parent, text, row, column):
        button = tk.Button(parent, text=text)
        button.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
        self.widgets["buttons"].append(button)
        parent.grid_columnconfigure(column, weight=1)  # Center column
        parent.grid_rowconfigure(row, weight=1)        # Center row

if __name__ == "__main__":
    root = tk.Tk()
    app = GUImaker(root, title="My Custom GUI")
    
    # Example of adding a new tab dynamically
    app.add_tab("NewTab")
    app.create_label(app.tabs["NewTab"], "New Tab Label", 0, 0)
    app.create_button(app.tabs["NewTab"], "New Tab Button", 1, 0)

    root.mainloop()
