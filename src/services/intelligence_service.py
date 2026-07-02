"""
ARDS Intelligence Service
=========================

Provides the latest intelligence state
for the dashboard.
"""
from src.shared.runtime import live_events


def get_latest_intelligence():

    if not live_events:

        return {

            "behavior": "No Threat",

            "confidence": 0,

            "stage": "Safe",

            "risk_score": 0,

            "risk_level": "Low",

            "decision": "None",

            "priority": 0,

            "actions": [],

            "status": "Monitoring"

        }

    latest = live_events[0]

    return {

        "behavior": latest.get("behavior_name", "Unknown"),

        "confidence": latest.get("confidence", 0),

        "stage": latest.get("stage", "Observation"),

        "risk_score": latest.get("risk_score", 0),

        "risk_level": latest.get("risk_level", "Low"),

        "decision": latest.get("decision", "Observe"),

        "priority": latest.get("priority", 0),

        "actions": latest.get("actions", []),

        "status": latest.get("status", "Monitoring")

    }