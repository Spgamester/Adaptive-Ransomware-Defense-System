import os

from src.detection.detection_result import DetectionResult


class HoneypotDetector:

    def detect(self, file_path):

        if "ARDS_Honeypot" not in file_path:

            return DetectionResult(

                detected=False,

                detector="Honeypot Detector",

                signal="",

                severity="Low",

                confidence=0

            )

        return DetectionResult(

            detected=True,

            detector="Honeypot Detector",

            signal="Honeypot Triggered",

            severity="Critical",

            confidence=100,

            details="Protected decoy file accessed."

        )