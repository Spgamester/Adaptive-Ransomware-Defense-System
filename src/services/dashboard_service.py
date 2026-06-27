import psutil
from src.core.monitoring import (
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

    for event in live_events:

        severity = event.get("severity", "").lower()

        if severity == "low":
            security_score -= 2

        elif severity == "medium":
            security_score -= 6

        elif severity == "high":
            security_score -= 12

        elif severity == "critical":
            security_score -= 20

    security_score = max(0, security_score)

    return {

        "security_score": security_score,

        "active_monitors":
        len(psutil.pids()),

        "threats_blocked":
            monitor_stats["files_quarantined"],

        "critical_threats":
            critical,

        "files_scanned":
            monitor_stats["files_monitored"],

        "severity": {

            "low": low,

            "medium": medium,

            "high": high,

            "critical": critical

        }

    }
def get_attack_vectors():

    vectors = {

        "Entropy Detection": 0,

        "Behavior Analysis": 0,

        "Machine Learning": 0,

        "Mass Modification": 0,

        "Static Detection": 0

    }

    for event in live_events:

        name = event.get("event", "").lower()

        if "entropy" in name:

            vectors["Entropy Detection"] += 1

        elif "mass" in name:

            vectors["Mass Modification"] += 1

        elif "initial scan" in name:

            vectors["Static Detection"] += 1

        elif "behavior" in name:

            vectors["Behavior Analysis"] += 1

        elif "ml" in name or "machine" in name:

            vectors["Machine Learning"] += 1

    return [

        {

            "name": key,

            "value": value

        }

        for key, value in vectors.items()

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