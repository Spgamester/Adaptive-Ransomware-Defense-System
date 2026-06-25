import src.core.monitoring as monitoring

from src.utils.settings_manager import load_settings


def calculate_security_score():

    settings = load_settings()

    score = 100

    # ----------------------------
    # Monitoring Status
    # ----------------------------

    if not monitoring.monitor_running:
        score -= 30

    # ----------------------------
    # Protection Settings
    # ----------------------------

    if not settings.get("real_time", True):
        score -= 15

    if not settings.get("entropy", True):
        score -= 10

    if not settings.get("heuristic", True):
        score -= 10

    if not settings.get("threat_alerts", True):
        score -= 5

    if not settings.get("auto_quarantine", True):
        score -= 5

    # ----------------------------
    # Active Threats
    # ----------------------------

    score -= (
        monitoring.monitor_stats["active_threats"] * 15
    )

    # ----------------------------
    # Clamp Score
    # ----------------------------

    score = max(0, min(score, 100))

    return score


def get_dashboard_stats():

    security_score = calculate_security_score()

    active_monitors = (
        1 if monitoring.monitor_running else 0
    )

    return {

        "security_score": security_score,

        "active_monitors": active_monitors,

        "threats_blocked":
            monitoring.monitor_stats[
                "files_quarantined"
            ],

        "critical_threats":
            monitoring.monitor_stats[
                "active_threats"
            ],

        "files_scanned":
            monitoring.monitor_stats[
                "files_monitored"
            ]

    }