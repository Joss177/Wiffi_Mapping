import csv
import os
import matplotlib.pyplot as plt


FILE_PATH = "data/measurements.csv"
OUTPUT_PATH = "output/rssi_line.png"


def load_measurements():

    distances = []
    rssi_values = []
    bssids = []

    with open(FILE_PATH, "r", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            distances.append(float(row["x"]))
            rssi_values.append(float(row["rssi"]))
            bssids.append(row["bssid"])

    return distances, rssi_values, bssids


def generate_graph():

    distances, rssi_values, bssids = load_measurements()

    os.makedirs("output", exist_ok=True)

    plt.figure(figsize=(10, 6))

    plt.plot(
        distances,
        rssi_values,
        marker="o"
    )

    for x, y, bssid in zip(distances, rssi_values, bssids):

        plt.annotate(
            bssid[-5:],
            (x, y),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center"
        )

    plt.xlabel("Distancia desde el router (metros)")
    plt.ylabel("RSSI (dBm)")
    plt.title("Señal Wi-Fi - EnvCam_Site")

    plt.xticks(distances)

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_PATH,
        dpi=150
    )

    plt.show()

    print()
    print("Gráfica generada correctamente.")
    print(f"Archivo: {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_graph()