import tkinter as tk
from tkinter import messagebox
import subprocess
import time
import os
import sys
import datetime

class DesktopShell:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("PseudoOS Desktop")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")

        self.background = tk.Label(self.root, bg="black")
        self.background.place(relwidth=1, relheight=1)

        self.create_desktop_icons()

        self.taskbar = tk.Frame(self.root, bg="#222", height=40)
        self.taskbar.pack(side="bottom", fill="x")

        self.clock_label = tk.Label(self.taskbar, fg="#0f0", bg="#222", font=("Courier New", 14))
        self.clock_label.pack(side="right", padx=10)

        self.date_label = tk.Label(self.taskbar, fg="#0f0", bg="#222", font=("Courier New", 14))
        self.date_label.pack(side="right", padx=10)

        self.update_clock()

    def create_desktop_icons(self):
        icons = [
            ("My Computer", self.open_file_explorer),
            ("Terminal", self.launch_terminal),
            ("Notes", self.launch_notes),
            ("Calculator", self.launch_calculator),
            ("Snake Game", self.launch_snake),
            ("Shutdown", self.shutdown_system)
        ]

        for i, (label, command) in enumerate(icons):
            btn = tk.Button(
                self.root,
                text=label,
                font=("Courier New", 14),
                fg="#0f0",
                bg="black",
                activebackground="#111",
                activeforeground="#0f0",
                bd=0,
                command=command
            )
            btn.place(x=40, y=40 + i * 80, width=160, height=60)

    def update_clock(self):
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%A, %d %B %Y")
        self.clock_label.config(text=current_time)
        self.date_label.config(text=current_date)
        self.root.after(1000, self.update_clock)

    def launch_calculator(self):
        subprocess.Popen(["python3", "calculator.py", self.username])

    def launch_notes(self, file_path=None):
        args = ["python3", "notes.py", self.username]
        if file_path:
            args.append(file_path)
        subprocess.Popen(args)

    def launch_terminal(self):
        subprocess.Popen(["python3", "terminal.py", self.username])

    def launch_snake(self):
        subprocess.Popen(["python3", "snake.py", self.username])

    def open_file_explorer(self):
        subprocess.Popen(["python3", "my_computer.py", self.username])

    def shutdown_system(self):
        subprocess.Popen(["python3", "shutdown.py", self.username])
        self.root.after(2000, self.root.destroy)

if __name__ == "__main__":
    username = sys.argv[1] if len(sys.argv) > 1 else "guest"
    root = tk.Tk()
    app = DesktopShell(root, username)
    root.mainloop()
