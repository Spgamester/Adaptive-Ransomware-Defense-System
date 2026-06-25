import json
import os

SETTINGS_FILE = "settings.json"


DEFAULT_SETTINGS ={
    "auto_scan": True,
    "real_time": True,
    "heuristic": True,
    "entropy": True,
    "auto_quarantine": True,
    "threat_alerts": True,
    "launch_startup": False
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