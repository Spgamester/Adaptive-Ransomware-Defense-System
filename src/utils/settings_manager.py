import json
import os

SETTINGS_FILE = "settings.json"


DEFAULT_SETTINGS = {

    # ======================
    # General Protection
    # ======================

    "auto_scan": True,
    "real_time": True,
    "auto_quarantine": True,
    "launch_startup": False,

    # ======================
    # Detection Engines
    # ======================

    "ml_detection": True,
    "heuristic": True,
    "entropy": True,
    "behavior_monitoring": True,

    # ======================
    # Notifications
    # ======================

    "threat_alerts": True,
    "email_alerts": False,
    "desktop_notifications": True,
    "quarantine_notifications": True

}
def load_settings():

    if not os.path.exists(SETTINGS_FILE):

        save_settings(DEFAULT_SETTINGS)

        return DEFAULT_SETTINGS

    try:

        with open(
            SETTINGS_FILE,
            "r"
        ) as f:

            return json.load(f)

    except:

        return DEFAULT_SETTINGS


def save_settings(settings):

    with open(
        SETTINGS_FILE,
        "w"
    ) as f:

        json.dump(
            settings,
            f,
            indent=4
        )