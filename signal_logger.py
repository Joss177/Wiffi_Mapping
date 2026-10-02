import time
from datetime import datetime

from wifi_scanner import get_connected_wifi


def measure_point(target_ssid, x, y, zona, duration=10, interval=2):

    print()
    print(f"Zona: {zona}")
    print(f"Coordenadas: ({x}, {y})")
    print()

    readings = []
    last_connected = None

    start_time = time.time()

    while time.time() - start_time < duration:

        connected = get_connected_wifi()

        if connected and connected.get("ssid") == target_ssid:

            rssi = connected.get("rssi")

            if rssi is not None:

                readings.append(int(rssi))
                last_connected = connected

                print(
                    f"RSSI: {rssi} dBm | "
                    f"Canal: {connected.get('channel')} | "
                    f"Banda: {connected.get('band')} | "
                    f"BSSID: {connected.get('bssid')}"
                )

        else:

            print(
                f"ERROR: No estás conectado a {target_ssid}"
            )

        time.sleep(interval)

    if not readings:

        print()
        print("No se obtuvieron mediciones.")
        return None

    average_rssi = round(
        sum(readings) / len(readings),
        2
    )

    measurement = {
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "x": x,
        "y": y,
        "zona": zona,
        "ssid": last_connected.get("ssid"),
        "bssid": last_connected.get("bssid"),
        "rssi": average_rssi,
        "channel": last_connected.get("channel"),
        "band": last_connected.get("band")
    }

    print()
    print(f"RSSI promedio: {average_rssi} dBm")
    print(f"BSSID: {last_connected.get('bssid')}")

    return measurement