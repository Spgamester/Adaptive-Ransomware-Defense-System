import os
import src.core.monitoring as monitoring
from src.utils.restore import restore_file
from src.utils.delete_file import delete_quarantined_file
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.utils.settings_manager import save_settings
from src.core.scanner import run_scan
from src.core.monitoring import (
    live_events,
    threat_timeline,
    monitor_stats,
    monitor_running,
    start_monitoring,
    stop_monitoring
)
from src.utils.settings_manager import (
    load_settings
)
from src.services.dashboard_service import (
    get_dashboard_stats
)
class MonitorRequest(BaseModel):
    path: str

app = FastAPI(title="ARDS API")
scan_history = []

# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "ARDS Backend Running"
    }


@app.get("/api/dashboard")
def dashboard():

    return get_dashboard_stats()
@app.get("/api/monitor")
def monitor():

    return monitor_stats


@app.get("/api/quarantine")
def quarantine():

    quarantine_folder = "quarantine"

    if not os.path.exists(
        quarantine_folder
    ):
        return {
            "threats_isolated": 0,
            "files_quarantined": 0,
            "risk_score": 0,
            "storage_used": "0 KB"
        }

    files = os.listdir(
        quarantine_folder
    )

    file_count = len(files)

    total_size = 0

    for file in files:

        path = os.path.join(
            quarantine_folder,
            file
        )

        if os.path.isfile(path):

            total_size += os.path.getsize(
                path
            )

    storage_mb = round(
        total_size / (1024 * 1024),
        2
    )

    risk_score = min(
        file_count * 10,
        100
    )

    return {
        "threats_isolated": file_count,
        "files_quarantined": file_count,
        "risk_score": risk_score,
        "storage_used": f"{storage_mb} MB"
    }


@app.get("/api/settings")
def get_settings():

    return load_settings()

@app.post("/api/settings")
def update_settings(settings: dict):

    save_settings(settings)

    return {
        "success": True,
        "message": "Settings Saved Successfully"
    }

@app.get("/api/alerts")
def alerts():
    return [
        {
            "time": "11:59",
            "severity": "Critical",
            "alert": "Ransomware Behavior Detected",
            "status": "Blocked"
        },
        {
            "time": "09:56",
            "severity": "High",
            "alert": "Mass Encryption Attempt",
            "status": "Contained"
        },
        {
            "time": "09:40",
            "severity": "Medium",
            "alert": "Suspicious Process Activity",
            "status": "Monitoring"
        }
    ]

@app.get("/api/threats")
def threats():
    return [
        {
            "file": "invoice.exe",
            "family": "LockBit",
            "risk": "Critical"
        },
        {
            "file": "payload.dll",
            "family": "BlackCat",
            "risk": "High"
        }
    ]
import os

@app.get("/api/quarantine-files")
def quarantine_files():

    quarantine_folder = "quarantine"

    if not os.path.exists(quarantine_folder):
        return []

    files = []

    for index, filename in enumerate(
        os.listdir(quarantine_folder)
    ):
        path = os.path.join(
            quarantine_folder,
            filename
        )

        size_kb = round(
            os.path.getsize(path) / 1024,
            2
        )

        files.append({
            "id": index + 1,
            "file": filename,
            "family": "Unknown",
            "risk": "Critical",
            "status": "Quarantined",
            "size": f"{size_kb} KB"
        })
    return files
class ScanRequest(BaseModel):
    path: str


from datetime import datetime


@app.post("/api/scan")
def scan(request: ScanRequest):

    result = run_scan(request.path)

    scan_history.append({

        "time": datetime.now().strftime("%H:%M:%S"),

        "status": result["status"],

        "files_scanned": result["files_scanned"],

        "threat_count": result["threat_count"],

        "scan_time": result["scan_time"]

    })

    return result
@app.get("/api/scan-history")
def get_scan_history():

    return list(reversed(scan_history))
@app.post("/api/restore/{filename}")
def restore_quarantine_file(
    filename: str
):

    success, message = (
        restore_file(filename)
    )

    return {
        "success": success,
        "message": message
    }
@app.delete("/api/delete/{filename}")
def delete_quarantine_file(
    filename: str
):

    success, message = (
        delete_quarantined_file(
            filename
        )
    )

    return {
        "success": success,
        "message": message
    }
@app.get("/api/threat-intelligence")
def threat_intelligence():
    return {
        "sha256": "8f3a7b21f9dce4e5b7a92d11d0ab4f6c",
        "path": "C:/Users/Admin/Downloads/invoice.exe",
        "detection_time": "2026-06-22 12:01 PM",
        "status": "Quarantined",
        "family": "LockBit",
        "score": 98
    }
@app.get("/api/live-events")
def get_live_events():

        return monitoring.live_events
@app.get("/api/threat-timeline")
def get_timeline():

    return monitoring.threat_timeline

@app.get("/api/monitor-status")
def monitor_status():

    return {
        "running": monitoring.monitor_running
    }

@app.post("/api/start-monitoring")
def start_monitor(request: MonitorRequest):

    monitoring.start_monitoring(request.path)

    return {
        "message": "Monitoring Started"
    }
@app.post("/api/stop-monitoring")
def stop_monitor():

    monitoring.stop_monitoring()

    return {
        "message": "Monitoring Stopped"
    }