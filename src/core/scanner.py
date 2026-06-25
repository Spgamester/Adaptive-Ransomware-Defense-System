import os
import time
from src.utils.logger import alert
from src.core.entropy import calculate_entropy
from src.core.detector import predict_file
from src.core.monitoring import start_monitoring, suspicious_files


def run_scan(path):

    import time

    start_time = time.time()

    scan_results = []
    files_scanned = 0

    print("Scanning existing files...")

    def scan_file(file_path):

        nonlocal files_scanned

        try:

            files_scanned += 1

            entropy = calculate_entropy(file_path)

            print(
                f"Checking: {file_path} | Entropy: {entropy}"
            )

            ml_result = predict_file(file_path)

            if entropy > 7.0:

                reason = (
                    f"High entropy "
                    f"(encryption-like) + {ml_result}"
                )

                scan_results.append({
                    "file": file_path,
                    "reason": reason
                })

                alert(reason, file_path)

            elif file_path.lower().endswith(
                (".bin", ".enc", ".locked")
            ):

                reason = (
                    f"Suspicious extension + "
                    f"{ml_result}"
                )

                scan_results.append({
                    "file": file_path,
                    "reason": reason
                })

                alert(reason, file_path)

        except Exception as e:

            print("Scan error:", e)

    # ----------------------
    # FILE / DIRECTORY SCAN
    # ----------------------

    if os.path.isfile(path):

        scan_file(path)

    else:

        for root, dirs, files in os.walk(path):

            for file in files:

                scan_file(
                    os.path.join(root, file)
                )

    # ----------------------
    # MONITORING
    # ----------------------

    observer = start_monitoring(path)

    print("Monitoring started...")

    time.sleep(5)

    observer.stop()

    observer.join()

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

    return {

        "status": "RANSOMWARE DETECTED",

        "files_scanned": files_scanned,

        "threat_count": threat_count,

        "scan_time": scan_time,

        "details": final_results

    }

