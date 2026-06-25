import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from src.core.detector import predict_file
from src.core.entropy import calculate_entropy
from src.utils.logger import alert
from src.utils.quarantine import quarantine_file

# =========================

# GLOBAL DATA

# =========================

file_modifications = []
suspicious_files = []

live_events = []
threat_timeline = []

monitor_running = False
observer_instance = None

monitor_stats = {
    "files_monitored": 0,
    "processes_watching": 4328,
    "suspicious_events": 0,
    "active_threats": 0,
    "files_quarantined": 0,
}

# =========================

# THREAT LOGGING

# =========================

def log_suspicious(reason, file_path):

    alert(reason, file_path)

    quarantine_msg = quarantine_file(file_path)

    full_reason = f"{reason} | {quarantine_msg}"

    suspicious_files.append(
        (file_path, full_reason)
    )

    monitor_stats["suspicious_events"] += 1
    monitor_stats["active_threats"] += 1
    monitor_stats[
        "files_quarantined"
    ] += 1

    severity = "Medium"

    if "Entropy" in reason:
        severity = "High"

    if "Mass" in reason:
        severity = "Critical"

    live_events.insert(0, {
        "time": time.strftime("%H:%M:%S"),
        "source": "Detection Engine",
        "event": reason,
        "severity": severity
    })

    threat_timeline.insert(0, {
        "title": "Threat Quarantined",
        "time": time.strftime("%H:%M:%S"),
        "level": "critical"
    })

    print("\nTHREAT DETECTED")
    print("File:", file_path)
    print("Reason:", full_reason)


# =========================

# WATCHDOG HANDLER

# =========================

class RansomwareMonitor(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return

        try:
            file_path = event.src_path

            timestamp = time.strftime("%H:%M:%S")

            live_events.insert(0, {
                "time": timestamp,
                "source": "File Monitor",
                "event": f"Modified: {os.path.basename(file_path)}",
                "severity": "Medium"
            })

            file_modifications.append(
                time.time()
            )

            time.sleep(0.5)

            entropy = calculate_entropy(
                file_path
            )

            is_suspicious = (
                entropy > 7.0
                or file_path.lower().endswith(
                    (
                        ".bin",
                        ".enc",
                        ".locked"
                    )
                )
            )

            if is_suspicious:
                reason = ""

                if entropy > 7.5:
                    reason = "High Entropy Detected"

                elif file_path.lower().endswith(
                    (".enc", ".locked",".bin")
                ):
                    reason = "Suspicious Extension"

                if reason:
                    log_suspicious(
                        reason,
                        file_path
                    )

            check_mass_modification(
                file_path
            )

        except Exception as e:
            print(
                "Monitor Error:",
                e
            )
        


# =========================

# MASS MODIFICATION CHECK

# =========================

def check_mass_modification(file_path):

    current_time = time.time()

    recent = [
        t
        for t in file_modifications
        if current_time - t < 10
    ]

    if len(recent) > 50:

        ml_result = predict_file(
            file_path
        )

        reason = (
            f"Mass Modification | {ml_result}"
        )

        log_suspicious(
            reason,
            file_path
        )



# =========================

# INITIAL THREAT SCAN

# =========================

def initial_scan(path):

    for root, dirs, files in os.walk(path):

        for file in files:

            full_path = os.path.join(
                root,
                file
            )

            try:

                if full_path.lower().endswith(
                    (
                        ".bin",
                        ".enc",
                        ".locked"
                    )
                ):

                    log_suspicious(
                        "Initial Scan Detection",
                        full_path
                    )

                    live_events.insert(0, {
                        "time": time.strftime("%H:%M:%S"),
                        "source": "Initial Scan",
                        "event": f"Threat Found: {file}",
                        "severity": "High"
                    })

            except Exception as e:

                print(
                    "Initial Scan Error:",
                    e
                )


# =========================

# START MONITORING

# =========================

def start_monitoring(path):

    global monitor_running
    global observer_instance

    if monitor_running:
        return observer_instance

    monitor_running = True

    file_modifications.clear()
    suspicious_files.clear()

    live_events.clear()
    threat_timeline.clear()

    monitor_stats["suspicious_events"] = 0
    monitor_stats["active_threats"] = 0
    monitor_stats["files_quarantined"] = 0

    file_count = 0

    for root, dirs, files in os.walk(path):
        file_count += len(files)

    monitor_stats["files_monitored"] = file_count

    initial_scan(path)

    observer = Observer()

    event_handler = RansomwareMonitor()

    observer.schedule(
        event_handler,
        path,
        recursive=True
    )

    observer.start()

    observer_instance = observer

    live_events.insert(0, {
        "time": time.strftime("%H:%M:%S"),
        "source": "System",
        "event": "Monitoring Started",
        "severity": "Low"
    })

    print(
        f"Monitoring Started: {path}"
    )

    return observer


# =========================

# STOP MONITORING

# =========================

def stop_monitoring():

    global monitor_running
    global observer_instance

    if observer_instance:

        observer_instance.stop()
        observer_instance.join()

        observer_instance = None

    monitor_running = False

    live_events.insert(0, {
        "time": time.strftime("%H:%M:%S"),
        "source": "System",
        "event": "Monitoring Stopped",
        "severity": "Low"
    })

    return True
