import csv
import os

FILE_PATH = "data/measurements.csv"


def save_measurement(measurement):
    os.makedirs("data", exist_ok=True)

    file_exists = os.path.exists(FILE_PATH)

    with open(FILE_PATH, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "timestamp",
                "x",
                "y",
                "zona",
                "ssid",
                "bssid",
                "rssi",
                "channel",
                "band"
            ]
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(measurement)