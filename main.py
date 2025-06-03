import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os

class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Resize Tool")
        self.root.geometry("800x850")
        self.root.config(bg="#0a0a0a")

        # Variabile interne pentru imagine si dimensiuni
        self.image_path = None
        self.original_image = None
        self.resized_image = None
        self.aspect_ratio = None
        self.last_edited = None  # Ne ajuta sa stim ce câmp a fost modificat (width sau height)

        self.font_style = ("Arial", 12)
        self.create_widgets()

    def create_widgets(self):
        # Titlul aplicatiei
        tk.Label(self.root, text="Image Resize Tool", font=("Arial", 20, "bold"),
                 fg="white", bg="#0a0a0a").pack(pady=15)

        # Placeholder pentru preview imagine
        self.image_label = tk.Label(self.root, text="No image loaded", bg="#2a2a2a", fg="white",
                                    width=70, height=25, relief="groove", bd=2)
        self.image_label.pack(pady=10)

        # Buton de incarcare a imaginii
        self.create_button("Choose Image", self.load_image, "#00bcd4").pack(pady=5)

        # Entry-uri pentru latime si inaltime
        self.width_entry = self.create_labeled_entry("New Width:")
        self.height_entry = self.create_labeled_entry("New Height:")

        # Ascultam modificarile in fiecare entry
        self.width_entry.bind("<KeyRelease>", lambda e: self.update_dimensions("width"))
        self.height_entry.bind("<KeyRelease>", lambda e: self.update_dimensions("height"))

        # Dropdown pentru formatul de salvare
        self.format_var = tk.StringVar(value="PNG")
        format_frame = tk.Frame(self.root, bg="#0a0a0a")
        format_frame.pack(pady=5)
        tk.Label(format_frame, text="Save Format:", font=self.font_style,
                 fg="white", bg="#0a0a0a").pack(side=tk.LEFT, padx=5)

        # Lista de formate suportate
        self.supported_formats = ["PNG", "JPG", "BMP", "GIF", "TIFF", "WEBP"]
        format_menu = ttk.Combobox(format_frame, textvariable=self.format_var,
                                   values=self.supported_formats, state="readonly", width=10)
        format_menu.pack(side=tk.LEFT)

        # Progress bar pentru statusul operatiunii
        self.progress = ttk.Progressbar(self.root, length=300, mode="determinate")
        self.progress.pack(pady=10)

        # Butonul de resize + save
        self.create_button("Resize & Save", self.resize_image, "#003366").pack(pady=10)

    def create_labeled_entry(self, label_text):
        # Creeaza un entry (input) cu eticheta
        frame = tk.Frame(self.root, bg="#0a0a0a")
        frame.pack(pady=5)
        tk.Label(frame, text=label_text, font=self.font_style,
                 fg="white", bg="#0a0a0a").pack(side=tk.LEFT, padx=5)
        entry = tk.Entry(frame, font=self.font_style, fg="white", bg="#2a2a2a",
                         insertbackground='white', relief="flat", width=10)
        entry.pack(side=tk.LEFT, padx=5)
        return entry

    def create_button(self, text, command, color):
        # Creeaza un buton
        return tk.Button(self.root, text=text, command=command,
                         font=self.font_style, fg="white", bg=color,
                         activebackground=color, activeforeground="white",
                         relief="flat", padx=10, pady=7, bd=0,
                         highlightthickness=0)

    def load_image(self):
        # Deschide dialogul de alegere fisier si incarca imaginea selectata
        path = filedialog.askopenfilename(filetypes=[
            ("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff;*.webp")])
        if path:
            self.image_path = path
            self.original_image = Image.open(path)

            # Calculam aspect ratio-ul original
            self.aspect_ratio = self.original_image.height / self.original_image.width

            # Populam entry-urile cu dimensiunile imaginii originale
            self.width_entry.delete(0, tk.END)
            self.width_entry.insert(0, str(self.original_image.width))
            self.height_entry.delete(0, tk.END)
            self.height_entry.insert(0, str(self.original_image.height))

            # Afisam preview-ul imaginii
            self.show_preview(self.original_image)
            self.image_label.config(text="")

    def show_preview(self, image):
        # Reda o versiune micșorata (thumbnail) în UI
        preview_img = image.copy()
        preview_img.thumbnail((400, 300))
        tk_img = ImageTk.PhotoImage(preview_img)
        self.image_label.configure(image=tk_img)
        self.image_label.image = tk_img  # salvăm referința ca să nu fie garbage collected

    def update_dimensions(self, changed_field):
        # Actualizeaza width/height ca sa pastreze aspect ratio
        if self.original_image is None or self.aspect_ratio is None:
            return

        self.last_edited = changed_field
        try:
            if changed_field == "width":
                new_width = int(self.width_entry.get())
                new_height = int(new_width * self.aspect_ratio)
                self.height_entry.delete(0, tk.END)
                self.height_entry.insert(0, str(int(new_height)))
            elif changed_field == "height":
                new_height = int(self.height_entry.get())
                new_width = int(new_height / self.aspect_ratio)
                self.width_entry.delete(0, tk.END)
                self.width_entry.insert(0, str(int(new_width)))
        except ValueError:
            # Daca inputul nu e valid (ex: text), ignoram
            pass

    def resize_image(self):
        # Redimensioneaza si salveaza imaginea in formatul ales
        if self.original_image is None:
            messagebox.showerror("Error", "No image loaded")
            return

        try:
            # Preluam noile dimensiuni
            new_width = int(self.width_entry.get())
            new_height = int(self.height_entry.get())

            # Pornim progress bar-ul
            self.progress["value"] = 20
            self.root.update_idletasks()

            # Facem resize efectiv
            self.resized_image = self.original_image.resize((new_width, new_height))
            self.show_preview(self.resized_image)

            self.progress["value"] = 50
            self.root.update_idletasks()

            # Pregatim salvarea
            output_folder = "output"
            os.makedirs(output_folder, exist_ok=True)

            base_name = "Resized image"
            selected_format = self.format_var.get()
            ext = f".{selected_format.lower()}"
            counter = 1
            save_path = os.path.join(output_folder, base_name + ext)

            # Evitam sa suprascriem fisiere
            while os.path.exists(save_path):
                counter += 1
                save_path = os.path.join(output_folder, f"{base_name} ({counter}){ext}")

            # Unele formate trebuie denumite altfel în PIL
            save_format = "JPEG" if selected_format == "JPG" else selected_format

            # Salvam imaginea
            self.resized_image.save(save_path, format=save_format)

            self.progress["value"] = 100
            self.root.update_idletasks()

            messagebox.showinfo("Success", f"Image resized & saved to:\n{save_path}")
            self.progress["value"] = 0  # Resetam progress bar-ul

        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
            self.progress["value"] = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageResizerApp(root)
    root.mainloop()
