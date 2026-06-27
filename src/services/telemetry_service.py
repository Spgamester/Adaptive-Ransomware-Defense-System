from src.core.monitoring import (
    live_events,
    threat_timeline
)


def get_recent_alerts(limit=20):
    """
    Return the latest detection events
    for Dashboard, Reports and Notifications.
    """

    return live_events[:limit]


def get_live_events():
    """
    Return every live monitoring event.
    """

    return live_events


def get_timeline():
    """
    Timeline used by Monitor Page
    and Investigation View.
    """

    return threat_timeline