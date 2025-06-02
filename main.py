import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Resize Tool")
        self.root.geometry("500x550")
        self.root.config(bg="#f0f0f0")

        self.image_path = None
        self.original_image = None
        self.resized_image = None

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Image Resize Tool", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

        self.image_label = tk.Label(self.root, text="No image loaded", bg="#ccc", width=50, height=10)
        self.image_label.pack(pady=10)

        tk.Button(self.root, text="Choose Image", command=self.load_image, bg="#4CAF50", fg="white").pack(pady=5)

        self.width_entry = self.create_labeled_entry("New Width:")
        self.height_entry = self.create_labeled_entry("New Height:")

        self.keep_aspect_var = tk.BooleanVar()
        self.keep_aspect_check = tk.Checkbutton(self.root, text="Keep Aspect Ratio", variable=self.keep_aspect_var, bg="#f0f0f0")
        self.keep_aspect_check.pack(pady=5)

        tk.Button(self.root, text="Resize", command=self.resize_image, bg="#2196F3", fg="white").pack(pady=10)
        tk.Button(self.root, text="Save Resized Image", command=self.save_image, bg="#FF9800", fg="white").pack(pady=5)

    def create_labeled_entry(self, label_text):
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(pady=5)
        tk.Label(frame, text=label_text, bg="#f0f0f0").pack(side=tk.LEFT)
        entry = tk.Entry(frame)
        entry.pack(side=tk.LEFT)
        return entry

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
        self.image_label.configure(image=tk_img)
        self.image_label.image = tk_img

    def resize_image(self):
        if self.original_image is None:
            messagebox.showerror("Error", "No image loaded")
            return

        try:
            new_width = self.width_entry.get()
            new_height = self.height_entry.get()

            if not new_width and not new_height:
                raise ValueError("Please enter at least width or height")

            orig_width, orig_height = self.original_image.size

            if self.keep_aspect_var.get():
                if new_width:
                    new_width = int(new_width)
                    ratio = new_width / orig_width
                    new_height = int(orig_height * ratio)
                elif new_height:
                    new_height = int(new_height)
                    ratio = new_height / orig_height
                    new_width = int(orig_width * ratio)
                else:
                    raise ValueError("Enter at least one dimension")
            else:
                new_width = int(new_width)
                new_height = int(new_height)

            self.resized_image = self.original_image.resize((new_width, new_height), Image.ANTIALIAS)
            self.show_thumbnail(self.resized_image)
            messagebox.showinfo("Success", f"Image resized to {new_width} x {new_height}")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def save_image(self):
        if self.resized_image:
            path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
            if path:
                self.resized_image.save(path)
                messagebox.showinfo("Saved", "Image saved successfully!")
        else:
            messagebox.showerror("Error", "No resized image to save")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageResizerApp(root)
    root.mainloop()
