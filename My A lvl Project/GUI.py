import tkinter as tk
from tkinter import ttk

class GUImaker:
    def __init__(self, root, title):
        self.root = root
        self.root.title(title)
        self.root.geometry("500x300")  # Sets the initial window size

        # Create a menu bar
        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)

        # Create a notebook (tab control)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=1, fill="both")

        # Initial tabs
        self.tabs = {}
        #self.add_tab("Settings")
        #self.add_tab("Help")

        # Dictionary to store widgets
        self.widgets = {"labels": [], "buttons": []}

        # Example of what can be done
        #self.create_label(self.tabs["Settings"], "Settings Label", 0, 0)
        #self.create_button(self.tabs["Settings"], "Settings Button", 1, 0)
        #self.create_label(self.tabs["Help"], "Help Label", 0, 0)
        #self.create_button(self.tabs["Help"], "Help Button", 1, 0)
    
    # Adds menus
    def add_menu(self, menu_name):
        menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=menu_name, menu=menu)
        return menu
    
    # Adds submenus to the parent menu that you want
    def add_submenu(self, parent_menu, submenu_name):
        submenu = tk.Menu(parent_menu, tearoff=0)
        parent_menu.add_cascade(label=submenu_name, menu=submenu)
        return submenu
    
    # Adds items into a specific menu/submenu
    def add_menu_item(self, menu, label, command, position=None):
        if position == None:
            menu.add_command(label=label, command=command)
        else:
            menu.insert_command(position, label=label, command=command)
    
    # Adds seperator to a specific menu
    def add_seperator(self, menu, position=None):
        if position == None:
            menu.add_seperator()
        else:
            menu.insert_seperator(position)
    
    # List of commands for the menus and submenus go here
    # Example
    def new_command(self):
        print('New Command has been executed')
    
    def open_command(self):
        print('Open command has been executed')
    
    def preferences_command(self):
        print('Preferences command has been executed')
    #These commands depend on what you want to happen inside menus. Add them after inheritance


    def add_tab(self, tab_name):
        tab_frame = ttk.Frame(self.notebook)
        tab_frame.grid_columnconfigure(0, weight=1)  # Center column
        tab_frame.grid_rowconfigure(0, weight=1)     # Center row
        self.notebook.add(tab_frame, text=tab_name)
        self.tabs[tab_name] = tab_frame

    def create_label(self, parent, text, row, column):
        label = tk.Label(parent, text=text)
        label.grid(row=row, column=column, padx=10, pady=10, sticky="nw")
        self.widgets["labels"].append(label)
        parent.grid_columnconfigure(column, weight=1)  # Center column
        parent.grid_rowconfigure(row, weight=1)        # Center row

    def create_button(self, parent, text, row, column):
        button = tk.Button(parent, text=text)
        button.grid(row=row, column=column, padx=10, pady=10, sticky="nw")
        self.widgets["buttons"].append(button)
        parent.grid_columnconfigure(column, weight=1)  # Center column
        parent.grid_rowconfigure(row, weight=1)        # Center row

if __name__ == "__main__":
    root = tk.Tk()
    app = GUImaker(root, title="Ahmed's test")
    
    file_menu = app.add_menu('File')
    app.add_menu_item(file_menu, 'New student', app.new_command)
    app.add_menu_item(file_menu, 'Open student', app.open_command, 0)
    settings_submenu = app.add_submenu(file_menu, 'Settings')
    app.add_menu_item(settings_submenu, 'preferences', app.preferences_command, 0)
    # Example of adding a new tab dynamically
    #app.add_tab("Login")
    #app.add_tab('Progress')
    #app.add_tab('File')
    #app.create_label(app.tabs["Login"], "Username", 0, 0)
    #app.create_button(app.tabs["Login"], "Submit", 1, 1)
    #app.create_label(app.tabs["Login"], "MOOOOOOREEE", 1, 0)

    root.mainloop()
