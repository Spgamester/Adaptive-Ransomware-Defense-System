from src.detection.detector_registry import DETECTOR_REGISTRY


class DetectionManager:

    def detect(self, file_path):

        results = []

        detectors = sorted(

            DETECTOR_REGISTRY,

            key=lambda d: d["priority"]

        )

        process_result = None

        for detector in detectors:

            if not detector["enabled"]:

                continue

            try:

                # ----------------------------
                # Process Detector
                # ----------------------------

                if detector["name"] == "Process Detector":

                    if process_result is None:

                        process_result = detector["instance"].detect()

                        if process_result.detected:

                            results.append(process_result)

                    continue

                # ----------------------------
                # File Detectors
                # ----------------------------

                result = detector["instance"].detect(file_path)

                if result.detected:

                    results.append(result)

            except Exception as e:

                print(f"[{detector['name']}]", e)

        return results