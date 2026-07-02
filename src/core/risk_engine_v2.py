"""
ARDS Adaptive Risk Engine v2
"""

from src.knowledge.risk_profiles import RISK_PROFILES


class AdaptiveRiskEngine:

    def evaluate(self, behavior):

        profile = RISK_PROFILES.get(

            behavior["behavior_id"],

            RISK_PROFILES["UNKNOWN"]

        )

        base_risk = profile["risk_score"]

        confidence = behavior["confidence"]

        # Adaptive Risk Formula
        final_risk = min(

            int(base_risk + (confidence * 0.5)),

            100

        )

        if final_risk >= 90:

            level = "Critical"

        elif final_risk >= 70:

            level = "High"

        elif final_risk >= 40:

            level = "Medium"

        else:

            level = "Low"

        return {

            "behavior_id": behavior["behavior_id"],

            "behavior_name": behavior["behavior_name"],

            "confidence": confidence,

            "risk_score": final_risk,

            "risk_level": level,

            "decision": profile["decision"],

            "recommended_action":

                profile["recommended_action"],

            "evidence": behavior["evidence"]

        }