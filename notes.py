import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
import time

class NotesApp:
    def __init__(self, root, username, file_path=None):
        self.root = root
        self.username = username
        self.user_notes_dir = os.path.abspath(os.path.join("users", self.username, "notes"))
        os.makedirs(self.user_notes_dir, exist_ok=True)

        # Normalize file path
        if file_path and os.path.abspath(file_path).startswith(self.user_notes_dir):
            self.file_path = os.path.abspath(file_path)
        else:
            self.file_path = None

        self.root.title("PseudoOS Notes")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")
        self.build_ui()

        if self.file_path:
            self.load_file()

    def build_ui(self):
        self.text = tk.Text(
            self.root, font=("Courier New", 16),
            bg="black", fg="#00FF00",
            insertbackground="#00FF00", wrap="word"
        )
        self.text.pack(fill="both", expand=True, padx=10, pady=(10, 0))

        btn_frame = tk.Frame(self.root, bg="black")
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame, text="Save", command=self.save_file, bg="black", fg="#00FF00").pack(side="left", padx=10)
        tk.Button(btn_frame, text="Save As", command=self.save_as, bg="black", fg="#00FF00").pack(side="left", padx=10)
        tk.Button(btn_frame, text="Exit", command=self.root.destroy, bg="black", fg="#00FF00").pack(side="right", padx=10)

    def save_file(self):
        if not self.file_path:
            self.save_as()
            return

        normalized_path = os.path.abspath(self.file_path)
        if not normalized_path.startswith(self.user_notes_dir):
            messagebox.showerror("Access Denied", "You can only save files in your own Notes folder.")
            return

        try:
            with open(normalized_path, "w", encoding="utf-8") as f:
                f.write(self.text.get("1.0", tk.END))
            self.show_save_confirmation()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{e}")

    def save_as(self):
        file_path = filedialog.asksaveasfilename(
            initialdir=self.user_notes_dir,
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            title="Save As"
        )

        if file_path:
            normalized_path = os.path.abspath(file_path)
            if normalized_path.startswith(self.user_notes_dir):
                self.file_path = normalized_path
                self.save_file()
            else:
                messagebox.showerror("Access Denied", "You can only save files in your own Notes folder.")

    def load_file(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.text.insert("1.0", content)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load file:\n{e}")

    def show_save_confirmation(self):
        timestamp = time.strftime("[%H:%M:%S]")
        self.root.title(f"PseudoOS Notes - Saved {timestamp}")

if __name__ == "__main__":
    username = sys.argv[1] if len(sys.argv) > 1 else "guest"
    file_path = sys.argv[2] if len(sys.argv) > 2 else None

    root = tk.Tk()
    app = NotesApp(root, username, file_path)
    root.mainloop()
