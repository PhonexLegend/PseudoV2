
# os.py
"""
import tkinter as tk
from tkinter import messagebox

class SplashScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Pseudo OS")
        # Set the window to full screen
        self.master.attributes("-fullscreen", True)
        # Retro black background
        self.master.configure(bg="black")
        
        # Set a retro default font for all widgets using a tuple
        self.master.option_add("*Font", ("Courier New", 20, "bold"))
        
        # Create a frame to hold the content in the center
        content_frame = tk.Frame(self.master, bg="black")
        content_frame.pack(expand=True)
        
        # A retro title label at the top
        title_label = tk.Label(
            content_frame, 
            text="PSEUDO OS", 
            bg="black", 
            fg="#00FF00",  # using hex code for neon green
            font=("Courier New", 36, "bold")
        )
        title_label.pack(pady=(0, 50))
        
        # Create a frame to hold the buttons
        button_frame = tk.Frame(content_frame, bg="black")
        button_frame.pack()
        
        # "Boot Pseudo OS" button
        boot_button = tk.Button(
            button_frame, 
            text="Boot Pseudo OS", 
            width=20, 
            height=2,
            bg="black",
            fg="#00FF00",
            activebackground="gray",
            activeforeground="white",
            command=self.boot_os
        )
        boot_button.pack(pady=20)
        
        # "About" button
        about_button = tk.Button(
            button_frame, 
            text="About", 
            width=20, 
            height=2,
            bg="black",
            fg="#00FF00",
            activebackground="gray",
            activeforeground="white",
            command=self.show_about
        )
        about_button.pack(pady=20)
        
        # "Exit" button
        exit_button = tk.Button(
            button_frame, 
            text="Exit", 
            width=20, 
            height=2,
            bg="black",
            fg="#00FF00",
            activebackground="gray",
            activeforeground="white",
            command=self.exit_app
        )
        exit_button.pack(pady=20)
    
    def boot_os(self):
        # Placeholder function for booting the pseudo OS
        messagebox.showinfo("Booting", "Booting Pseudo OS...")
        # Here you can add code to launch your main pseudo OS interface
        
    def show_about(self):
        # Display a simple about message
        messagebox.showinfo("About", "Pseudo OS\nVersion 2.0\nDeveloped by PhonexLegend")
    
    def exit_app(self):
        # Exit the application
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SplashScreen(root)
    root.mainloop()
"""

# os.py
import tkinter as tk
from tkinter import messagebox
import subprocess

class SplashScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Pseudo OS")
        self.master.attributes("-fullscreen", True)
        self.master.configure(bg="black")
        self.master.option_add("*Font", ("Courier New", 20, "bold"))

        content_frame = tk.Frame(self.master, bg="black")
        content_frame.pack(expand=True)

        title_label = tk.Label(
            content_frame,
            text="PSEUDO OS",
            bg="black",
            fg="#00FF00",
            font=("Courier New", 36, "bold")
        )
        title_label.pack(pady=(0, 50))

        button_frame = tk.Frame(content_frame, bg="black")
        button_frame.pack()

        boot_button = tk.Button(
            button_frame,
            text="Boot Pseudo OS",
            width=20,
            height=2,
            bg="black",
            fg="#00FF00",
            activebackground="gray",
            activeforeground="white",
            command=self.boot_os
        )
        boot_button.pack(pady=20)

        about_button = tk.Button(
            button_frame,
            text="About",
            width=20,
            height=2,
            bg="black",
            fg="#00FF00",
            activebackground="gray",
            activeforeground="white",
            command=self.show_about
        )
        about_button.pack(pady=20)

        exit_button = tk.Button(
            button_frame,
            text="Exit",
            width=20,
            height=2,
            bg="black",
            fg="#00FF00",
            activebackground="gray",
            activeforeground="white",
            command=self.exit_app
        )
        exit_button.pack(pady=20)

    def boot_os(self):
        self.master.destroy()
        subprocess.run(["python3", "boot.py"])

    def show_about(self):
        messagebox.showinfo("About", "Pseudo OS\nVersion 2.0\nDeveloped by PhonexLegend")

    def exit_app(self):
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SplashScreen(root)
    root.mainloop()
