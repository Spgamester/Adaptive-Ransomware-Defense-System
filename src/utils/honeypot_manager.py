import os

HONEYPOT_FILES = [
    "salary.xlsx",
    "employees.xlsx",
    "passwords.txt",
    "accounts.db",
    "confidential.docx",
    "backup.zip"
]

def create_honeypot(monitor_path):

    honeypot_path = os.path.join(
        monitor_path,
        "ARDS_Honeypot"
    )

    os.makedirs(
        honeypot_path,
        exist_ok=True
    )

    for file in HONEYPOT_FILES:

        path = os.path.join(
            honeypot_path,
            file
        )

        if not os.path.exists(path):

            with open(path, "w") as f:

                f.write(
                    "ARDS Honeypot File"
                )

    return honeypot_path