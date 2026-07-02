from src.core.entropy import calculate_entropy
from src.detection.detection_result import DetectionResult


class EntropyDetector:

    def detect(self, file_path):

        try:

            entropy = calculate_entropy(file_path)

            if entropy >= 7.5:

                return DetectionResult(

                    detected=True,

                    detector="Entropy Detector",

                    signal="High Entropy Detected",

                    severity="High",

                    confidence=80,

                    details=f"Entropy={entropy:.2f}"

                )

            return DetectionResult(

                detected=False,

                detector="Entropy Detector",

                signal="",

                severity="Low",

                confidence=0,

                details=f"Entropy={entropy:.2f}"

            )

        except Exception:

            return DetectionResult(

                detected=False,

                detector="Entropy Detector",

                signal="",

                severity="Low",

                confidence=0

            )