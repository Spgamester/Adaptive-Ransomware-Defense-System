import os
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from src.core.detector import predict_file
from src.core.entropy import calculate_entropy

from src.utils.logger import alert
from src.utils.quarantine import quarantine_file


# ==========================================================
# GLOBAL RUNTIME DATA
# ==========================================================

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


# ==========================================================
# EVENT ID GENERATOR
# ==========================================================

_event_counter = 0


def next_event_id():

    global _event_counter

    _event_counter += 1

    return _event_counter


# ==========================================================
# TELEMETRY EVENT FACTORY
# ==========================================================

def create_event(

    source,

    event,

    severity="Low",

    status="Monitoring",

    category="General",

    file_name=None,

    file_path=None,

    attack_id=None

):

    return {

        "id": next_event_id(),

        "time": time.strftime("%H:%M:%S"),

        "source": source,

        "event": event,

        "severity": severity,

        "status": status,

        "category": category,

        "file_name": file_name,

        "file_path": file_path,

        "attack_id": attack_id

    }


# ==========================================================
# INITIAL SYSTEM EVENTS
# ==========================================================

def initialize_live_events():

    live_events.clear()

    threat_timeline.clear()

    live_events.append(

        create_event(

            source="System",

            event="Monitoring Started",

            severity="Low",

            status="Running",

            category="System"

        )

    )

    threat_timeline.append({

        "title": "Monitoring Started",

        "time": time.strftime("%H:%M:%S"),

        "level": "info"

    })
# ==========================================================
# THREAT LOGGING
# ==========================================================

def log_suspicious(reason, file_path):

    alert(reason, file_path)

    quarantine_result = quarantine_file(file_path)

    suspicious_files.append(

        (file_path, f"{reason} | {quarantine_result}")

    )

    monitor_stats["suspicious_events"] += 1
    monitor_stats["active_threats"] += 1
    monitor_stats["files_quarantined"] += 1

    severity = "Medium"

    if "Entropy" in reason:
        severity = "High"

    if "Mass" in reason:
        severity = "Critical"

    event = create_event(

        source="Detection Engine",

        event=reason,

        severity=severity,

        status="Blocked",

        category="Behavior",

        file_name=os.path.basename(file_path),

        file_path=file_path,

        attack_id="T1486"

    )

    live_events.insert(0, event)

    threat_timeline.insert(0, {

        "title": "Threat Quarantined",

        "time": time.strftime("%H:%M:%S"),

        "level": severity.lower()

    })

    print("\n========== THREAT DETECTED ==========")
    print("Reason :", reason)
    print("File   :", file_path)
    print("=====================================\n")


# ==========================================================
# FILE MONITOR
# ==========================================================

class RansomwareMonitor(FileSystemEventHandler):

    def on_modified(self, event):

        if event.is_directory:
            return

        file_path = event.src_path

        try:

            monitor_stats["files_monitored"] += 1

            file_modifications.append(time.time())

            live_events.insert(

                0,

                create_event(

                    source="File Monitor",

                    event="File Modified",

                    severity="Low",

                    status="Monitoring",

                    category="Filesystem",

                    file_name=os.path.basename(file_path),

                    file_path=file_path

                )

            )

            time.sleep(0.5)

            entropy = calculate_entropy(file_path)

            suspicious = (

                entropy > 7.0

                or file_path.lower().endswith(

                    (

                        ".enc",

                        ".locked",

                        ".bin"

                    )

                )

            )

            if suspicious:

                if entropy > 7.5:

                    log_suspicious(

                        "High Entropy Detected",

                        file_path

                    )

                elif file_path.lower().endswith(

                    (

                        ".enc",

                        ".locked",

                        ".bin"

                    )

                ):

                    log_suspicious(

                        "Suspicious Extension",

                        file_path

                    )

            check_mass_modification(file_path)

        except Exception as e:

            print("Monitor Error :", e)


# ==========================================================
# MASS MODIFICATION DETECTION
# ==========================================================

def check_mass_modification(file_path):

    now = time.time()

    recent = [

        t

        for t in file_modifications

        if now - t < 10

    ]

    if len(recent) > 50:

        prediction = predict_file(file_path)

        reason = f"Mass Modification | {prediction}"

        log_suspicious(

            reason,

            file_path

        )
# ==========================================================
# INITIAL THREAT SCAN
# ==========================================================

def initial_scan(path):

    for root, dirs, files in os.walk(path):

        for file in files:

            full_path = os.path.join(root, file)

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

            except Exception as e:

                print(

                    "Initial Scan Error:",

                    e

                )


# ==========================================================
# START MONITORING
# ==========================================================

def start_monitoring(path):

    global monitor_running

    global observer_instance

    if monitor_running:

        return observer_instance

    monitor_running = True

    file_modifications.clear()

    suspicious_files.clear()

    initialize_live_events()

    monitor_stats["suspicious_events"] = 0

    monitor_stats["active_threats"] = 0

    monitor_stats["files_quarantined"] = 0

    file_count = 0

    for root, dirs, files in os.walk(path):

        file_count += len(files)

    monitor_stats["files_monitored"] = file_count

    initial_scan(path)

    observer = Observer()

    observer.schedule(

        RansomwareMonitor(),

        path,

        recursive=True

    )

    observer.start()

    observer_instance = observer

    print(f"Monitoring Started : {path}")

    return observer


# ==========================================================
# STOP MONITORING
# ==========================================================

def stop_monitoring():

    global monitor_running

    global observer_instance

    if observer_instance:

        observer_instance.stop()

        observer_instance.join()

        observer_instance = None

    monitor_running = False

    live_events.insert(

        0,

        create_event(

            source="System",

            event="Monitoring Stopped",

            severity="Low",

            status="Stopped",

            category="System"

        )

    )

    threat_timeline.insert(

        0,

        {

            "title": "Monitoring Stopped",

            "time": time.strftime("%H:%M:%S"),

            "level": "info"

        }

    )

    return True