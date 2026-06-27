"""
ARDS Behavior Correlation Engine
Version 1.0

Collects recent detection signals and correlates them
before sending them to the Risk Engine.
"""

from collections import deque
import time

# Store recent detection signals (last 30 seconds)
signal_buffer = deque(maxlen=100)


def add_signal(signal):

    signal_buffer.append({

        "signal": signal,

        "timestamp": time.time()

    })


def get_recent_signals(window=30):

    now = time.time()

    recent = []

    for item in signal_buffer:

        if now - item["timestamp"] <= window:

            recent.append(item["signal"])

    return recent

def detect_behavior_pattern():
    signals = get_recent_signals()
    signal_set = set(signals)

    # Encryption Behaviour
    if (
        "High Entropy Detected" in signal_set
        and "Mass Modification" in signal_set
    ):
        return {
            "pattern": "Encryption Behavior",
            "confidence": 95,
            "signals": signals
        }

    # Suspicious File Activity
    if (
        "Suspicious Extension" in signal_set
        and "Initial Scan Detection" in signal_set
    ):
        return {
            "pattern": "Suspicious File Activity",
            "confidence": 80,
            "signals": signals
        }

    # Generic Behaviour
    return {
        "pattern": "Unknown",
        "confidence": 40,
        "signals": signals
    }


def clear_old_signals(window=30):

    now = time.time()

    while signal_buffer:

        if now - signal_buffer[0]["timestamp"] > window:

            signal_buffer.popleft()

        else:

            break