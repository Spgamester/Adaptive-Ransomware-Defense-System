"""
ARDS Behavior Knowledge Base
============================

Behavior definitions used by the Behavior Engine.
"""

BEHAVIOR_REGISTRY = {

    "BEH-001": {

        "name": "Encryption Behavior",

        "description":
            "File encryption activity has been observed.",

        "required": [
            "High Entropy Detected"
        ],

        "optional": [
            "Machine Learning Detection",
            "Mass Modification"
        ],

        "forbidden": [],

        "minimum_match": 2

    },

    "BEH-002": {

        "name": "Suspicious File Activity",

        "description":
            "Suspicious file operations detected.",

        "required": [
            "Suspicious Extension"
        ],

        "optional": [
            "Initial Scan Detection",
            "High Entropy Detected"
        ],

        "forbidden": [],

        "minimum_match": 2

    },

    "BEH-003": {

        "name": "Aggressive Encryption",

        "description":
            "Multiple ransomware indicators confirm an active attack.",

        "required": [
            "Mass File Modification"
        ],

        "optional": [
            "High Entropy Detected",
            "Machine Learning Detection",
            "Known Malware Hash",
            "Suspicious Extension",
            "Honeypot Triggered",
            "Suspicious Process"
        ],

        "forbidden": [],

        "minimum_match": 2

    }

}