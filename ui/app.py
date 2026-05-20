import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from core.crypto import encrypt_file, decrypt_file
import os
import re

# Настройка внешнего вида (дизайна) интерфейса
def setup_style():
    style = ttk.Style()
    style.theme_use("clam")

    # Основной фон и цвета
    BG = "#f5f6fa"
    FG = "#2c3e50"

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

# Функция проверки надежности пароля
def check_strength(password):
    score = 0

    if len(password) >= 8: score += 1
    if len(password) >= 12: score += 1
    if re.search(r"[a-zA-Z]", password): score += 1
    if re.search(r"[0-9]", password): score += 1
    if re.search(r"[@$!%*?&._-]", password): score += 1

    weak_patterns = ["123", "1234", "12345", "123456", "qwerty", "password", "1111", "0000"]
    if any(p in password.lower() for p in weak_patterns):
        score -= 2

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
        self.root.geometry("520x470") # Увеличенное окно под новые кнопки

        # Вызов настройки стилей, который падал из-за отсутствия функции выше
        setup_style()

        self.filepath = ""
        self.folderpath = ""

        frame = ttk.Frame(root, padding=15)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="SecureFile Pro", style="Header.TLabel").pack(pady=10)

        self.label = ttk.Label(frame, text="Ничего не выбрано", wraplength=480)
        self.label.pack(pady=5)

        ttk.Button(frame, text="📁 Выбрать файл / .enc архив", command=self.select_file).pack(fill="x", pady=3)

        self.password = ttk.Entry(frame, show="*")
        self.password.pack(fill="x", pady=8)
        self.password.bind("<KeyRelease>", self.update_strength)

        self.strength_label = ttk.Label(frame, text="Сложность: -")
        self.strength_label.pack()

        ttk.Button(frame, text="🔒 Зашифровать файл", command=self.encrypt).pack(fill="x", pady=3)
        ttk.Button(frame, text="🔓 Расшифровать файл", command=self.decrypt).pack(fill="x", pady=3)

        ttk.Separator(frame).pack(fill="x", pady=10)

        ttk.Button(frame, text="📁 Выбрать папку для шифрования", command=self.select_folder).pack(fill="x", pady=3)
        ttk.Button(frame, text="🔐 Зашифровать папку (в .zip.enc)", command=self.encrypt_folder).pack(fill="x", pady=3)
        ttk.Button(frame, text="🔓 Расшифровать папку", command=self.decrypt_folder_ui).pack(fill="x", pady=3)

        self.status = ttk.Label(frame, text="")
        self.status.pack(pady=10)

    # ===== ВЫБОР ФАЙЛА =====
    def select_file(self):
        from tkinter import filedialog
        path = filedialog.askopenfilename()
        if path:
            self.filepath = path
            self.label.config(text=f"Выбран файл: {path}")

    # ===== ВЫБОР ПАПКИ =====
    def select_folder(self):
        from tkinter import filedialog
        path = filedialog.askdirectory()
        if path:
            self.folderpath = path
            self.label.config(text=f"Выбрана папка: {path}")

    # ===== ОБНОВЛЕНИЕ СЛОЖНОСТИ ПАРОЛЯ =====
    def update_strength(self, event=None):
        self.strength_label.config(
            text=f"Сложность: {check_strength(self.password.get())}"
        )

    # ===== ШИФРОВАНИЕ ФАЙЛА =====
    def encrypt(self):
        if not self.filepath:
            messagebox.showerror("Ошибка", "Выберите файл")
            return
        if not self.password.get():
            messagebox.showerror("Ошибка", "Введите пароль")
            return

        try:
            encrypt_file(self.filepath, self.password.get())
            self.status.config(text="Файл зашифрован, оригинал удален ✅")
            self.filepath = ""
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    # ===== РАСШИФРОВКА ФАЙЛА =====
    def decrypt(self):
        if not self.filepath:
            messagebox.showerror("Ошибка", "Выберите файл .enc")
            return

        try:
            decrypt_file(self.filepath, self.password.get())
            self.status.config(text="Файл расшифрован, .enc удален ✅")
            self.filepath = ""
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    # ===== ШИФРОВАНИЕ ПАПКИ =====
    def encrypt_folder(self):
        if not self.folderpath:
            messagebox.showerror("Ошибка", "Выберите папку")
            return
        if not self.password.get():
            messagebox.showerror("Ошибка", "Введите пароль")
            return

        try:
            from core.crypto import encrypt_folder as enc_f
            enc_f(self.folderpath, self.password.get())
            self.status.config(text="Папка успешно заархивирована и зашифрована ✅")
            self.folderpath = ""
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    # ===== РАСШИФРОВКА ПАПКИ =====
    def decrypt_folder_ui(self):
        if not self.filepath or not self.filepath.endswith('.zip.enc'):
            messagebox.showerror("Ошибка", "Для восстановления папки выберите файл формата .zip.enc через верхнюю кнопку!")
            return

        try:
            from core.crypto import decrypt_folder as dec_f
            dec_f(self.filepath, self.password.get())
            self.status.config(text="Папка успешно восстановлена, архив удален ✅")
            self.filepath = ""
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
