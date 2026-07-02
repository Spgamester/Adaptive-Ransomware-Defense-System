"""
ARDS Incident Manager
=====================

Maintains all active incidents.
"""

from src.incident.incident import Incident


class IncidentManager:

    def __init__(self):

        # key = file_path
        self.active_incidents = {}

    # ----------------------------------------

    def get_or_create(self, file_path):

        if file_path not in self.active_incidents:

            self.active_incidents[file_path] = Incident(file_path)

        return self.active_incidents[file_path]

    # ----------------------------------------

    def add_detection(self, file_path, result):

        incident = self.get_or_create(file_path)

        incident.add_detection(result)

        return incident

    # ----------------------------------------

    def update_incident(

        self,

        file_path,

        behavior,

        risk,

        decision,

        response

    ):

        incident = self.get_or_create(file_path)

        incident.update_intelligence(

            behavior,

            risk,

            decision,

            response

        )

        return incident

    # ----------------------------------------

    def close(self, file_path):

        if file_path in self.active_incidents:

            self.active_incidents[file_path].close()

    # ----------------------------------------

    def get(self, file_path):

        return self.active_incidents.get(file_path)

    # ----------------------------------------

    def all(self):

        return [

            incident.to_dict()

            for incident in self.active_incidents.values()

        ]