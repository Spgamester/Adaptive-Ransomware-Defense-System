import os
import shutil

def quarantine_file(file_path):
    try:
        if not os.path.exists("quarantine"):
            os.makedirs("quarantine")

        filename = os.path.basename(file_path)
        destination = os.path.join("quarantine", filename)

        shutil.move(file_path, destination)

        return f"Moved to quarantine: {destination}"

    except Exception as e:
        return f"Quarantine failed: {e}"