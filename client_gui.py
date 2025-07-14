import tkinter as tk
from tkinter import ttk, messagebox
import configparser
import subprocess
import os
import sys

CONFIG_FILE = "config.ini"

DARK_BG = "#18192a"
CARD_BG = "#23243a"
TEXT_COLOR = "#e6e6f0"
ACCENT = "#a78bfa"
BUTTON_BG = "#393a4d"
BUTTON_FG = "#a78bfa"
ENTRY_BG = "#23243a"
ENTRY_FG = "#e6e6f0"


class ConfigApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("OBS Monitor Client Configurator")
        self.geometry("420x350")
        self.resizable(False, False)
        self.configure(bg=DARK_BG)
        self.create_widgets()
        self.load_config()

    def create_widgets(self):
        pad = {"padx": 10, "pady": 6}
        self.fields = {}
        labels = [
            ("Server URL", "server_url"),
            ("Device ID", "device_id"),
            ("OBS Host", "obs_host"),
            ("OBS Port", "obs_port"),
            ("OBS Password", "obs_password"),
        ]
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "TLabel", background=DARK_BG, foreground=TEXT_COLOR, font=("Segoe UI", 10)
        )
        style.configure(
            "TEntry", fieldbackground=ENTRY_BG, foreground=ENTRY_FG, background=ENTRY_BG
        )
        style.configure(
            "TButton",
            background=BUTTON_BG,
            foreground=BUTTON_FG,
            font=("Segoe UI", 10, "bold"),
        )
        style.map("TButton", background=[("active", ACCENT)])
        style.configure("TCheckbutton", background=DARK_BG, foreground=TEXT_COLOR)
        for i, (label, key) in enumerate(labels):
            ttk.Label(self, text=label + ":").grid(row=i, column=0, sticky="e", **pad)
            entry = ttk.Entry(self, width=32, show="*" if "password" in key else None)
            entry.grid(row=i, column=1, **pad)
            entry.configure(
                font=("Segoe UI", 10), background=ENTRY_BG, foreground=ENTRY_FG
            )
            self.fields[key] = entry
        self.show_pw_var = tk.BooleanVar()
        show_pw = ttk.Checkbutton(
            self,
            text="Show Password",
            variable=self.show_pw_var,
            command=self.toggle_password,
        )
        show_pw.grid(row=4, column=2, sticky="w")
        ttk.Button(self, text="Save Config", command=self.save_config).grid(
            row=6, column=0, **pad
        )
        ttk.Button(self, text="Run Client", command=self.run_client).grid(
            row=6, column=1, **pad
        )

    def toggle_password(self):
        show = "" if self.show_pw_var.get() else "*"
        self.fields["obs_password"].config(show=show)

    def load_config(self):
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        section = config["client"] if "client" in config else {}
        self.fields["server_url"].insert(
            0, section.get("server_url", "http://0.0.0.0:5500/api/status")
        )
        self.fields["device_id"].insert(0, section.get("device_id", "device_001"))
        self.fields["obs_host"].insert(0, section.get("obs_host", "localhost"))
        self.fields["obs_port"].insert(0, section.get("obs_port", "4455"))
        self.fields["obs_password"].insert(0, section.get("obs_password", ""))

    def save_config(self):
        config = configparser.ConfigParser()
        config["client"] = {
            "server_url": self.fields["server_url"].get(),
            "device_id": self.fields["device_id"].get(),
            "obs_host": self.fields["obs_host"].get(),
            "obs_port": self.fields["obs_port"].get(),
            "obs_password": self.fields["obs_password"].get(),
        }
        with open(CONFIG_FILE, "w") as f:
            config.write(f)
        messagebox.showinfo("Saved", "Configuration saved to config.ini")

    def run_client(self):
        self.save_config()
        # Run client.py in a new process
        python_exe = sys.executable
        try:
            subprocess.Popen(
                [python_exe, "client.py"],
                creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == "nt" else 0,
            )
            messagebox.showinfo(
                "Client Started", "OBS Monitor Client started in a new window."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Could not start client.py: {e}")


if __name__ == "__main__":
    app = ConfigApp()
    app.mainloop()
