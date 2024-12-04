import tkinter as tk

class FontSizeChanger:
    def __init__(self, root):
        self.root = root
        self.root.title("Font Size Changer")

        self.label = tk.Label(root, text="Sample Text", font=("Arial", 12))
        self.label.pack(pady=20)

        self.small_button = tk.Button(root, text="Small", command=self.set_small_font)
        self.small_button.pack(side=tk.LEFT, padx=10)

        self.medium_button = tk.Button(root, text="Medium", command=self.set_medium_font)
        self.medium_button.pack(side=tk.LEFT, padx=10)

        self.large_button = tk.Button(root, text="Large", command=self.set_large_font)
        self.large_button.pack(side=tk.LEFT, padx=10)
        self.light_mode_button = tk.Button(root, text="Light Mode", command=self.set_light_mode)
        self.light_mode_button.pack(side=tk.LEFT, padx=10)

        self.dark_mode_button = tk.Button(root, text="Dark Mode", command=self.set_dark_mode)
        self.dark_mode_button.pack(side=tk.LEFT, padx=10)

        self.contrast_mode_button = tk.Button(root, text="Contrast Mode", command=self.set_contrast_mode)
        self.contrast_mode_button.pack(side=tk.LEFT, padx=10)

    def set_light_mode(self):
        self.root.config(bg="white")
        self.label.config(bg="white", fg="black")
        self.small_button.config(bg="white", fg="black")
        self.medium_button.config(bg="white", fg="black")
        self.large_button.config(bg="white", fg="black")
        self.light_mode_button.config(bg="white", fg="black")
        self.dark_mode_button.config(bg="white", fg="black")
        self.contrast_mode_button.config(bg="white", fg="black")

    def set_dark_mode(self):
        self.root.config(bg="black")
        self.label.config(bg="black", fg="white")
        self.small_button.config(bg="black", fg="white")
        self.medium_button.config(bg="black", fg="white")
        self.large_button.config(bg="black", fg="white")
        self.light_mode_button.config(bg="black", fg="white")
        self.dark_mode_button.config(bg="black", fg="white")
        self.contrast_mode_button.config(bg="black", fg="white")

    def set_contrast_mode(self):
        self.root.config(bg="yellow")
        self.label.config(bg="yellow", fg="blue")
        self.small_button.config(bg="yellow", fg="blue")
        self.medium_button.config(bg="yellow", fg="blue")
        self.large_button.config(bg="yellow", fg="blue")
        self.light_mode_button.config(bg="yellow", fg="blue")
        self.dark_mode_button.config(bg="yellow", fg="blue")
        self.contrast_mode_button.config(bg="yellow", fg="blue")
    def set_small_font(self):
        self.label.config(font=("Arial", 8))

    def set_medium_font(self):
        self.label.config(font=("Arial", 12))

    def set_large_font(self):
        self.label.config(font=("Arial", 20))

if __name__ == "__main__":
    root = tk.Tk()
    app = FontSizeChanger(root)
    root.mainloop()