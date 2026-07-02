"""
ARDS Decision Knowledge Base
============================
Maps risk levels to security decisions.
"""

DECISION_PROFILES = {

    "Low": {

        "decision": "Observe",

        "priority": 1,

        "notify": False,

        "quarantine": False

    },

    "Medium": {

        "decision": "Monitor",

        "priority": 2,

        "notify": True,

        "quarantine": False

    },

    "High": {

        "decision": "Quarantine",

        "priority": 3,

        "notify": True,

        "quarantine": True

    },

    "Critical": {

        "decision": "Quarantine",

        "priority": 4,

        "notify": True,

        "quarantine": True

    }

}