import hashlib

from src.detection.detection_result import DetectionResult
from src.knowledge.hash_database import KNOWN_HASHES


class HashDetector:

    def detect(self, file_path):

        try:

            with open(file_path, "rb") as f:

                sha256 = hashlib.sha256(

                    f.read()

                ).hexdigest()

            if sha256 in KNOWN_HASHES:

                return DetectionResult(

                    detected=True,

                    detector="Hash Detector",

                    signal="Known Malware Hash",

                    severity="Critical",

                    confidence=100,

                    details=KNOWN_HASHES[sha256]["family"]

                )

            return DetectionResult(

                detected=False,

                detector="Hash Detector",

                signal="",

                severity="Low",

                confidence=0,

                details=sha256

            )

        except Exception:

            return DetectionResult(

                detected=False,

                detector="Hash Detector",

                signal="",

                severity="Low",

                confidence=0

            )