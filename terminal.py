import tkinter as tk
from tkinter import messagebox
import os
import sys
import time
import subprocess

class Terminal:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        # Base directory is the user's folder
        self.base_dir = os.path.abspath(os.path.join("users", self.username))
        self.current_dir = self.base_dir
        
        self.root.title("PseudoOS Terminal")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")
        self.root.option_add("*Font", ("Courier New", 14))
        
        # Text widget for output
        self.output = tk.Text(self.root, bg="black", fg="#00FF00", insertbackground="#00FF00", wrap="word")
        self.output.pack(fill="both", expand=True)
        self.output.config(state="disabled")
        
        # Entry widget for input
        self.input_entry = tk.Entry(self.root, bg="black", fg="#00FF00", insertbackground="#00FF00")
        self.input_entry.pack(fill="x")
        self.input_entry.bind("<Return>", self.process_command)
        self.input_entry.focus_set()
        
        self.print_prompt()

    def print_prompt(self):
        # Show prompt as the current directory relative to base_dir with "Home" as root.
        rel_path = os.path.relpath(self.current_dir, self.base_dir)
        if rel_path == ".":
            rel_path = "Home"
        else:
            rel_path = "Home/" + rel_path
        prompt = f"{rel_path}> "
        self.output.config(state="normal")
        self.output.insert(tk.END, prompt)
        self.output.config(state="disabled")
        self.input_entry.delete(0, tk.END)
        self.input_entry.focus_set()

    def process_command(self, event):
        command = self.input_entry.get().strip()
        self.output.config(state="normal")
        self.output.insert(tk.END, command + "\n")
        self.output.config(state="disabled")
        self.execute_command(command)
        self.print_prompt()

    def execute_command(self, command):
        if not command:
            return
        parts = command.split()
        cmd = parts[0]
        args = parts[1:]
        if cmd == "cd":
            self.change_directory(args)
        elif cmd == "ls":
            self.list_directory()
        elif cmd == "tree":
            self.tree_directory()
        elif cmd == "time":
            self.write_output(time.strftime("%H:%M:%S\n"))
        elif cmd == "notes":
            if args:
                filename = args[0]
                file_path = os.path.abspath(os.path.join(self.current_dir, filename))
                # Check file is within sandbox and is a .txt file
                if file_path.startswith(self.base_dir) and file_path.endswith(".txt") and os.path.isfile(file_path):
                    subprocess.Popen(["python3", "notes.py", self.username, file_path])
                else:
                    self.write_output("Error: File not found or invalid file type.\n")
            else:
                self.write_output("Usage: notes <file.txt>\n")
        elif cmd == "exit":
            self.root.destroy()
        else:
            self.write_output("Unknown command\n")

    def change_directory(self, args):
        if not args:
            new_path = self.base_dir
        else:
            new_path = os.path.join(self.current_dir, args[0])
        new_path = os.path.abspath(new_path)
        if new_path.startswith(self.base_dir) and os.path.isdir(new_path):
            self.current_dir = new_path
        else:
            self.write_output("Access Denied or Directory not found\n")

    def list_directory(self):
        try:
            items = os.listdir(self.current_dir)
            for item in items:
                self.write_output(item + "\n")
        except Exception as e:
            self.write_output("Error listing directory: " + str(e) + "\n")

    def tree_directory(self):
        def recurse(path, indent=""):
            try:
                items = os.listdir(path)
                items.sort()
                for item in items:
                    full_path = os.path.join(path, item)
                    self.write_output(indent + item + "\n")
                    if os.path.isdir(full_path):
                        recurse(full_path, indent + "    ")
            except Exception as e:
                self.write_output(indent + f"Error: {e}\n")
        recurse(self.current_dir)

    def write_output(self, text):
        self.output.config(state="normal")
        self.output.insert(tk.END, text)
        self.output.config(state="disabled")
        self.output.see(tk.END)

if __name__ == "__main__":
    username = sys.argv[1] if len(sys.argv) > 1 else "guest"
    root = tk.Tk()
    app = Terminal(root, username)
    root.mainloop()
