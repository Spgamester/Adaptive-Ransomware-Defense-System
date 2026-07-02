"""
ARDS Scan Result

Represents the result of scanning a single file.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class ScanResult:
    file_path: str
    file_name: str
    sha256: str
    file_size: int

    prediction: int
    is_malware: bool

    malware_probability: float
    benign_probability: float

    scan_time_seconds: float

    scanned_at: datetime

    status: str