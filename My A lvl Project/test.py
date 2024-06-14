import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Simple Tkinter GUI")

# Set the size of the window
root.geometry("800x500+200+100")  # Width x Height + x-offset +y-offset

# Create a label widget
label = tk.Label(root, text="Enter something:")
label.pack(pady=10)  # Add the label to the window with some padding

# Create an entry widget
entry = tk.Entry(root, width=30)
entry.pack(pady=5)  # Add the entry to the window with some padding

# Create a button widget
def on_button_click():
    user_input = entry.get()
    label.config(text=f"You entered: {user_input}")

button = tk.Button(root, text="Submit", command=on_button_click)
button.pack(pady=10)  # Add the button to the window with some padding

# Run the main loop
root.mainloop()
