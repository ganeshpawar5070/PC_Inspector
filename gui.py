import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
from datetime import datetime

from system_info import *
from export import save_report
from logger import Logger

# ---------------------------
# Config / About Details
# ---------------------------
VERSION = "1.0.0"
DEVELOPER = "Ganesh Pawar"
EMAIL = "ganeshpawar5070@gmail.com"
GITHUB = "https://github.com/ganeshpawar5070"
LICENSE_TEXT = "Free for personal & educational use"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("PC Inspector v1.0")
        self.root.geometry("850x600")

        self.log_text = scrolledtext.ScrolledText(root, height=8)
        self.log_text.pack(fill="x")

        self.output = scrolledtext.ScrolledText(root)
        self.output.pack(fill="both", expand=True)

        self.logger = Logger(self.add_log)
        self.report = ""

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Scan", command=self.scan).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Save", command=self.save).pack(side="left", padx=5)
        tk.Button(btn_frame, text="About", command=self.about_window).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Exit", command=root.quit).pack(side="left", padx=5)

    def add_log(self, msg):
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")

    def show(self, title, data):
        self.output.insert("end", f"\n===== {title} =====\n")
        self.report += f"\n===== {title} =====\n"

        if isinstance(data, list):
            for item in data:
                for k, v in item.items():
                    self.output.insert("end", f"{k} : {v}\n")
                    self.report += f"{k} : {v}\n"
        else:
            for k, v in data.items():
                self.output.insert("end", f"{k} : {v}\n")
                self.report += f"{k} : {v}\n"

    def scan(self):
        def run():
            self.output.delete("1.0", "end")
            self.report = ""

            now = datetime.now()
            self.show("SCAN TIME", {
                "Date": now.strftime("%d-%m-%Y"),
                "Time": now.strftime("%H:%M:%S")
            })

            self.show("SYSTEM", get_system_info())
            self.show("CPU", get_cpu_info())
            self.show("RAM", get_ram_info())
            self.show("STORAGE", get_storage_info())
            self.show("GPU", get_gpu_info())
            self.show("MOTHERBOARD", get_motherboard_info())
            self.show("BIOS", get_bios_info())
            self.show("NETWORK (IP Addresses)", get_network_info())
            self.show("MAC", {"MAC": get_mac()})

            self.logger.log("SUCCESS", "Scan Complete")

        threading.Thread(target=run).start()

    def save(self):
        try:
            pc_name = get_system_info()["PC Name"]
            path = save_report(pc_name, self.report)
            self.logger.log("SUCCESS", f"Saved: {path}")
        except Exception as e:
            self.logger.log("ERROR", f"Failed to save: {str(e)}")

    def about_window(self):
        messagebox.showinfo(
            "About PC Inspector",
            f"PC Inspector System Diagnostic Tool\n\n"
            f"Developer: {DEVELOPER}\n"
            f"Email: {EMAIL}\n"
            f"Version: {VERSION}\n"
            f"License: {LICENSE_TEXT}\n"
            f"GitHub: {GITHUB}\n"
            f"© 2026 {DEVELOPER}"
        )

def start_gui():
    root = tk.Tk()
    App(root)
    root.mainloop()