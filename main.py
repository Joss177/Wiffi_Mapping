from wifi_scanner import get_connected_wifi
from signal_logger import measure_point
from measurements import save_measurement


def get_plant_points():

    return [

        # ANTIGUO TALLER DE MONTACARGAS

        (0.00, 0, "Deco principal - Antiguo taller de montacargas"),
        (2.50, 0, "Antiguo taller de montacargas"),
        (5.00, 0, "Antiguo taller de montacargas"),
        (7.50, 0, "Antiguo taller de montacargas"),
        (10.00, 0, "Antiguo taller de montacargas"),

        # ENTRADA A ENVASADO

        (13.13, 0, "Entrada a envasado"),

        # ENVASADO

        (15.50, 0, "Interior de envasado"),
        (18.00, 0, "Interior de envasado"),
        (20.50, 0, "Interior de envasado"),
        (23.00, 0, "Interior de envasado"),
        (25.09, 0, "Salida de envasado"),

        # CAMINO HACIA ESCALERAS

        (27.50, 0, "Corredor hacia escaleras"),
        (30.00, 0, "Corredor hacia escaleras"),
        (32.50, 0, "Corredor hacia escaleras"),
        (35.00, 0, "Corredor hacia escaleras"),

        # ESCALERAS

        (37.20, 0, "Inicio de escaleras"),
        (39.50, 0, "Escaleras"),
        (42.00, 0, "Escaleras"),

        # PLANTA DE RECUPERACIÓN DE AGUA

        (44.50, 0, "Planta de recuperación de agua"),
        (47.00, 0, "Entrada al laboratorio"),

        # DECO 2

        (49.71, 0, "Laboratorio - Deco 2"),

        # SALIDA DEL LABORATORIO

        (52.00, 0, "Salida del laboratorio"),
        (54.00, 0, "Segundas escaleras"),
        (56.00, 0, "Subiendo hacia oficinas"),

        # DECO 3

        (58.79, 0, "Oficinas - Deco 3")
    ]


def get_office_points():

    # Oficina:
    # Largo: 6.32 m
    # Ancho: 4.81 m
    #
    # Coordenadas:
    # X = 0.00 -> 6.32
    # Y = 0.00 -> 4.81
    #
    # Deco aproximadamente en:
    # X = 3.16
    # Y = 2.405
    # Z = 0.80 m
    #
    # Por ahora utilizamos una cuadrícula de 9 puntos.
    # Posteriormente podremos hacerla más densa.

    return [

        # Fila 1

        (0.80, 0.80, "Oficina - punto 1"),
        (3.16, 0.80, "Oficina - punto 2"),
        (5.50, 0.80, "Oficina - punto 3"),

        # Fila 2

        (0.80, 2.405, "Oficina - punto 4"),
        (3.16, 2.405, "Oficina - Deco"),
        (5.50, 2.405, "Oficina - punto 6"),

        # Fila 3

        (0.80, 4.00, "Oficina - punto 7"),
        (3.16, 4.00, "Oficina - punto 8"),
        (5.50, 4.00, "Oficina - punto 9")
    ]


def show_points(points):

    print()
    print("PUNTOS DEL RECORRIDO")
    print("------------------------------------")

    for number, point in enumerate(points, start=1):

        x = point[0]
        y = point[1]
        zona = point[2]

        print(
            f"{number:02d}. "
            f"X: {x:05.2f} m | "
            f"Y: {y:05.2f} m | "
            f"{zona}"
        )

    print()


def run_measurement(target_ssid, points):

    print()
    print("====================================")
    print("       INICIO DEL RECORRIDO")
    print("====================================")
    print()

    print(f"Se medirán {len(points)} puntos.")
    print()

    show_points(points)

    input("Presiona ENTER para comenzar...")

    total_points = 0

    for number, point in enumerate(points, start=1):

        x = point[0]
        y = point[1]
        zona = point[2]

        print()
        print("====================================")
        print(f"          PUNTO {number} DE {len(points)}")
        print("====================================")
        print()

        print(f"X: {x:.2f} m")
        print(f"Y: {y:.2f} m")
        print(f"Zona: {zona}")
        print()

        input(
            "Colócate en esta zona y presiona ENTER..."
        )

        measurement = measure_point(
            target_ssid=target_ssid,
            x=x,
            y=y,
            zona=zona,
            duration=10,
            interval=2
        )

        if measurement:

            save_measurement(measurement)

            total_points += 1

            print()
            print("Punto guardado correctamente.")

        else:

            print()
            print("El punto no pudo ser guardado.")

    print()
    print("====================================")
    print("        RECORRIDO TERMINADO")
    print("====================================")
    print()

    print(f"Puntos guardados: {total_points}")
    print(f"Puntos esperados: {len(points)}")
    print()
    print("Archivo:")
    print("data/measurements.csv")
    print()


def main():

    print("====================================")
    print("          WIFI MAPPING")
    print("====================================")
    print()

    wifi = get_connected_wifi()

    if not wifi:

        print(
            "No se pudo obtener información "
            "de la conexión Wi-Fi."
        )

        return

    print("CONEXIÓN ACTUAL")
    print("------------------------------------")
    print(f"SSID:   {wifi.get('ssid')}")
    print(f"BSSID:  {wifi.get('bssid')}")
    print(f"RSSI:   {wifi.get('rssi')} dBm")
    print(f"Canal:  {wifi.get('channel')}")
    print(f"Banda:  {wifi.get('band')}")
    print()

    target_ssid = input(
        "Escribe el SSID que quieres mapear: "
    ).strip()

    if target_ssid != wifi.get("ssid"):

        print()
        print("ERROR:")
        print("Debes estar conectado al SSID que quieres medir.")

        return

    print()
    print("====================================")
    print("             MODO")
    print("====================================")
    print()
    print("1. Recorrido completo de la planta")
    print("2. Calibración de oficina")
    print()

    option = input(
        "Selecciona una opción: "
    ).strip()

    if option == "1":

        points = get_plant_points()

        print()
        print("Modo seleccionado:")
        print("RECORRIDO COMPLETO")
        print()
        print("Distancia total: 58.79 metros")

        run_measurement(
            target_ssid=target_ssid,
            points=points
        )

    elif option == "2":

        points = get_office_points()

        print()
        print("Modo seleccionado:")
        print("CALIBRACIÓN DE OFICINA")
        print()
        print("Dimensiones:")
        print("Largo:  6.32 m")
        print("Ancho:  4.81 m")
        print("Altura: 2.15 m")
        print()
        print("Deco:")
        print("X: 3.16 m")
        print("Y: 2.405 m")
        print("Z: 0.80 m")
        print()

        run_measurement(
            target_ssid=target_ssid,
            points=points
        )

    else:

        print()
        print("Opción no válida.")


if __name__ == "__main__":
    main()