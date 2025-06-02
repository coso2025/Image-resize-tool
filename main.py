import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Resize Tool")
        self.root.geometry("500x550")
        self.root.config(bg="#1e1e1e")  # Dark mode background

        self.image_path = None
        self.original_image = None

        self.font_style = ("Arial", 12)

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Image Resize Tool", font=("Arial", 20, "bold"),
                 bg="#1e1e1e", fg="white").pack(pady=15)

        self.image_label = tk.Label(self.root, text="No image loaded", bg="#2e2e2e",
                                    fg="white", width=50, height=10, relief="groove", bd=2)
        self.image_label.pack(pady=10)

        self.create_button("Choose Image", self.load_image, "#00bcd4").pack(pady=5)

        self.width_entry = self.create_labeled_entry("New Width:")
        self.height_entry = self.create_labeled_entry("New Height:")

        self.create_button("Resize", self.resize_image, "#ff5252").pack(pady=10)
        self.create_button("Save Resized Image", self.save_image, "#ffa500").pack(pady=5)

    def create_labeled_entry(self, label_text):
        frame = tk.Frame(self.root, bg="#1e1e1e")
        frame.pack(pady=5)

        label = tk.Label(frame, text=label_text, font=self.font_style,
                         fg="white", bg="#1e1e1e")
        label.pack(side=tk.LEFT, padx=5)

        entry = tk.Entry(frame, font=self.font_style, fg="white", bg="#2e2e2e",
                         insertbackground='white', relief="flat", width=10,
                         highlightbackground="#444", highlightthickness=1)
        entry.pack(side=tk.LEFT, padx=5)

        return entry

    def create_button(self, text, command, color):
        return tk.Button(self.root, text=text, command=command,
                         font=self.font_style, fg="white", bg=color,
                         activebackground=color, activeforeground="white",
                         relief="flat", bd=0, padx=15, pady=7,
                         highlightthickness=1, highlightbackground="#1e1e1e", cursor="hand2")

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if path:
            self.image_path = path
            self.original_image = Image.open(path)
            self.show_thumbnail(self.original_image)
            self.image_label.config(text="Image Loaded!")

    def show_thumbnail(self, image):
        thumb = image.copy()
        thumb.thumbnail((200, 200))
        tk_img = ImageTk.PhotoImage(thumb)
        self.image_label.configure(image=tk_img, compound="top")
        self.image_label.image = tk_img

    def resize_image(self):
        if self.original_image is None:
            messagebox.showerror("Error", "No image loaded")
            return

        try:
            new_width = int(self.width_entry.get())
            new_height = int(self.height_entry.get())
            self.resized_image = self.original_image.resize((new_width, new_height))
            self.show_thumbnail(self.resized_image)
            messagebox.showinfo("Success", "Image resized successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def save_image(self):
        if hasattr(self, 'resized_image'):
            path = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
            if path:
                self.resized_image.save(path)
                messagebox.showinfo("Saved", "Image saved successfully!")
        else:
            messagebox.showerror("Error", "No resized image to save")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageResizerApp(root)
    root.mainloop()
