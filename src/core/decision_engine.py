"""
ARDS Decision Engine
====================
Determines the response based on risk assessment.
"""

from src.knowledge.decision_profiles import DECISION_PROFILES


class DecisionEngine:

    def decide(self, risk):

        profile = DECISION_PROFILES.get(

            risk["risk_level"],

            DECISION_PROFILES["Low"]

        )

        return {

            "behavior_id": risk["behavior_id"],

            "behavior_name": risk["behavior_name"],

            "risk_score": risk["risk_score"],

            "risk_level": risk["risk_level"],

            "confidence": risk["confidence"],

            "decision": profile["decision"],

            "priority": profile["priority"],

            "notify": profile["notify"],

            "quarantine": profile["quarantine"],

            "evidence": risk["evidence"]

        }