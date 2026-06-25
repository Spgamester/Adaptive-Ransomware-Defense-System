import customtkinter as ctk
from tkinter import filedialog
import threading

from src.core.scanner import run_scan
from src.core.monitoring import monitor_events

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

        ctk.CTkLabel(
            self.quarantine_frame,
            text="Quarantine",
            font=("Arial", 28, "bold")
            ).pack(pady=40)

        ctk.CTkLabel(
            self.logs_frame,
            text="Logs",
            font=("Arial", 28, "bold")
            ).pack(pady=40)

        ctk.CTkLabel(
            self.settings_frame,
            text="Settings",
            font=("Arial", 28, "bold")
            ).pack(pady=40)

           # =========================
           # DASHBOARD TITLE
           # =========================

        dashboard_title = ctk.CTkLabel(
                self.dashboard_frame,
                text="Dashboard",
                font=("Arial", 36, "bold")
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

        self.create_card(cards_frame, "Monitoring Status", "ACTIVE")
        self.create_card(cards_frame, "Threat Detections", "0")
        self.create_card(cards_frame, "Quarantined Files", "0")
        self.create_card(cards_frame, "False Positive Rate", "0.0%")
        self.create_card(cards_frame, "CPU Usage", "34%")
        self.create_card(cards_frame, "RAM Usage", "56%")


        # =========================
        # ALERT FEED
        # =========================

        alert_title = ctk.CTkLabel(
            self.dashboard_frame,
            text="Alert Feed",
            font=("Arial", 24, "bold")
            )
        alert_title.pack(pady=(40, 15))

        alert_frame = ctk.CTkFrame(
            self.dashboard_frame,
            width=1000,
            height=250,
            corner_radius=15,
            fg_color="#1F2430"
            )
        alert_frame.pack(pady=10)
        alert_frame.pack_propagate(False)

        ctk.CTkLabel(
            alert_frame,
            text="🔴 CRITICAL    Malware Payload Detected",
            anchor="w",
            font=("Arial", 16)
            ).pack(fill="x", padx=20, pady=(20,10))

        ctk.CTkLabel(
            alert_frame,
            text="🟠 WARNING    Suspicious Network Activity",
            anchor="w",
            font=("Arial", 16)
            ).pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            alert_frame,
            text="🟢 INFO       Monitoring Service Started",
            anchor="w",
            font=("Arial", 16)
            ).pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            alert_frame,
            text="🟢 INFO       AI Detection Model Loaded",
            anchor="w",
            font=("Arial", 16)
            ).pack(fill="x", padx=20, pady=10)
    

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