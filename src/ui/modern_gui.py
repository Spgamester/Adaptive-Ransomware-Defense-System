from importlib.resources import files

import psutil
import customtkinter as ctk
from tkinter import filedialog
import os
import threading

from src.core.scanner import run_scan
from src.core.monitoring import monitor_events
from src.utils.logger import detected_threats
from src.utils.restore import restore_file
from src.utils.delete_file import delete_quarantined_file
from src.utils.settings_manager import (
    load_settings,
    save_settings
)


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ARDSApp(ctk.CTk):
       



    def __init__(self):
        super().__init__()

        

        self.title("ARDS - AI Ransomware Detection System")
        self.geometry("1200x700")

        self.selected_path = ""

        # =========================
        # SIDEBAR
        # =========================

        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(
            self.sidebar,
            text="ARDS",
            font=("Arial", 26, "bold")
        ).pack(pady=25)

        self.dashboard_btn = ctk.CTkButton(
        self.sidebar,
        text="Dashboard",
        command=lambda: self.show_frame(self.dashboard_frame)
        )
        self.dashboard_btn.pack(pady=8)

        self.scan_nav_btn = ctk.CTkButton(
        self.sidebar,
        text="Scan",
        command=lambda: self.show_frame(self.scan_frame)
        )
        self.scan_nav_btn.pack(pady=8)

        self.monitor_btn = ctk.CTkButton(
        self.sidebar,
        text="Monitor",
        command=lambda: self.show_frame(self.monitor_frame)
         )
        self.monitor_btn.pack(pady=8)

        self.quarantine_btn = ctk.CTkButton(
        self.sidebar,
        text="Quarantine",
        command=lambda: self.show_frame(self.quarantine_frame)
        )
        self.quarantine_btn.pack(pady=8)

        self.logs_btn = ctk.CTkButton( 
        self.sidebar,
        text="Logs",
        command=lambda: self.show_frame(self.logs_frame)
        )
        self.logs_btn.pack(pady=8)

        self.settings_btn = ctk.CTkButton(
        self.sidebar,
        text="Settings",
        command=lambda: self.show_frame(self.settings_frame)
        )
        self.settings_btn.pack(pady=8)
        

        # =========================
        # MAIN CONTAINER
        # =========================

        self.main = ctk.CTkFrame(self)
        self.main.pack(fill="both", expand=True, padx=10, pady=10)

        # Pages

        self.dashboard_frame = ctk.CTkFrame(self.main)
        self.scan_frame = ctk.CTkFrame(self.main)
        self.monitor_frame = ctk.CTkFrame(self.main)
        self.quarantine_frame = ctk.CTkFrame(self.main)
        self.logs_frame = ctk.CTkFrame(self.main)
        self.settings_frame = ctk.CTkFrame(self.main)
        

        # Show Dashboard by default
        self.show_frame(self.dashboard_frame)
        ctk.CTkLabel(
            self.scan_frame,
            text="Scan",
            font=("Arial", 28, "bold")
            ).pack(pady=40)

        # =========================
        # MONITOR PAGE
        # =========================

        monitor_title = ctk.CTkLabel(
        self.monitor_frame,
            text="Real-Time Behavioral Monitor",
            font=("Arial", 28, "bold")
            )
        monitor_title.pack(pady=(30, 20))

        self.monitor_status = ctk.CTkLabel(
        self.monitor_frame,
            text="Status: ACTIVE",
            font=("Arial", 18)
            )
        self.monitor_status.pack(pady=10)

        self.monitor_box = ctk.CTkTextbox(
            self.monitor_frame,
            width=900,
            height=400
            )
        self.monitor_box.pack(pady=20)
        self.monitor_start_btn = ctk.CTkButton(
            self.monitor_frame,
            text="Start Monitoring",
            command=self.start_monitoring_gui
           )
        self.monitor_start_btn.pack(pady=10)

        self.monitor_box.insert(
            "end",
            "Monitoring engine ready...\n"
            )

        # =========================
        # QUARANTINE PAGE
        # =========================

        quarantine_title = ctk.CTkLabel(
            self.quarantine_frame,
            text="Quarantine Vault",
            font=("Arial", 28, "bold")
        )
        quarantine_title.pack(pady=(30, 20))
        
        ctk.CTkButton(
            self.quarantine_frame,
            text="Refresh Quarantine",
            command=self.load_quarantine_files
        ).pack(pady=10)


        self.quarantine_box = ctk.CTkTextbox(
            self.quarantine_frame,
            width=900,
            height=350
            )
        self.quarantine_box.pack(pady=20)

        self.restore_btn = ctk.CTkButton(
            self.quarantine_frame,
            text="Restore First File",
            command=self.restore_first_file
        )

        self.restore_btn.pack(
            pady=10
        )

        self.delete_btn = ctk.CTkButton(
            self.quarantine_frame,
            text="Delete First File",
            command=self.delete_first_file,
            fg_color="darkred"
        )

        self.delete_btn.pack(
            pady=5
        )

        # =========================
        # LOGS & SETTINGS
        # =========================
        logs_title = ctk.CTkLabel(
            self.logs_frame,
            text="Detection Logs",
            font=("Arial", 28, "bold")
            )
        logs_title.pack(pady=(30, 20))

        self.refresh_logs_btn = ctk.CTkButton(
            self.logs_frame,
            text="Refresh Logs",
            command=self.load_logs
            )
        self.refresh_logs_btn.pack(pady=10)

        self.logs_box = ctk.CTkTextbox(
            self.logs_frame,
            width=900,
            height=450
            )
        self.logs_box.pack(pady=20)

        
        # =========================
        # SETTINGS PAGE
        # =========================

        settings_title = ctk.CTkLabel(
            self.settings_frame,
            text="System Settings",
            font=("Arial", 28, "bold")
            )
        settings_title.pack(pady=(30, 20))

        # -------------------------
        # Detection Settings
        # -------------------------

        detection_frame = ctk.CTkFrame(self.settings_frame)
        detection_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(
            detection_frame,
            text="Detection Settings",
            font=("Arial", 18, "bold")
            ).pack(pady=10)

        ctk.CTkLabel(
            detection_frame,
            text="Entropy Threshold"
            ).pack()

        self.entropy_entry = ctk.CTkEntry(
            detection_frame
            )
        self.entropy_entry.pack(pady=5)
        self.entropy_entry.insert(0, "7.5")

        ctk.CTkLabel(
            detection_frame,
            text="Mass Modification Limit"
            ).pack()

        self.mass_mod_entry = ctk.CTkEntry(
            detection_frame
           )
        self.mass_mod_entry.pack(pady=5)
        self.mass_mod_entry.insert(0, "50")

        # -------------------------
        # Behavior Settings
        # -------------------------

        behavior_frame = ctk.CTkFrame(self.settings_frame)
        behavior_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(
            behavior_frame,
            text="Behavior",
            font=("Arial", 18, "bold")
            ).pack(pady=10)

        self.auto_quarantine = ctk.CTkSwitch(
            behavior_frame,
            text="Enable Auto Quarantine"
            )
        self.auto_quarantine.pack(pady=5)

        self.enable_monitoring = ctk.CTkSwitch(
            behavior_frame,
            text="Enable Monitoring"
            )
        self.enable_monitoring.pack(pady=5)

        # -------------------------
        # Notifications
        # -------------------------

        notification_frame = ctk.CTkFrame(self.settings_frame)
        notification_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(
            notification_frame,
            text="Notifications",
            font=("Arial", 18, "bold")
            ).pack(pady=10)

        self.enable_alerts = ctk.CTkSwitch(
            notification_frame,
            text="Enable Threat Alerts"
          )
        self.enable_alerts.pack(pady=5)

        # -------------------------
        # Save Button
        # -------------------------

        self.save_settings_btn = ctk.CTkButton(
            self.settings_frame,
            text="Save Settings",
            command=lambda: print("Settings module coming soon")
        )

        self.save_settings_btn.pack(
            pady=20
        )

        
           # =========================
           # DASHBOARD TITLE
           # =========================

        dashboard_title = ctk.CTkLabel(
            self.dashboard_frame,
            text="ARDS Security Operations Center",
            font=("Arial", 32, "bold")
        )
        dashboard_title.pack(pady=(30, 20))

            # =========================
            # DASHBOARD CARDS
            # =========================

        cards_frame = ctk.CTkFrame(
            self.dashboard_frame,
            fg_color="transparent"
            )
        cards_frame.pack(pady=20)

        self.monitor_card = self.create_card(
             cards_frame,
            "Monitoring Status",
            "ACTIVE"
        )  

        self.threat_card = self.create_card(
            cards_frame,
            "Threat Detections",
            "0"
            )

        self.quarantine_card = self.create_card(
            cards_frame,
            "Quarantined Files",
            "0"
        )

        self.fp_card = self.create_card(
            cards_frame,
            "False Positive Rate",
            "0.0%"
        )

        self.cpu_card = self.create_card(
            cards_frame,
            "CPU Usage",
            "0%"
        )

        self.ram_card = self.create_card(
            cards_frame,
            "RAM Usage",
            "0%"
        )


        # =========================
        # ALERT FEED
        # =========================

        alert_title = ctk.CTkLabel(
            self.dashboard_frame,
            text="Alert Feed",
            font=("Arial", 24, "bold")
            )
        alert_title.pack(pady=(40, 15))

        alert_frame =ctk.CTkFrame(
            self.dashboard_frame,
            width = 1000,
            height = 250,
            corner_radius = 15,
            fg_color = "#1F2430"
            )
        alert_frame.pack(pady=10)
        alert_frame.pack_propagate(False)


        

        self.alert_box = ctk.CTkTextbox(
            alert_frame,
            width=950,
            height=200
        )

        self.alert_box.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )


        # =========================
        # SCAN SECTION
        # =========================

        ctk.CTkLabel(
            self.scan_frame,
            text="Scan Files and Folders",
            font=("Arial", 20)
        ).pack(pady=15)

        self.path_label = ctk.CTkLabel(
            self.scan_frame,
            text="No file/folder selected"
        )
        self.path_label.pack(pady=5)

        btn_frame = ctk.CTkFrame(self.scan_frame)
        btn_frame.pack(pady=10)

        ctk.CTkButton(
            btn_frame,
            text="Select Folder",
            command=self.select_folder
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_frame,
            text="Select File",
            command=self.select_file
        ).pack(side="left", padx=10)

        self.scan_btn = ctk.CTkButton(
            self.scan_frame,
            text="Start Scan",
            command=self.start_scan
        )
        self.scan_btn.pack(pady=15)

        self.status_label = ctk.CTkLabel(
            self.scan_frame,
            text="Status: Idle",
            font=("Arial", 18)
        )
        self.status_label.pack(pady=10)

        # =========================
        # LOG BOX
        # =========================

        self.log_box = ctk.CTkTextbox(
            self.scan_frame,
            width=800,
            height=200
        )
        self.log_box.pack(pady=15)

        self.log_box.insert("end", "ARDS Ready...\n")
        self.update_monitor_feed()
        self.load_quarantine_files()
        self.load_logs()
        self.update_dashboard_metrics()
        self.update_alert_feed()

    # =========================
    # CARD FUNCTION
    # =========================

    def create_card(self, parent, title, value):

      card = ctk.CTkFrame(
        parent,
        width=150,
        height=120,
        corner_radius=15,
        fg_color="#1F2430"
        )

      card.pack(side="left", padx=8)
      card.pack_propagate(False)

      title_label = ctk.CTkLabel(
        card,
        text=title,
        font=("Arial", 14)
        )
      title_label.pack(pady=(20, 5))

      value_label = ctk.CTkLabel(
        card,
        text=value,
        font=("Arial", 24, "bold")
        )
      value_label.pack()

      return value_label

    # =========================
    # FILE/FOLDER
    # =========================
      # =========================
     # PAGE SWITCHING
    # =========================

    def show_frame(self, frame):

     for f in (
        self.dashboard_frame,
        self.scan_frame,
        self.monitor_frame,
        self.quarantine_frame,
        self.logs_frame,
        self.settings_frame
    ):
        f.pack_forget()

     frame.pack(fill="both", expand=True)


    # =========================
    # MONITOR FEED
    # =========================

    def update_monitor_feed(self):

            try:

                self.monitor_box.delete("1.0", "end")

                from src.core.monitoring import monitor_events

                for event in monitor_events[-50:]:
                    self.monitor_box.insert(
                    "end",
                    event + "\n"
                    )
 
            except Exception:
                pass

            self.after(1000, self.update_monitor_feed)


        # =========================
        # ALERT FEED
        # =========================

    def update_alert_feed(self):

            try:

                self.alert_box.delete(
                   "1.0",
                   "end"
                )

                from src.utils.logger import alert_feed

                for alert in alert_feed[-20:]:

                    if "CRITICAL" in alert or "🔴" in alert:
                        line = f"🔴 {alert}\n"

                    elif "WARNING" in alert or "🟠" in alert:
                        line = f"🟠 {alert}\n"

                    else:
                        line = f"🟢 {alert}\n"

                    self.alert_box.insert(
                        "end",
                        line
                    )

            except Exception:
               pass

            self.after(
                1000,
                self.update_alert_feed
            )

    from src.utils.logger import alert_feed

    alert_feed.append(
        "INFO: Monitoring Service Started"
    )

    alert_feed.append(
        "INFO: AI Detection Model Loaded"
    )



    # =========================
    # DASHBOARD METRICS
    # =========================

    def update_dashboard_metrics(self):

        try:

            cpu = psutil.cpu_percent()

            ram = psutil.virtual_memory().percent

            quarantine_count = len(
                os.listdir("quarantine")
            )          

            threat_count = len(
                detected_threats
            )

            self.cpu_card.configure(
                text=f"{cpu}%"
            )

            self.ram_card.configure(
                text=f"{ram}%"
            )

            self.quarantine_card.configure(
                text=str(quarantine_count)
            )

            self.threat_card.configure(
                text=str(threat_count)
            )

        except Exception as e:

            print("Dashboard Error:", e)

        self.after(
            2000,
            self.update_dashboard_metrics
        )

        # =========================
        # FILE / FOLDER
        # =========================

    def select_folder(self):

        self.selected_path = filedialog.askdirectory()

        if self.selected_path:
         self.path_label.configure(
            text=self.selected_path
           )


    def select_file(self):

        self.selected_path = filedialog.askopenfilename()
 
        if self.selected_path:
            self.path_label.configure(
            text=self.selected_path
            )             
    # =========================
    # # QUARANTINE
    # =========================

    def load_quarantine_files(self):

        self.quarantine_box.delete("1.0", "end")

        quarantine_folder = os.path.join(
            os.getcwd(),
            "quarantine"
            )

        print("Quarantine Folder:", quarantine_folder)

        if not os.path.exists(quarantine_folder):

            self.quarantine_box.insert(
                "end",
                "No quarantine folder found."
            )
            return

        files = os.listdir(quarantine_folder)

        print("Files Found:", files)

        if not files:

            self.quarantine_box.insert(
                "end",
                "No quarantined files."
            )
            return

        self.quarantine_box.insert(
            "end",
            "QUARANTINED FILES\n"
            )

        self.quarantine_box.insert(
            "end",
            "=====================\n\n"
            )

        self.quarantine_box.insert(
            "end",
            f"TOTAL FILES: {len(files)}\n"
        )

        self.quarantine_box.insert(
            "end",
            "============================\n\n"
        )

        for index, file in enumerate(files, start=1):

            self.quarantine_box.insert(
                "end",
                f"{index}. {file}\n"
            )

    # =========================
    # RESTORE
    # =========================

    def restore_first_file(self):

        quarantine_folder = os.path.join(
            os.getcwd(),
            "quarantine"
        )

        if not os.path.exists(
            quarantine_folder
        ):
            return

        files = os.listdir(
            quarantine_folder
        )

        if not files:
            return

        success, message = restore_file(
            files[0]
        )

        self.load_quarantine_files()

        self.log_box.insert(
            "end",
            f"\n{message}\n"
        )
    

    # =========================
    # DELETE
    # =========================

    def delete_first_file(self):

        quarantine_folder = os.path.join(
            os.getcwd(),
            "quarantine"
        )

        if not os.path.exists(
            quarantine_folder
        ):
            return

        files = os.listdir(
            quarantine_folder
        )

        if not files:
            return

        success, message = delete_quarantined_file(
            files[0]
        )

        self.load_quarantine_files()

        self.log_box.insert(
            "end",
            f"\n{message}\n"
        )

    # =========================
    # LOGS
    # =========================

    def load_logs(self):

        self.logs_box.delete("1.0", "end")

        log_file = os.path.join(
            os.getcwd(),
            "logs",
            "detection_log.txt"
            )

        if not os.path.exists(log_file):

            self.logs_box.insert(
                "end",
                "No log file found."
            )
            return

        with open(log_file, "r") as f:

            content = f.read()

        if not content:

            self.logs_box.insert(
                "end",
                "No logs available."
            )
            return

        self.logs_box.insert(
            "end",
            content
            )




    # =========================
    # SCAN
    # =========================
    def start_monitoring_gui(self):

        folder = filedialog.askdirectory()

        if not folder:
         return

        from src.core.monitoring import start_monitoring

        start_monitoring(folder)

        self.monitor_status.configure(
        text=f"Monitoring: {folder}"
       )

    def start_scan(self):

        if not self.selected_path:

            self.status_label.configure(
                text="⚠ Select file/folder first",
                text_color="red"
            )
            return

        self.status_label.configure(
            text="Scanning...",
            text_color="blue"
        )

        def scan():

            result = run_scan(self.selected_path)

            if result["status"] == "SAFE":

                self.status_label.configure(
                    text="✔ SAFE",
                    text_color="green"
                )

                self.log_box.insert(
                    "end",
                    "\n✔ No threats detected\n"
                )

            else:

                self.status_label.configure(
                    text="⚠ THREAT DETECTED",
                    text_color="red"
                )

                self.log_box.insert(
                    "end",
                    "\n⚠ Threat Detected\n"
                )

                for file, reason in result["details"]:
                    self.log_box.insert(
                        "end",
                        f"\nFile: {file}\nReason: {reason}\n"
                    )

        threading.Thread(
            target=scan,
            daemon=True
        ).start()


if __name__ == "__main__":
    app = ARDSApp()
    app.mainloop()