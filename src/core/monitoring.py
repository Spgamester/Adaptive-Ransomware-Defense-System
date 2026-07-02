"""
ARDS Monitoring Engine
======================

Central monitoring engine for ARDS.

Pipeline

Filesystem
    ↓
Detection Manager
    ↓
Incident Manager
    ↓
Behavior Engine
    ↓
Risk Engine
    ↓
Decision Engine
    ↓
Response Engine
    ↓
Dashboard + Analytics + Telemetry
"""

import os
import time
import psutil

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from src.utils.honeypot_manager import create_honeypot
from src.utils.logger import alert
from src.utils.quarantine import quarantine_file

from src.core.telemetry import TelemetryEvent

from src.core.correlation import CorrelationEngine
from src.core.behavior_engine import BehaviorEngine
from src.core.risk_engine_v2 import AdaptiveRiskEngine
from src.core.decision_engine import DecisionEngine
from src.core.response_engine import ResponseEngine

from src.detection.detection_manager import DetectionManager

from src.incident.incident_manager import IncidentManager

from src.shared.runtime import (
    live_events,
    threat_timeline,
    monitor_stats,
    suspicious_files,
)


import src.services.analytics_service as analytics_service
# ==========================================================
# Runtime Objects
# ==========================================================

observer = None

correlation_engine = CorrelationEngine()

behavior_engine = BehaviorEngine()

risk_engine = AdaptiveRiskEngine()

decision_engine = DecisionEngine()

response_engine = ResponseEngine()

detection_manager = DetectionManager()

incident_manager = IncidentManager()

monitor_running = False

_event_counter = 0


# ==========================================================
# Event Helpers
# ==========================================================

def next_event_id():

    global _event_counter

    _event_counter += 1

    return _event_counter
def create_event(

    source,

    event,

    severity,

    status,

    category,

    file_name,

    file_path,

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

        "attack_id": attack_id,

        "behavior_name": None,

        "confidence": 0,

        "stage": None,

        "risk_score": 0,

        "risk_level": None,

        "decision": None,

        "priority": 0,

        "actions": [],

        "evidence": []

    }
# ==========================================================
# Dashboard Initialization
# ==========================================================

def initialize_dashboard():

    live_events.clear()

    threat_timeline.clear()

    live_events.append(

        create_event(

            source="System",

            event="Monitoring Started",

            severity="Low",

            status="Running",

            category="System",

            file_name=None,

            file_path=None

        )

    )

# ==========================================================
# Detection Pipeline
# ==========================================================

def process_detection(
    result,
    file_path
):
    
    
    
    if result is None:
         return

    # ------------------------------------------
    # Incident
    # ------------------------------------------

    incident = incident_manager.add_detection(
        file_path,
        result
    )

    # ------------------------------------------
    # Alert
    # ------------------------------------------

    alert(
        result.signal,
        file_path
    )

    # ------------------------------------------
    # Telemetry
    # ------------------------------------------

    TelemetryEvent(

        source=result.detector,

        signal=result.signal,

        severity=result.severity,

        category="Behavior",

        file_name=os.path.basename(file_path),

        file_path=file_path

    ).emit()

    # ------------------------------------------
    # Correlation
    # ------------------------------------------

    groups = correlation_engine.correlate()

    latest_group = groups[-1] if groups else []

    # ------------------------------------------
    # Behavior
    # ------------------------------------------

    behavior = behavior_engine.analyze(
        latest_group
    )

    # ------------------------------------------
    # Risk
    # ------------------------------------------

    risk = risk_engine.evaluate(
        behavior
    )

    # ------------------------------------------
    # Decision
    # ------------------------------------------

    decision = decision_engine.decide(
        risk
    )

    # ------------------------------------------
    # Response
    # ------------------------------------------

    response = response_engine.execute(
        decision
    )

    # ------------------------------------------
    # Incident Update
    # ------------------------------------------

    incident_manager.update_incident(

        file_path,

        behavior,

        risk,

        decision,

        response

    )

    # ------------------------------------------
    # Quarantine
    # ------------------------------------------


    print("=" * 50)
    print("Risk Level :", risk["risk_level"])
    print("Decision   :", decision["decision"])
    print("Quarantine :", decision["quarantine"])
    print("File Exists Before:", os.path.exists(file_path))
    print("=" * 50)

    quarantine_status = "Not Quarantined"

    if decision["quarantine"] or risk["risk_level"] in ["High", "Critical"]:
        if os.path.exists(file_path):
            quarantine_status = quarantine_file(file_path)

            if "Moved" in quarantine_status:
                monitor_stats["files_quarantined"] += 1

                suspicious_files.append(
                    (
                        file_path,
                        quarantine_status
                    )
                )
        else:
            quarantine_status = "Already Quarantined"

    # ------------------------------------------
    # Statistics
    # ------------------------------------------

    monitor_stats["suspicious_events"] += 1
    monitor_stats["processes_watching"] = len(psutil.pids())

    monitor_stats["active_threats"] += 1

    # ------------------------------------------
    # Dashboard Event
    # ------------------------------------------

    event = create_event(

        source=result.detector,

        event=result.signal,

        severity=risk["risk_level"],

        status=response["status"],

        category="Behavior",

        file_name=os.path.basename(file_path),

        file_path=file_path,

        attack_id="T1486"

    )

    event["behavior_name"] = behavior["behavior_name"]

    event["confidence"] = behavior["confidence"]

    event["stage"] = behavior["stage"]

    event["risk_score"] = risk["risk_score"]

    event["risk_level"] = risk["risk_level"]

    event["decision"] = decision["decision"]

    event["priority"] = decision["priority"]

    event["actions"] = response["actions"]

    event["evidence"] = risk["evidence"]

    live_events.insert(0, event)

    threat_timeline.insert(

        0,

        {

            "title": result.signal,

            "time": time.strftime("%H:%M:%S"),

            "level": risk["risk_level"].lower()

        }

    )

    # ------------------------------------------
    # Analytics
    # ------------------------------------------

    analytics_service.update(event)

    # ------------------------------------------
    # Console
    # ------------------------------------------

    print()

    print("=" * 65)

    print("ARDS INTELLIGENCE PIPELINE")

    print("=" * 65)

    print(f"Detector      : {result.detector}")

    print(f"Signal        : {result.signal}")

    print(f"Behavior      : {behavior['behavior_name']}")

    print(f"Confidence    : {behavior['confidence']}%")

    print(f"Risk Score    : {risk['risk_score']}")

    print(f"Risk Level    : {risk['risk_level']}")

    print(f"Decision      : {decision['decision']}")

    print(f"Response      : {response['status']}")

    print(f"Quarantine    : {quarantine_status}")

    print("=" * 65)

    print()

# ==========================================================
# File Monitor
# ==========================================================

class RansomwareMonitor(FileSystemEventHandler):

    def __init__(self):

        super().__init__()

    # ------------------------------------------------------

    def on_created(self, event):

        if event.is_directory:
            return

        self._scan(event.src_path)

    # ------------------------------------------------------

    def on_modified(self, event):

        if event.is_directory:
            return

        self._scan(event.src_path)

    # ------------------------------------------------------

    def on_moved(self, event):

        if event.is_directory:
            return

        self._scan(event.dest_path)

    # ------------------------------------------------------

    def _scan(self, file_path):

        try:

            if not os.path.exists(file_path):
                return

            if not os.path.isfile(file_path):
                return

            if "quarantine" in file_path.lower():
                return

            if "logs" in file_path.lower():
                return

            if "telemetry" in file_path.lower():
                return

            if file_path.endswith(".json"):
                return

            if file_path.endswith(".db"):
                return

            if file_path.endswith(".tmp"):
                return

            monitor_stats["files_monitored"] += 1

            results = detection_manager.detect(file_path)

            # ==============================
            # DEBUG OUTPUT
            # ==============================

            print("\n" + "=" * 50)
            print("FILE:", file_path)

            if not results:

                print("RESULTS: 0")

            else:

                print("RESULTS:", len(results))

                for r in results:

                    print(
                        r.detector,
                        "|",
                        r.signal,
                        "|",
                        r.severity,
                        "|",
                        r.detected
                    )

            print("=" * 50)

            # ==============================

            if not results:
                return

            for result in results:

                process_detection(
                    result,
                    file_path
                )
        except PermissionError:
            return

        except FileNotFoundError:
            return

        except Exception as e:

            print()

            

# ==========================================================
# Initial Scan
# ==========================================================
def initial_scan(path):
    if not os.path.exists(path):
        return

    for root, _, files in os.walk(path):

        for file in files:

            file_path = os.path.join(root, file)

            try:

                if not os.path.isfile(file_path):
                    continue

                if "quarantine" in file_path.lower():
                    continue

                if "logs" in file_path.lower():
                    continue

                if "telemetry" in file_path.lower():
                    continue

                if file_path.endswith(".json"):
                    continue

                if file_path.endswith(".db"):
                    continue

                if file_path.endswith(".tmp"):
                    continue

                monitor_stats["files_monitored"] += 1

                results = detection_manager.detect(file_path)

                # ==============================
                # DEBUG OUTPUT
                # ==============================

                print("\n" + "=" * 50)
                print("FILE:", file_path)

                if not results:

                    print("RESULTS: 0")

                else:

                    print("RESULTS:", len(results))

                    for r in results:

                        print(
                            r.detector,
                            "|",
                            r.signal,
                            "|",
                            r.severity,
                            "|",
                            r.detected
                        )

                print("=" * 50)

                # ==============================

                if not results:
                    continue

                for result in results:

                    process_detection(
                        result,
                        file_path
                    )

            except Exception as e:

                print("Initial Scan Error :", e)
# ==========================================================
# Start Monitoring
# ==========================================================

def start_monitoring(path):
    global monitor_running
    global observer

    # Stop previous observer if it exists
    if observer is not None:

        if observer.is_alive():

            observer.stop()

            observer.join()

    # Create a NEW observer every time
    observer = Observer()

    reset_statistics()

    initialize_dashboard()

    create_honeypot(path)

    time.sleep(1)

    monitor_running = True

    if not os.path.exists(path):

        raise FileNotFoundError(path)

    initial_scan(path)

    handler = RansomwareMonitor()

    observer.schedule(

        handler,

        path,

        recursive=True

    )

    if not observer.is_alive():

        observer.start()

    print()

    return observer


# ==========================================================
# Stop Monitoring
# ==========================================================

def stop_monitoring():

    global monitor_running
    global observer

    if observer is not None:

        if observer.is_alive():

            observer.stop()

            observer.join()

    observer = None

    monitor_running = False

    
# ==========================================================
# Monitor Status
# ==========================================================

def get_monitor_status():

    return {

        "running": observer.is_alive(),

        "files_monitored": monitor_stats["files_monitored"],

        "suspicious_events": monitor_stats["suspicious_events"],

        "files_quarantined": monitor_stats["files_quarantined"],

        "active_threats": monitor_stats["active_threats"]

    }
# ==========================================================
# Dashboard APIs
# ==========================================================

def get_live_events():

    return live_events


# ==========================================================
# Timeline
# ==========================================================

def get_threat_timeline():

    return threat_timeline


# ==========================================================
# Suspicious Files
# ==========================================================

def get_suspicious_files():

    return suspicious_files


# ==========================================================
# Statistics
# ==========================================================

def get_monitor_statistics():

    

    return {"running": observer is not None and observer.is_alive()}


# ==========================================================
# Analytics
# ==========================================================

def get_dashboard_analytics():

    try:

        return analytics_service.snapshot()

    except Exception:

        return {

            "severity": {},

            "behaviors": {},

            "decisions": {},

            "risk_history": [],

            "confidence_history": []

        }


# ==========================================================
# Incidents
# ==========================================================

def get_incidents():

    return incident_manager.all()


# ==========================================================
# Reset Runtime
# ==========================================================

def reset_runtime():

    live_events.clear()

    threat_timeline.clear()

    suspicious_files.clear()

    monitor_stats["files_monitored"] = 0

    monitor_stats["suspicious_events"] = 0

    monitor_stats["files_quarantined"] = 0

    monitor_stats["active_threats"] = 0

    initialize_dashboard()
# ==========================================================
# Runtime Helpers
# ==========================================================

def is_running():

    return observer is not None and observer.is_alive()


def active_incidents():

    return len(incident_manager.all())


def reset_statistics():

    monitor_stats["files_monitored"] = 0
    monitor_stats["suspicious_events"] = 0
    monitor_stats["files_quarantined"] = 0
    monitor_stats["active_threats"] = 0

    suspicious_files.clear()

    live_events.clear()

    threat_timeline.clear()

    analytics_service.reset()

    initialize_dashboard()