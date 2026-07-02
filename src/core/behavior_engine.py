"""
ARDS Behavior Evolution Engine
==============================

Converts correlated telemetry into high-level behavior objects.

This engine does NOT calculate risk.
It only identifies behaviors based on required and optional signals.
"""

from src.knowledge.behaviors import BEHAVIOR_REGISTRY


class BehaviorEngine:

    def analyze(self, correlation_group):

        observed_signals = {

            event["signal"]

            for event in correlation_group

        }

        best_behavior = None

        best_confidence = -1

        for behavior_id, behavior in BEHAVIOR_REGISTRY.items():

            required = set(behavior["required"])

            optional = set(behavior["optional"])

            forbidden = set(behavior["forbidden"])

            # --------------------------------------
            # Required signals must ALL exist
            # --------------------------------------

            if not required.issubset(observed_signals):
                continue

            # --------------------------------------
            # Forbidden signals must NOT exist
            # --------------------------------------

            if forbidden.intersection(observed_signals):
                continue

            # --------------------------------------
            # Count matches
            # --------------------------------------

            matched_required = len(required)

            matched_optional = len(

                observed_signals.intersection(optional)

            )

            total_matches = matched_required + matched_optional

            if total_matches < behavior["minimum_match"]:
                continue

            # --------------------------------------
            # Confidence
            # --------------------------------------

            confidence = min(

                100,

                int(
                    (total_matches /
                     (len(required) + len(optional))) * 100
                )

            )

            if confidence > best_confidence:

                best_confidence = confidence

                best_behavior = {

                    "behavior_id": behavior_id,

                    "behavior_name": behavior["name"],

                    "description": behavior["description"],

                    "confidence": confidence,

                    "evidence": list(

                        observed_signals.intersection(

                            required.union(optional)

                        )

                    )

                }

        # --------------------------------------
        # Unknown Behavior
        # --------------------------------------

        if best_behavior is None:

            return {

                "behavior_id": "UNKNOWN",

                "behavior_name": "Unknown Behavior",

                "description": "No behavior matched.",

                "confidence": 0,

                "stage": "Observation",

                "evidence": list(observed_signals)

            }

        confidence = best_behavior["confidence"]

        if confidence >= 80:

            stage = "Confirmed"

        elif confidence >= 50:

            stage = "Emerging"

        else:

            stage = "Observation"

        best_behavior["stage"] = stage

        return best_behavior