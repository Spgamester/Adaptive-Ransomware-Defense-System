import os

from src.detection.detection_result import DetectionResult

from src.knowledge.ransomware_extensions import (
    RANSOMWARE_EXTENSIONS
)


class ExtensionDetector:

    def detect(self, file_path):

        extension = os.path.splitext(file_path)[1].lower()

        if extension in RANSOMWARE_EXTENSIONS:

            return DetectionResult(

                detected=True,

                detector="Extension Detector",

                signal="Suspicious Extension",

                severity="Medium",

                confidence=40,

                details=extension

            )

        return DetectionResult(

            detected=False,

            detector="Extension Detector",

            signal="",

            severity="Low",

            confidence=0

        )