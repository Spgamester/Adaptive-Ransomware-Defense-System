import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from src.core.detector import predict_file
from src.core.entropy import calculate_entropy
from src.utils.logger import alert
from src.utils.quarantine import quarantine_file  #  NEW

file_modifications = []
suspicious_files = []
monitor_events = []
monitor_events.append("Monitoring engine ready...")
detected = False


def log_suspicious(reason, file_path, observer):
    global detected

    if detected:
        return

    detected = True

    # 🔹 Alert
    alert(reason, file_path)

    # 🔹 Quarantine file
    quarantine_msg = quarantine_file(file_path)

    full_reason = f"{reason} | {quarantine_msg}"

    # 🔹 Store result
    suspicious_files.append((file_path, full_reason))

    monitor_events.append(
    f"THREAT DETECTED: {file_path}"
    )

    monitor_events.append(
    f"REASON: {full_reason}"
    )

    print("\n⚠ RANSOMWARE DETECTED")
    print("File:", file_path)
    print("Reason:", full_reason)

     #  Stop monitoring safely
    try:
        observer.stop()
    except:
        pass


class RansomwareMonitor(FileSystemEventHandler):

    def __init__(self, observer):
        self.observer = observer

    def on_modified(self, event):
        global detected

        if detected:
            return

        if not event.is_directory:

            try:
                file_path = event.src_path
                timestamp = time.strftime("%H:%M:%S")

                event_text = f"[{timestamp}] Modified: {file_path}"

                print(event_text)
                
                timestamp = time.strftime("%H:%M:%S")

                monitor_events.append(
                    f"[{timestamp}] THREAT DETECTED: {file_path}"
                    )
                
                monitor_events.append(
                    f"[{timestamp}] REASON: {full_reason}"
           )

                monitor_events.append(event_text)

                file_modifications.append(time.time())

                # -------- ENTROPY CHECK --------
                entropy = calculate_entropy(file_path)

                if entropy > 7.5:
                    ml_result = predict_file(file_path)

                    reason = f"High entropy (encryption) + {ml_result}"

                    log_suspicious(reason, file_path, self.observer)
                    return

                # -------- MASS MODIFICATION --------
                check_mass_modification(file_path, self.observer)

            except Exception as e:
                print("Error:", e)


def check_mass_modification(file_path, observer):
    global detected

    if detected:
        return

    current_time = time.time()

    recent = [t for t in file_modifications if current_time - t < 10]

    if len(recent) > 50:
        ml_result = predict_file(file_path)

        reason = f"Mass file modification + {ml_result}"

        log_suspicious(reason, file_path, observer)


def start_monitoring(path):
    global detected, file_modifications, suspicious_files

    # 🔹 Reset everything
    detected = False
    file_modifications.clear()
    suspicious_files.clear()
    monitor_events.clear()

    observer = Observer()

    event_handler = RansomwareMonitor(observer)
    observer.schedule(event_handler, path, recursive=True)

    observer.start()

    print(" Monitoring started on:", path)

    return observer
