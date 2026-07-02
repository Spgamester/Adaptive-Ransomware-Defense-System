import time
from collections import deque

from src.detection.detection_result import DetectionResult


class BurstDetector:

    WINDOW = 10
    THRESHOLD = 20

    def __init__(self):
        self.events = deque()
        self.file_events = {}

    def detect(self, file_path):

        now = time.time()

        self.events.append(now)

        while self.events and (now - self.events[0]) > self.WINDOW:

            self.events.popleft()

        if len(self.events) >= self.THRESHOLD:

            return DetectionResult(

                detected=True,

                detector="Burst Detector",

                signal="Mass File Modification",

                severity="High",

                confidence=85,

            details=f"{len(self.events)} file events in {self.WINDOW} seconds"

            )

        return DetectionResult(

            detected=False,

            detector="Burst Detector",

            signal="",

            severity="Low",

            confidence=0

        )