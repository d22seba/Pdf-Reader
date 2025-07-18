import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os

class PDFUploaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Upload GUI")
        self.root.geometry("400x200")

        self.pdf_path = None

        self.label = tk.Label(root, text="Keine Datei ausgewählt", fg="gray")
        self.label.pack(pady=10)

        self.upload_button = tk.Button(root, text="Hochladen", command=self.upload_pdf)
        self.upload_button.pack(pady=5)

        self.submit_button = tk.Button(root, text="Abschicken", command=self.submit_pdf)
        self.submit_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Löschen", command=self.delete_pdf)
        self.delete_button.pack(pady=5)

    def upload_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF-Dateien", "*.pdf")])
        if file_path:
            self.pdf_path = file_path
            self.label.config(text=f"Ausgewählt: {os.path.basename(file_path)}", fg="black")

    def submit_pdf(self):
        if self.pdf_path:
            try:
                zielordner = os.getcwd()
                dateiname = os.path.basename(self.pdf_path)
                zielpfad = os.path.join(zielordner, dateiname)

                shutil.copy2(self.pdf_path, zielpfad)

                messagebox.showinfo("Erfolg", f"PDF wurde in '{zielordner}' gespeichert!")
            except Exception as e:
                messagebox.showerror("Fehler", f"Konnte Datei nicht speichern:\n{e}")
        else:
            messagebox.showwarning("Fehler", "Keine PDF ausgewählt!")

    def delete_pdf(self):
        self.pdf_path = None
        self.label.config(text="Keine Datei ausgewählt", fg="gray")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFUploaderApp(root)
    root.mainloop()
