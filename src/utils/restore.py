import os
import shutil


def restore_file(filename):

    try:

        quarantine_folder = os.path.join(
            os.getcwd(),
            "quarantine"
        )

        restore_folder = os.path.join(
            os.getcwd(),
            "restored_files"
        )

        if not os.path.exists(restore_folder):
            os.makedirs(restore_folder)

        source = os.path.join(
            quarantine_folder,
            filename
        )

        destination = os.path.join(
            restore_folder,
            filename
        )

        shutil.move(
            source,
            destination
        )

        return (
            True,
            f"Restored: {destination}"
        )

    except Exception as e:

        return (
            False,
            str(e)
        )