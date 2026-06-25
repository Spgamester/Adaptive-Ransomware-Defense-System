import math
import time


def calculate_entropy(file_path):

    for _ in range(5):

        try:

            with open(file_path, "rb") as f:
                data = f.read()

            if not data:
                return 0

            entropy = 0

            for x in range(256):

                p_x = data.count(
                    bytes([x])
                ) / len(data)

                if p_x > 0:
                    entropy -= (
                        p_x * math.log2(p_x)
                    )

            return entropy

        except PermissionError:

            time.sleep(0.2)

        except Exception as e:

            print(
                "Entropy error:",
                e
            )

            return 0

    return 0