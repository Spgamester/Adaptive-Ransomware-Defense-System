"""
ARDS Adaptive Risk Engine
Version 1.0

This module combines multiple detection signals into
one adaptive risk score and returns an explainable decision.
"""

RISK_WEIGHTS = {

    "High Entropy Detected": 30,

    "Suspicious Extension": 20,

    "Mass Modification": 35,

    "Initial Scan Detection": 10,

    "Machine Learning Detection": 25,

}


DECISION_LEVELS = [

    (80, "Critical Response"),

    (60, "Quarantine"),

    (30, "Warning"),

    (0, "Monitor")

]


def evaluate_risk(signals):

    """
    signals

    Example:

    [

        "High Entropy Detected",

        "Mass Modification",

        "Machine Learning Detection"

    ]
    """

    score = 0

    matched = []

    for signal in signals:

        for key, weight in RISK_WEIGHTS.items():

            if key.lower() in signal.lower():

                score += weight

                matched.append(key)

    score = min(score, 100)

    decision = "Monitor"

    for threshold, action in DECISION_LEVELS:

        if score >= threshold:

            decision = action

            break

    confidence = min(

        50 + score // 2,

        99

    )

    return {

        "risk_score": score,

        "decision": decision,

        "confidence": confidence,

        "signals": matched

    }