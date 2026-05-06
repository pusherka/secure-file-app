import os
import tkinter as tk


class FileBrowser(tk.Toplevel):
    def __init__(self, root, callback):
        super().__init__(root)

        self.title("Выбор файла")
        self.geometry("500x400")

        self.callback = callback
        self.current_path = os.path.expanduser("~")

        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(self.listbox)
        scrollbar.pack(side="right", fill="y")

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        self.listbox.bind("<Double-1>", self.open_item)

        self.load(self.current_path)

    def load(self, path):
        self.current_path = path
        self.listbox.delete(0, tk.END)

        if os.path.dirname(path) != path:
            self.listbox.insert(tk.END, "..")

        for item in os.listdir(path):
            self.listbox.insert(tk.END, item)

    def open_item(self, event):
        item = self.listbox.get(self.listbox.curselection())

        if item == "..":
            self.load(os.path.dirname(self.current_path))
            return

        full = os.path.join(self.current_path, item)

        if os.path.isdir(full):
            self.load(full)
        else:
            self.callback(full)
            self.destroy()
