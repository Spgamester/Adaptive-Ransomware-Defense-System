from src.core.telemetry import TelemetryEvent, clear_telemetry
from src.core.correlation import CorrelationEngine

# Reset telemetry
clear_telemetry()

# Create fake telemetry events
TelemetryEvent(
    source="Entropy",
    signal="High Entropy",
    severity="High"
).emit()

TelemetryEvent(
    source="Filesystem",
    signal="Mass Modification",
    severity="Critical"
).emit()

TelemetryEvent(
    source="ML",
    signal="Machine Learning Detection",
    severity="High"
).emit()

# Correlate
engine = CorrelationEngine(window_seconds=30)

groups = engine.correlate()

print("=" * 50)

print("Correlation Groups:", len(groups))

print("=" * 50)

for i, group in enumerate(groups, start=1):

    print(f"\nGroup {i}")

    for event in group:

        print(f"- {event['source']} -> {event['signal']}")