from collections import Counter

severity_counter = Counter()

behavior_counter = Counter()

decision_counter = Counter()

risk_history = []

confidence_history = []


MAX_HISTORY = 50


def update(event):

    severity = event.get("risk_level")
    behavior = event.get("behavior_name")
    decision = event.get("decision")

    if severity:
        severity_counter[severity] += 1

    if behavior:
        behavior_counter[behavior] += 1

    if decision:
        decision_counter[decision] += 1

    risk_history.append(
        event.get("risk_score", 0)
    )

    confidence_history.append(
        event.get("confidence", 0)
    )

    if len(risk_history) > MAX_HISTORY:
        risk_history.pop(0)

    if len(confidence_history) > MAX_HISTORY:
        confidence_history.pop(0)


def snapshot():

    return {

        "severity": dict(severity_counter),

        "behaviors": dict(behavior_counter),

        "decisions": dict(decision_counter),

        "risk_history": risk_history,

        "confidence_history": confidence_history

    }


def reset():

    severity_counter.clear()

    behavior_counter.clear()

    decision_counter.clear()

    risk_history.clear()

    confidence_history.clear()