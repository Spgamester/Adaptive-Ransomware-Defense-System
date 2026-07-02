"""
ARDS Incident Model
===================

Represents a single security incident.

Each suspicious file has its own incident.
"""

import uuid
import time


class Incident:

    def __init__(self, file_path):

        self.id = str(uuid.uuid4())[:8]

        self.file_path = file_path

        self.file_name = file_path.split("\\")[-1]

        self.created_at = time.strftime("%H:%M:%S")

        self.updated_at = self.created_at

        self.status = "Open"

        self.behavior = None

        self.risk = None

        self.decision = None

        self.response = None

        self.detectors = []

        self.evidence = []

        self.confidence = 0

        self.risk_score = 0

    # ----------------------------------

    def add_detection(self, result):

        self.detectors.append(result.detector)

        self.evidence.append({

            "detector": result.detector,

            "signal": result.signal,

            "severity": result.severity,

            "confidence": result.confidence,

            "details": result.details

        })

        self.updated_at = time.strftime("%H:%M:%S")

    # ----------------------------------

    def update_intelligence(

        self,

        behavior,

        risk,

        decision,

        response

    ):

        self.behavior = behavior

        self.risk = risk

        self.decision = decision

        self.response = response

        self.confidence = behavior["confidence"]

        self.risk_score = risk["risk_score"]

        self.updated_at = time.strftime("%H:%M:%S")

    # ----------------------------------

    def close(self):

        self.status = "Closed"

        self.updated_at = time.strftime("%H:%M:%S")

    # ----------------------------------

    def to_dict(self):

        return {

            "incident_id": self.id,

            "file_name": self.file_name,

            "file_path": self.file_path,

            "status": self.status,

            "created_at": self.created_at,

            "updated_at": self.updated_at,

            "behavior": self.behavior,

            "risk": self.risk,

            "decision": self.decision,

            "response": self.response,

            "confidence": self.confidence,

            "risk_score": self.risk_score,

            "detectors": self.detectors,

            "evidence": self.evidence

        }