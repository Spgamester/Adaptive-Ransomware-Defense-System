import sys
import os

#  Fix for PyInstaller
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
import threading

from src.core.scanner import run_scan

selected_path = ""

def browse_folder():
    global selected_path
    selected_path = filedialog.askdirectory()
    path_label.config(text=f"Selected Folder: {selected_path}")

def browse_file():
    global selected_path
    selected_path = filedialog.askopenfilename()
    path_label.config(text=f"Selected File: {selected_path}")

def start_scan():
    if not selected_path:
        messagebox.showwarning("Warning", "Please select a file or folder first!")
        return

    progress.start()
    status_label.config(text="Scanning...", fg="blue")

    def scan():
        result = run_scan(selected_path)

        progress.stop()

        # 🔹 Update status
        if result["status"] == "SAFE":
            status_label.config(text="✔ SAFE", fg="green")
        else:
            status_label.config(text="⚠ THREAT DETECTED", fg="red")

        # 🔹 Clear old logs
        log_box.delete(1.0, tk.END)

        # 🔹 Display results
        log_box.insert(tk.END, "\n--- SCAN RESULT ---\n")

        if result["status"] == "SAFE":
            log_box.insert(tk.END, "✔ No threats detected\n")
        else:
            log_box.insert(tk.END, "⚠ RANSOMWARE DETECTED\n\n")

            for file, reason in result["details"]:
                log_box.insert(tk.END, f"File: {file}\n")
                log_box.insert(tk.END, f"Reason: {reason}\n\n")

    threading.Thread(target=scan).start()

def clear_logs():
    log_box.delete(1.0, tk.END)


# ---------------- UI ----------------

root = tk.Tk()
root.title("AI Ransomware Detection System")
root.geometry("650x420")

title = tk.Label(root, text="AI Ransomware Detection System", font=("Arial", 16, "bold"))
title.pack(pady=10)

# 🔹 Selection buttons
btn_frame = tk.Frame(root)
btn_frame.pack()

folder_btn = tk.Button(btn_frame, text="Select Folder", command=browse_folder, width=20)
folder_btn.grid(row=0, column=0, padx=5)

file_btn = tk.Button(btn_frame, text="Select File", command=browse_file, width=20)
file_btn.grid(row=0, column=1, padx=5)

# 🔹 Path label
path_label = tk.Label(root, text="No file/folder selected", fg="gray")
path_label.pack(pady=5)

# 🔹 Scan button
scan_btn = tk.Button(root, text="Start Scan", command=start_scan, width=25, bg="black", fg="white")
scan_btn.pack(pady=10)

# 🔹 Progress bar
progress = Progressbar(root, mode="indeterminate", length=350)
progress.pack(pady=5)

# 🔹 Status
status_label = tk.Label(root, text="Status: Idle", font=("Arial", 12))
status_label.pack(pady=5)

# 🔹 Logs
clear_btn = tk.Button(root, text="Clear Logs", command=clear_logs)
clear_btn.pack()

log_box = tk.Text(root, height=10, width=75)
log_box.pack(pady=10)

root.mainloop()