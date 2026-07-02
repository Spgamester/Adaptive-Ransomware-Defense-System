import os
import time
from src.utils.logger import alert
from src.core.entropy import calculate_entropy
from src.detection.detection_manager import DetectionManager
from src.core.monitoring import process_detection
from src.shared.runtime import scan_progress

from src.core.decision_engine import DecisionEngine 
from src.utils.quarantine import quarantine_file


detection_manager = DetectionManager()


def run_scan(path):

    import time

    start_time = time.time()

    scan_progress["running"] = True
    scan_progress["files_scanned"] = 0
    scan_progress["current_file"] = ""
    scan_progress["elapsed"] = 0

    scan_results = []
    files_scanned = 0

    print("Scanning existing files...")

    def scan_file(file_path):

        nonlocal files_scanned
        try:
            files_scanned += 1

            scan_progress["files_scanned"] = files_scanned

            scan_progress["current_file"] = os.path.basename(file_path)

            scan_progress["elapsed"] = round(

                time.time() - start_time,

                1

            )

            size = os.path.getsize(file_path)

            # Skip empty files
            if size == 0:

                scan_progress["running"] = False
                return

            results = detection_manager.detect(file_path)

            print("=" * 50)
            print("FILE:", file_path)
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

            entropy = calculate_entropy(file_path)

            print(
                f"Checking: {file_path} | Entropy: {entropy:.2f}"
            )

            if results:
                for result in results:

                    process_detection(
                        result,
                        file_path
                    )

                    scan_results.append({
                        "file": file_path,
                        "reason": result.signal,
                        "detector": result.detector,
                        "severity": result.severity,
                        "confidence": result.confidence
                    })

            elif entropy > 7.5:
                scan_results.append({
                    "file": file_path,
                    "reason": f"High entropy ({entropy:.2f})"
                })

        except Exception as e:
            print("Scan error:", e)

    # ----------------------
    # FILE / DIRECTORY SCAN
    # ----------------------

    total_files = 0

    if os.path.isfile(path):

        total_files = 1

    else:

        for root, dirs, files in os.walk(path):

            dirs[:] = [

                d for d in dirs

                if d.lower() not in {

                    "logs",

                    "quarantine",

                    "__pycache__",

                    ".git",

                    "node_modules",

                    "venv",

                    ".venv"

                }

            ]

            total_files += len(files)

    scan_progress["total_files"] = total_files

    if os.path.isfile(path):

        scan_file(path)

    else:

        for root, dirs, files in os.walk(path):

            dirs[:] = [
                d for d in dirs
                if d.lower() not in {
                    "logs",
                    "quarantine",
                    "__pycache__",
                    ".git",
                    "node_modules",
                    "venv",
                    ".venv"
                }
            ]

            for file in files:

                scan_file(
                    os.path.join(root, file)
                )

    # ----------------------
    # MONITORING
    # ----------------------
    print("Scan completed.")
    # ----------------------
    # COMBINE RESULTS
    # ----------------------

    final_results = scan_results

    threat_count = len(final_results)

    scan_time = round(
        time.time() - start_time,
        2
    )

    if threat_count == 0:

        return {

            "status": "SAFE",

            "files_scanned": files_scanned,

            "threat_count": 0,

            "scan_time": scan_time,

            "details": []

        }
    
    scan_progress["running"] = False

    return {

        "status": "RANSOMWARE DETECTED",

        "files_scanned": files_scanned,

        "threat_count": threat_count,

        "scan_time": scan_time,

        "details": final_results

    }

