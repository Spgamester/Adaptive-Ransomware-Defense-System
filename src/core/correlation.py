"""
ARDS Correlation Engine
=======================

Purpose:
Group telemetry events that occur within a configurable
time window.

This module NEVER calculates risk.
This module NEVER makes decisions.

It only correlates observations.
"""

from datetime import datetime, timedelta

from src.core.telemetry import get_telemetry


class CorrelationEngine:

    def __init__(self, window_seconds=30):

        self.window = timedelta(seconds=window_seconds)

    def correlate(self):

        events = get_telemetry()

        if not events:
            return []

        correlated_groups = []

        current_group = []

        previous_time = None

        # Telemetry is stored newest first.
        # We reverse so we process oldest -> newest.
        ordered_events = list(reversed(events))

        for event in ordered_events:

            event_time = datetime.strptime(
                event["timestamp"],
                "%Y-%m-%d %H:%M:%S"
            )

            if previous_time is None:

                current_group.append(event)

            else:

                if event_time - previous_time <= self.window:

                    current_group.append(event)

                else:

                    correlated_groups.append(current_group)

                    current_group = [event]

            previous_time = event_time

        if current_group:

            correlated_groups.append(current_group)

        return correlated_groups