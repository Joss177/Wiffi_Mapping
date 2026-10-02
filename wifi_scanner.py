import subprocess
import re


def get_wifi_interface():
    """
    Obtiene información de la interfaz Wi-Fi actualmente conectada.
    """

    result = subprocess.run(
        ["netsh", "wlan", "show", "interfaces"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )

    return result.stdout


def get_connected_wifi():
    """
    Obtiene información de la red Wi-Fi a la que está conectada
    actualmente la computadora.
    """

    output = get_wifi_interface()

    data = {
        "ssid": None,
        "bssid": None,
        "signal": None,
        "rssi": None,
        "channel": None,
        "band": None,
        "radio": None
    }

    patterns = {
        "ssid": r"^\s*SSID\s*:\s*(.+)$",
        "bssid": r"^\s*AP BSSID\s*:\s*(.+)$",
        "signal": r"^\s*Señal\s*:\s*(\d+)%$",
        "rssi": r"^\s*Rssi\s*:\s*(-?\d+)$",
        "channel": r"^\s*Canal\s*:\s*(\d+)$",
        "band": r"^\s*Banda\s*:\s*(.+)$",
        "radio": r"^\s*Tipo de radio\s*:\s*(.+)$"
    }

    for line in output.splitlines():

        for key, pattern in patterns.items():

            match = re.search(pattern, line, re.IGNORECASE)

            if match:
                data[key] = match.group(1).strip()

    return data


def scan_wifi():
    """
    Obtiene todas las redes Wi-Fi visibles.
    """

    result = subprocess.run(
        ["netsh", "wlan", "show", "networks", "mode=bssid"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )

    output = result.stdout

    networks = []

    current_ssid = None
    current_bssid = None
    current_signal = None
    current_channel = None
    current_band = None
    current_radio = None

    for line in output.splitlines():

        line = line.strip()

        # SSID
        match = re.match(
            r"SSID\s+\d+\s*:\s*(.*)",
            line,
            re.IGNORECASE
        )

        if match:

            current_ssid = match.group(1).strip()

            # Reiniciamos los datos del BSSID
            current_bssid = None
            current_signal = None
            current_channel = None
            current_band = None
            current_radio = None

            continue

        # BSSID
        match = re.match(
            r"BSSID\s+\d+\s*:\s*(.*)",
            line,
            re.IGNORECASE
        )

        if match:

            # Si ya teníamos un BSSID anterior,
            # guardamos esa red.
            if current_bssid:

                networks.append({
                    "ssid": current_ssid,
                    "bssid": current_bssid,
                    "signal": current_signal,
                    "channel": current_channel,
                    "band": current_band,
                    "radio": current_radio
                })

            current_bssid = match.group(1).strip()

            current_signal = None
            current_channel = None
            current_band = None
            current_radio = None

            continue

        # Signal
        match = re.match(
            r"Señal\s*:\s*(\d+)%",
            line,
            re.IGNORECASE
        )

        if match:

            current_signal = int(match.group(1))

            continue

        # Channel
        match = re.match(
            r"Canal\s*:\s*(\d+)",
            line,
            re.IGNORECASE
        )

        if match:

            current_channel = int(match.group(1))

            continue

        # Band
        match = re.match(
            r"Banda\s*:\s*(.+)",
            line,
            re.IGNORECASE
        )

        if match:

            current_band = match.group(1).strip()

            continue

        # Radio
        match = re.match(
            r"Tipo de radio\s*:\s*(.+)",
            line,
            re.IGNORECASE
        )

        if match:

            current_radio = match.group(1).strip()

            continue

    # Guardar último BSSID
    if current_bssid:

        networks.append({
            "ssid": current_ssid,
            "bssid": current_bssid,
            "signal": current_signal,
            "channel": current_channel,
            "band": current_band,
            "radio": current_radio
        })

    return networks


def find_network(target_ssid):
    """
    Busca todas las apariciones de un SSID específico.
    """

    networks = scan_wifi()

    matches = []

    for network in networks:

        if network["ssid"] == target_ssid:

            matches.append(network)

    return matches