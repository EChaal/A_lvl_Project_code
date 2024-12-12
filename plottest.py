import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import matplotlib.pyplot as plt

class PlotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Plotting App")

        self.values = []

        self.entry = ttk.Entry(root)
        self.entry.pack()

        self.add_button = ttk.Button(root, text="Add Value", command=self.add_value)
        self.add_button.pack()

        self.plot_button = ttk.Button(root, text="Plot Values", command=self.plot_values)
        self.plot_button.pack()

        self.figure = plt.Figure()
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, root)
        self.canvas.get_tk_widget().pack()

    def add_value(self):
        try:
            value = float(self.entry.get())
            self.values.append(value)
            self.entry.delete(0, tk.END)
        except ValueError:
            pass

    def plot_values(self):
        self.ax.clear()
        self.ax.plot(self.values, marker='o')
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = PlotApp(root)
    root.mainloop()