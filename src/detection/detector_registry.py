"""
ARDS Detector Registry
======================

Central registry for every detector.
"""
from src.detection.entropy_detector import EntropyDetector
from src.detection.extension_detector import ExtensionDetector
from src.detection.burst_detector import BurstDetector
from src.detection.ml_detector import MLDetector
from src.detection.honeypot_detector import HoneypotDetector
from src.detection.hash_detector import HashDetector
from src.detection.process_detector import ProcessDetector


DETECTOR_REGISTRY = [

    {
        "name": "Entropy Detector",
        "priority": 1,
        "enabled": True,
        "instance": EntropyDetector()
    },

    {
        "name": "Extension Detector",
        "priority": 2,
        "enabled": True,
        "instance": ExtensionDetector()
    },

    {
        "name": "Burst Detector",
        "priority": 3,
        "enabled": True,
        "instance": BurstDetector()
    },

    {
        "name": "ML Detector",
        "priority": 4,
        "enabled": True,
        "instance": MLDetector()
    },

    {
        "name": "Honeypot Detector",
        "priority": 5,
        "enabled": True,
        "instance": HoneypotDetector()
    },

    {
        "name": "Hash Detector",
        "priority": 6,
        "enabled": True,
        "instance": HashDetector()
    },

    {
        "name": "Process Detector",
        "priority": 7,
        "enabled": True,
        "instance": ProcessDetector()
    }

]