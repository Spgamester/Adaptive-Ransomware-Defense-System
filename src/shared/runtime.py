"""
ARDS Runtime State
==================
Shared runtime state used across the application.
"""

live_events = []

threat_timeline = []

monitor_stats = {

    "files_monitored": 0,

    "processes_watching": 0,

    "suspicious_events": 0,

    "files_quarantined": 0,

    "active_threats": 0

}

scan_progress = {

    "running": False,

    "current_file": "",

    "files_scanned": 0,

    "total_files": 0,

    "elapsed": 0

}

suspicious_files = []