import datetime

detected_threats = []
alert_feed = []

def alert(message, file_path=None):

    alert_message = f"{message}"

    if file_path:
        alert_message += f" | Location: {file_path}"

    print("\n⚠ RANSOMWARE ALERT:", alert_message)

    detected_threats.append(alert_message)

    alert_feed.append(
        f"CRITICAL: {alert_message}"
    )


    with open("logs/detection_log.txt","a") as f:
        f.write(str(datetime.datetime.now()) + " : " + alert_message + "\n")