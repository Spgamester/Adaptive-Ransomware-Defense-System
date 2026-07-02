"""
ARDS Telemetry Layer
====================

Purpose:
- Standardize every event generated inside ARDS.
- Acts as the single source of truth for telemetry.

IMPORTANT:
Do NOT calculate risk here.
Do NOT make decisions here.
Do NOT quarantine here.

This module ONLY stores observations.
"""

from datetime import datetime
import uuid

telemetry_stream = []


class TelemetryEvent:

    def __init__(
        self,
        source,
        signal,
        severity="Low",
        category="General",
        file_name="",
        file_path="",
        process="",
        user="SYSTEM",
        confidence=0,
        mitre="",
        metadata=None,
    ):

        if metadata is None:
            metadata = {}

        self.event = {

            "id": str(uuid.uuid4()),

            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "source": source,

            "signal": signal,

            "severity": severity,

            "category": category,

            "confidence": confidence,

            "mitre": mitre,

            "file_name": file_name,

            "file_path": file_path,

            "process": process,

            "user": user,

            "metadata": metadata

        }

    def emit(self):

        telemetry_stream.insert(0, self.event)

        return self.event


def get_telemetry():

    return telemetry_stream


def clear_telemetry():

    telemetry_stream.clear()