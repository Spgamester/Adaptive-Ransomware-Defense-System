"""
ARDS File Scanner

Scans a single executable using the ML predictor.
"""

import hashlib
import time
from pathlib import Path
from datetime import datetime

from src.ml.predictor import Predictor
from src.scanner.scan_result import ScanResult


class FileScanner:

    def __init__(self):
        self.predictor = Predictor()

    @staticmethod
    def calculate_sha256(file_path: Path) -> str:
        """
        Calculate SHA256 hash of a file.
        """
        sha256 = hashlib.sha256()

        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(8192)

                if not chunk:
                    break

                sha256.update(chunk)

        return sha256.hexdigest()

    def scan(self, file_path: str) -> ScanResult:

        file = Path(file_path)

        if not file.exists():
            raise FileNotFoundError(file)

        start = time.perf_counter()

        prediction = self.predictor.predict(str(file))

        end = time.perf_counter()

        return ScanResult(
            file_path=str(file.resolve()),
            file_name=file.name,
            sha256=self.calculate_sha256(file),
            file_size=file.stat().st_size,

            prediction=prediction["prediction"],
            is_malware=prediction["is_malware"],

            malware_probability=prediction["malware_probability"],
            benign_probability=prediction["benign_probability"],

            scan_time_seconds=round(end - start, 3),

            scanned_at=datetime.now(),

            status="Malicious" if prediction["is_malware"] else "Clean"
        )