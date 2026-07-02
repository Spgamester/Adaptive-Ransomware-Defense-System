import psutil
from src.shared.runtime import (
    live_events,
    monitor_stats
)


def get_dashboard_data():

    low = 0
    medium = 0
    high = 0
    critical = 0

    for event in live_events:

        severity = event.get("severity", "").lower()

        if severity == "low":
            low += 1

        elif severity == "medium":
            medium += 1

        elif severity == "high":
            high += 1

        elif severity == "critical":
            critical += 1

    # ==========================================
    # Dynamic Security Score
    # ==========================================

    security_score = 100

    # Severity penalties
    security_score -= low * 2
    security_score -= medium * 6
    security_score -= high * 12
    security_score -= critical * 20

    # Reward successful quarantine
    security_score += monitor_stats["files_quarantined"] * 2

    # Clamp score
    security_score = max(0, min(100, security_score))

    return {

        "security_score": security_score,

        "detection_engines": 7,

        "threats_blocked":
            monitor_stats["files_quarantined"],

        "critical_threats":
            monitor_stats["active_threats"],

        "files_scanned":
            monitor_stats["files_monitored"],

        "severity":{

            "low":low,

            "medium":medium,

            "high":high,

            "critical":critical

        }

    }

    
    


def get_attack_vectors():
    vectors = {

        "Entropy": 0,
        "ML": 0,
        "Extension": 0,
        "Hash": 0,
        "Burst": 0,
        "Process": 0,
        "Honeypot": 0

    }

    for event in live_events:

        detector = event.get("source", "").lower()

        if "entropy" in detector:
            vectors["Entropy"] += 1

        elif "ml" in detector:
            vectors["ML"] += 1

        elif "extension" in detector:
            vectors["Extension"] += 1

        elif "hash" in detector:
            vectors["Hash"] += 1

        elif "burst" in detector:
            vectors["Burst"] += 1

        elif "process" in detector:
            vectors["Process"] += 1

        elif "honeypot" in detector:
            vectors["Honeypot"] += 1

    return [

        {

            "name": k,

            "value": v

        }

        for k, v in vectors.items()

        if v > 0

    ]

def get_mitre_mapping():

    latest = None

    if live_events:
        latest = live_events[0]

    if latest is None:

        return {
            "technique": "No Threats",
            "id": "-",
            "confidence": 0,
            "reason": "No suspicious activity detected"
        }

    event = latest.get("event", "").lower()

    if "entropy" in event:

        return {
            "id": "T1486",
            "technique": "Data Encrypted for Impact",
            "confidence": 96,
            "reason": "High entropy indicates possible ransomware encryption."
        }

    elif "mass" in event:

        return {
            "id": "T1485",
            "technique": "Data Destruction",
            "confidence": 92,
            "reason": "Large-scale file modification detected."
        }

    elif "initial scan" in event:

        return {
            "id": "T1204",
            "technique": "User Execution",
            "confidence": 80,
            "reason": "Suspicious file identified during initial scan."
        }

    elif "extension" in event:

        return {
            "id": "T1486",
            "technique": "Data Encrypted for Impact",
            "confidence": 88,
            "reason": "Known ransomware extension detected."
        }

    return {

        "id": "Unknown",

        "technique": "Behavior Under Investigation",

        "confidence": 60,

        "reason": "Awaiting additional telemetry."

    }