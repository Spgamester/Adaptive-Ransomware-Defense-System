import psutil

from src.detection.detection_result import DetectionResult


SUSPICIOUS = {

    "encrypt.exe",

    "locker.exe",

    "lockbit.exe",

    "wannacry.exe",

    "blackcat.exe",

    "conti.exe"

}


class ProcessDetector:

    def detect(self, file_path=None):

        try:

            for process in psutil.process_iter(

                ["name", "cpu_percent"]

            ):

                name = (

                    process.info["name"] or ""

                ).lower()

                cpu = (

                    process.info["cpu_percent"] or 0

                )

                if name in SUSPICIOUS:

                    return DetectionResult(

                        detected=True,

                        detector="Process Detector",

                        signal="Suspicious Process",

                        severity="Critical",

                        confidence=100,

                        details=name

                    )

                if cpu > 80:

                    return DetectionResult(

                        detected=True,

                        detector="Process Detector",

                        signal="High CPU Encryption Activity",

                        severity="High",

                        confidence=80,

                        details=f"{name} ({cpu}%)"

                    )

        except Exception:

            pass

        return DetectionResult(

            detected=False,

            detector="Process Detector",

            signal="",

            severity="Low",

            confidence=0

        )