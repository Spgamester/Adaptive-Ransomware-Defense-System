from src.detection.detection_manager import DetectionManager


manager = DetectionManager()

results = manager.detect("virus.locked")

print("=" * 60)
print("Detection Manager")
print("=" * 60)

for r in results:

    print("Detector   :", r.detector)
    print("Signal     :", r.signal)
    print("Severity   :", r.severity)
    print("Confidence :", r.confidence)
    print("Details    :", r.details)
    print("-" * 40)