import os
from src.core.detector import predict_file
from src.detection.detection_result import DetectionResult



class MLDetector:

    

    def detect(self, file_path):

        extension = os.path.splitext(file_path)[1].lower()

        if extension not in {
            ".exe",
            ".dll",
            ".sys",
            ".scr",
            ".com",
            ".drv"
        }:
            return DetectionResult(
                detected=False,
                detector="ML Detector",
                signal="",
                severity="Low",
                confidence=0
            )

        try:

            print("\n========== ML DETECTOR ==========")
            print("Analyzing:", file_path)

            prediction = predict_file(file_path)

            print(prediction)
            print("===============================")

            if prediction["is_malware"]:

                confidence = round(
                    prediction["malware_probability"] * 100,
                    2
                )

                return DetectionResult(

                    detected=True,

                    detector="ML Detector",

                    signal="Machine Learning Detection",

                    severity="High",

                    confidence=confidence,

                    details=f"ML Confidence: {confidence}%"

                )

        except Exception as e:

            print("[ML Detector]", e)

        return DetectionResult(

            detected=False,

            detector="ML Detector",

            signal="",

            severity="Low",

            confidence=0

        )