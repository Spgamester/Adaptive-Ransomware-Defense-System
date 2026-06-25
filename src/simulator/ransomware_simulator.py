import os
import time

folder = "test_folder"

for i in range(100):

    file_path = f"{folder}/file{i}.txt"

    with open(file_path, "w") as f:
        f.write("encrypted_data")

    print("Encrypting:", file_path)

    time.sleep(0.05)