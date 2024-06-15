import tkinter as tk
from tkinter import ttk

class MyWindow:
    def __init__(self, root, given_title):
        self.root = root
        self.root.title(given_title)

        # Create a frame
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create a button
        self.button = ttk.Button(self.frame, text="Click Me", command=self.on_button_click)
        self.button.grid(row=0, column=0, pady=10)

        # Configure the grid to expand with the window
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
    #Creates a label
    def create_label(self, label_name, given_row, given_column):
        self.label = ttk.Label(self.frame, text=label_name)
        self.label.grid(row=given_row, column=given_column, pady=10)


    def on_button_click(self):
        self.label.config(text="Button Clicked!")

if __name__ == "__main__":
    root = tk.Tk()  # Create the main window instance
    app = MyWindow(root, 'testing')  # Pass the main window instance
    app.create_label('Hello :)', 1, 0)
    app.create_label('Hello again', 2, 0)
    root.mainloop()  # Start the Tkinter event loop
