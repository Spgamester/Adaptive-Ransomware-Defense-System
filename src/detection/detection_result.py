from dataclasses import dataclass


@dataclass
class DetectionResult:

    detected: bool

    detector: str

    signal: str

    severity: str

    confidence: int

    details: str = ""