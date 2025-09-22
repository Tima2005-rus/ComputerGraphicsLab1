import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Обработка изображения")

        frame_buttons = tk.Frame(root)
        frame_buttons.pack(side=tk.TOP, pady=5)

        btn_open = tk.Button(frame_buttons, text="Открыть", command=self.open_image)
        btn_open.pack(side=tk.LEFT, padx=5)

        btn_process = tk.Button(frame_buttons, text="Обработать", command=self.process_image)
        btn_process.pack(side=tk.LEFT, padx=5)

        btn_save = tk.Button(frame_buttons, text="Сохранить", command=self.save_image)
        btn_save.pack(side=tk.LEFT, padx=5)

        self.canvas = tk.Canvas(root, bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.image = None
        self.photo = None
        self.file_path = None

    def open_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JPEG files", "*.jpg;*.jpeg")]
        )
        if file_path:
            self.file_path = file_path
            self.image = Image.open(file_path).convert("RGB")
            self.show_image(self.image)

    def show_image(self, img):
        self.photo = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo)

    def process_image(self):
        if self.image:
            img = self.image.copy()
            width, height = img.size
            pixels = img.load()

            pixels[0, 0] = (64, 255, 255)  # верхний левый угол
            pixels[width - 1, 0] = (64, 127, 64)  # верхний правый угол
            pixels[width // 2, height - 1] = (127, 64, 64)  # центр нижней строки

            self.image = img
            self.show_image(img)

    def save_as_ppm(self, file_path):
        """Сохраняет изображение в формате PPM (ASCII)"""
        if self.image:
            img = self.image.convert("RGB")
            width, height = img.size
            pixels = img.load()

            with open(file_path, "w") as f:
                f.write("P3\n")
                f.write(f"{width} {height}\n")
                f.write("255\n")
                for y in range(height):
                    row = []
                    for x in range(width):
                        r, g, b = pixels[x, y]
                        row.append(f"{r} {g} {b}")
                    f.write(" ".join(row) + "\n")

    def save_image(self):
        if self.image:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("PPM ASCII files", "*.ppm")
                ]
            )
            if file_path:
                if file_path.lower().endswith(".ppm"):
                    self.save_as_ppm(file_path)
                else:
                    self.image.save(file_path, "PNG")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.geometry("1300x1000")
    root.mainloop()
