import tkinter as tk
from tkinter import messagebox
import os
import sys
import subprocess

class MyComputer:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "users", self.username))
        self.current_path = self.base_dir
        self.history = []

        self.root.title("My Computer - PseudoOS")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")

        self.root.option_add("*Font", ("Courier New", 14))

        self.build_ui()
        self.load_directory()

    def build_ui(self):
        top = tk.Frame(self.root, bg="black")
        top.pack(fill="x", pady=10)

        self.path_label = tk.Label(top, text="", fg="#00FF00", bg="black")
        self.path_label.pack(side="left", padx=20)

        back_btn = tk.Button(top, text="Back", command=self.go_back, bg="black", fg="#00FF00")
        back_btn.pack(side="right", padx=20)

        exit_btn = tk.Button(top, text="Exit", command=self.root.destroy, bg="black", fg="#00FF00")
        exit_btn.pack(side="right")

        self.content_frame = tk.Frame(self.root, bg="black")
        self.content_frame.pack(fill="both", expand=True)

    def load_directory(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        display_path = self.current_path.replace(self.base_dir, "Home")
        self.path_label.config(text=display_path)

        try:
            items = os.listdir(self.current_path)
            items.sort()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        for item in items:
            full_path = os.path.join(self.current_path, item)
            if os.path.isdir(full_path):
                btn = tk.Button(
                    self.content_frame, text=f"[Folder] {item}",
                    command=lambda p=full_path: self.open_folder(p),
                    fg="#00FF00", bg="black", anchor="w", relief="flat"
                )
            else:
                btn = tk.Button(
                    self.content_frame, text=f"[File]   {item}",
                    command=lambda p=full_path: self.open_file(p),
                    fg="#00FF00", bg="black", anchor="w", relief="flat"
                )
            btn.pack(fill="x", padx=40, pady=2)

    def open_folder(self, path):
        if not path.startswith(self.base_dir):
            messagebox.showwarning("Access Denied", "You cannot access files outside your own user directory.")
            return
        self.history.append(self.current_path)
        self.current_path = path
        self.load_directory()

    def go_back(self):
        if self.history:
            self.current_path = self.history.pop()
            self.load_directory()

    def open_file(self, path):
        if not path.startswith(self.base_dir):
            messagebox.showwarning("Access Denied", "You cannot access files outside your own user directory.")
            return
        if path.endswith(".txt"):
            subprocess.Popen(["python3", "notes.py", self.username, path])
        else:
            messagebox.showinfo("Info", "Only .txt files are supported.")

if __name__ == "__main__":
    username = sys.argv[1] if len(sys.argv) > 1 else "guest"
    root = tk.Tk()
    app = MyComputer(root, username)
    root.mainloop()
