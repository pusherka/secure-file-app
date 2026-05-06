import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from core.crypto import encrypt_file, decrypt_file, get_all_files
import os
import re

def setup_style():
    style = ttk.Style()
    style.theme_use("clam")

    # основной фон
    BG = "#f5f6fa"
    FG = "#2c3e50"
    BTN = "#e1e6ef"

    style.configure("TFrame", background=BG)
    style.configure("TLabel", background=BG, foreground=FG)
    style.configure("TButton", padding=6)
    style.configure("TEntry", fieldbackground="white", foreground=FG)

    style.configure(
        "Header.TLabel",
        font=("Arial", 16, "bold"),
        background=BG,
        foreground=FG
    )




def check_strength(password):
    score = 0

    # длина
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1

    # буквы
    if re.search(r"[a-zA-Z]", password):
        score += 1

    # цифры
    if re.search(r"[0-9]", password):
        score += 1

    # спецсимволы
    if re.search(r"[@$!%*?&._-]", password):
        score += 1

    # слабые шаблоны
    weak_patterns = [
        "123", "1234", "12345", "123456",
        "qwerty", "password", "1111", "0000"
    ]

    if any(p in password.lower() for p in weak_patterns):
        score -= 2

    # итог
    if score <= 1:
        return "Слабый ❌"
    elif score <= 3:
        return "Средний ⚠️"
    else:
        return "Сильный ✅"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("SecureFile Pro")
        self.root.geometry("520x420")

        setup_style()

        self.filepath = ""
        self.folderpath = ""

        frame = ttk.Frame(root, padding=15)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="SecureFile Pro", style="Header.TLabel").pack(pady=10)

        self.label = ttk.Label(frame, text="Файл не выбран")
        self.label.pack(pady=5)

        ttk.Button(frame, text="📁 Выбрать файл", command=self.select_file).pack(fill="x", pady=3)

        self.password = ttk.Entry(frame, show="*")
        self.password.pack(fill="x", pady=8)
        self.password.bind("<KeyRelease>", self.update_strength)

        self.strength_label = ttk.Label(frame, text="Сложность: -")
        self.strength_label.pack()

        ttk.Button(frame, text="🔒 Зашифровать файл", command=self.encrypt).pack(fill="x", pady=3)
        ttk.Button(frame, text="🔓 Расшифровать файл", command=self.decrypt).pack(fill="x", pady=3)

        ttk.Separator(frame).pack(fill="x", pady=10)

        ttk.Button(frame, text="📁 Выбрать папку", command=self.select_folder).pack(fill="x", pady=3)
        ttk.Button(frame, text="🔐 Зашифровать папку", command=self.encrypt_folder).pack(fill="x", pady=3)

        self.status = ttk.Label(frame, text="")
        self.status.pack(pady=10)

    # ===== FILE =====
    def select_file(self):
        from tkinter import filedialog
        path = filedialog.askopenfilename()
        if path:
            self.filepath = path
            self.label.config(text=path)

    # ===== FOLDER =====
    def select_folder(self):
        from tkinter import filedialog
        path = filedialog.askdirectory()
        if path:
            self.folderpath = path
            self.label.config(text=path)

    # ===== PASSWORD =====
    def update_strength(self, event=None):
        self.strength_label.config(
            text=f"Сложность: {check_strength(self.password.get())}"
        )

    # ===== ENCRYPT =====
    def encrypt(self):
        if not self.filepath:
            messagebox.showerror("Ошибка", "Выберите файл")
            return

        encrypt_file(self.filepath, self.password.get())
        self.status.config(text="Файл зашифрован ✅")

    # ===== DECRYPT =====
    def decrypt(self):
        try:
            decrypt_file(self.filepath, self.password.get())
            self.status.config(text="Файл расшифрован ✅")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    # ===== FOLDER ENCRYPT =====
    def encrypt_folder(self):
        if not self.folderpath:
            messagebox.showerror("Ошибка", "Выберите папку")
            return

        files = get_all_files(self.folderpath)

        for f in files:
            try:
                encrypt_file(f, self.password.get())
            except:
                pass

        self.status.config(text="Папка зашифрована ✅")
