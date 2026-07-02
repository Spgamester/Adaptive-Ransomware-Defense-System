"""
ARDS Risk Knowledge Base
========================

Defines the default risk associated with
every known behavior.

The Risk Engine never hardcodes risk values.
"""

RISK_PROFILES = {

    "BEH-001": {

        "risk_score": 90,

        "risk_level": "Critical",

        "decision": "Quarantine",

        "recommended_action":
            "Immediately isolate the affected endpoint."

    },

    "BEH-002": {

        "risk_score": 45,

        "risk_level": "Medium",

        "decision": "Monitor",

        "recommended_action":
            "Continue monitoring for additional evidence."

    },

    "BEH-003": {

        "risk_score": 98,

        "risk_level": "Critical",

        "decision": "Emergency Isolation",

        "recommended_action":
            "Immediately isolate endpoint and terminate encryption process."

    },

    "UNKNOWN": {

        "risk_score": 15,

        "risk_level": "Low",

        "decision": "Observe",

        "recommended_action":
            "Collect additional telemetry."

    }

}