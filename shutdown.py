import tkinter as tk
import time
import random

shutdown_messages = [
    "[INFO] Saving session...",
    "[INFO] Unmounting drives...",
    "[INFO] Stopping services...",
    "[OK] Service manager shutdown complete.",
    "[INFO] Flushing write buffers...",
    "[OK] All data written to disk.",
    "[INFO] Logging out user...",
    "[OK] User session terminated.",
    "[INFO] Powering off network interfaces...",
    "[OK] Network interfaces disabled.",
    "[INFO] Terminating background processes...",
    "[OK] All processes have exited.",
    "[INFO] Shutting down core modules...",
    "[INFO] Disabling graphical interface...",
    "[OK] Display server stopped.",
    "[INFO] Halting system...",
    "[OK] Shutdown sequence complete."
]

class ShutdownScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Shutting Down...")
        self.root.configure(bg="black")
        self.root.attributes("-fullscreen", True)

        self.text_widget = tk.Text(self.root, bg="black", fg="#0f0", font=("Courier New", 12))
        self.text_widget.pack(fill="both", expand=True)
        self.text_widget.config(state="disabled")

        self.index = 0
        self.show_next_message()

        self.root.mainloop()

    def show_next_message(self):
        if self.index < len(shutdown_messages):
            msg = shutdown_messages[self.index]
            self.text_widget.config(state="normal")
            self.text_widget.insert(tk.END, msg + "\n")
            self.text_widget.see(tk.END)
            self.text_widget.config(state="disabled")
            self.index += 1
            self.root.after(random.randint(200, 500), self.show_next_message)
        else:
            self.root.after(1000, self.root.destroy)

if __name__ == "__main__":
    ShutdownScreen()
