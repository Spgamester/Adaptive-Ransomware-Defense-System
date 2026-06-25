import os


def delete_quarantined_file(filename):

    try:

        quarantine_folder = os.path.join(
            os.getcwd(),
            "quarantine"
        )

        file_path = os.path.join(
            quarantine_folder,
            filename
        )

        if not os.path.exists(file_path):

            return (
                False,
                "File not found."
            )

        os.remove(file_path)

        return (
            True,
            f"Deleted: {filename}"
        )

    except Exception as e:

        return (
            False,
            str(e)
        )