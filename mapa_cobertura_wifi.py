import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# MAPA ESQUEMÁTICO DE COBERTURA WI-FI
# Red: EnvCam_Site
# ============================================================

# ------------------------------------------------------------
# 1. POSICIONES APROXIMADAS DE LOS PUNTOS PRINCIPALES
# ------------------------------------------------------------
# Coordenadas en metros.
# El eje X representa el recorrido principal.
# El eje Y se utiliza para separar visualmente las áreas.

decos = {
    "Deco 1": (0, 0),
    "Deco 2": (42, 0),
    "Deco 3": (54, 9)
}

# ------------------------------------------------------------
# 2. PUNTOS DEL RECORRIDO PRINCIPAL
#    Deco 1 -> Envasado -> Escaleras -> Deco 2 -> Oficinas
# ------------------------------------------------------------

ruta_principal = [
    (0.0, 0, "Deco 1"),
    (2.5, 0, ""),
    (5.0, 0, ""),
    (7.5, 0, ""),
    (10.0, 0, ""),
    (13.13, 0, "Entrada envasado"),
    (15.5, 0, ""),
    (18.0, 0, ""),
    (20.5, 0, ""),
    (23.0, 0, ""),
    (25.09, 0, "Salida envasado"),
    (27.5, 0, ""),
    (30.0, 0, ""),
    (32.5, 0, ""),
    (35.0, 0, ""),
    (37.2, 0, "Inicio escaleras"),
    (39.5, 0, "Escaleras"),
    (42.0, 0, "Roaming → Deco 2"),
    (44.5, 0, ""),
    (47.0, 0, "Entrada laboratorio"),
    (49.71, 0, "Laboratorio"),
    (52.0, 0, ""),
    (54.0, 0, "Segundas escaleras"),
    (56.0, 0, "Subida oficinas"),
    (58.79, 0, "Oficinas")
]

# ------------------------------------------------------------
# 3. RSSI DE LA PRUEBA PRINCIPAL
# ------------------------------------------------------------

distancias = [
    0.0, 2.5, 5.0, 7.5, 10.0,
    13.13, 15.5, 18.0, 20.5, 23.0,
    25.09, 27.5, 30.0, 32.5, 35.0,
    37.2, 39.5, 42.0, 44.5, 47.0,
    49.71, 52.0, 54.0, 56.0, 58.79
]

rssi = [
    -32.0, -32.0, -32.0, -32.0, -32.0,
    -32.0, -32.0, -32.0, -32.0, -37.8,
    -67.0, -69.6, -60.2, -60.0, -60.0,
    -60.0, -60.0, -60.4, -52.8, -50.0,
    -50.0, -50.0, -50.0, -50.0, -50.0
]

# ------------------------------------------------------------
# 4. CREAR FIGURA
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(16, 9))

# ------------------------------------------------------------
# 5. DIBUJAR RECORRIDO PRINCIPAL
# ------------------------------------------------------------

x = [p[0] for p in ruta_principal]
y = [p[1] for p in ruta_principal]

ax.plot(
    x,
    y,
    linewidth=3,
    marker="o",
    markersize=5,
    label="Recorrido principal"
)

# ------------------------------------------------------------
# 6. COLOREAR PUNTOS SEGÚN RSSI
# ------------------------------------------------------------

for i in range(len(x)):
    if rssi[i] >= -50:
        color = "green"
    elif rssi[i] >= -60:
        color = "orange"
    else:
        color = "red"

    ax.scatter(
        x[i],
        y[i],
        color=color,
        s=70,
        zorder=5
    )

# ------------------------------------------------------------
# 7. DIBUJAR LOS DECO
# ------------------------------------------------------------

for nombre, (dx, dy) in decos.items():

    ax.scatter(
        dx,
        dy,
        marker="s",
        s=350,
        color="blue",
        edgecolor="black",
        linewidth=2,
        zorder=10
    )

    ax.text(
        dx,
        dy + 1.5,
        nombre,
        ha="center",
        fontsize=12,
        fontweight="bold"
    )

# ------------------------------------------------------------
# 8. ETIQUETAS DE ZONAS
# ------------------------------------------------------------

zonas = [
    (6, -2.0, "Antiguo taller"),
    (18, -2.0, "Envasado"),
    (31, -2.0, "Corredor"),
    (39, -2.0, "Escaleras"),
    (49, -2.0, "Laboratorio"),
    (58, 1.8, "Oficinas")
]

for zx, zy, texto in zonas:
    ax.text(
        zx,
        zy,
        texto,
        ha="center",
        fontsize=11
    )

# ------------------------------------------------------------
# 9. MARCAR PUNTO DE ROAMING
# ------------------------------------------------------------

ax.axvline(
    x=42,
    linestyle="--",
    linewidth=2
)

ax.text(
    42,
    3,
    "Roaming observado\nDeco 1 → Deco 2\n≈ 42 m",
    ha="center",
    fontsize=11,
    fontweight="bold"
)

# ------------------------------------------------------------
# 10. LEYENDA DE RSSI
# ------------------------------------------------------------

ax.scatter([], [], color="green", s=80, label="RSSI ≥ -50 dBm")
ax.scatter([], [], color="orange", s=80, label="-60 a -50 dBm")
ax.scatter([], [], color="red", s=80, label="RSSI < -60 dBm")

# ------------------------------------------------------------
# 11. CONFIGURACIÓN DEL MAPA
# ------------------------------------------------------------

ax.set_title(
    "Mapa esquemático del recorrido y cobertura Wi-Fi",
    fontsize=18,
    fontweight="bold"
)

ax.set_xlabel(
    "Distancia recorrida desde el punto inicial (m)",
    fontsize=12
)

ax.set_ylabel(
    "Distribución esquemática de las zonas",
    fontsize=12
)

ax.grid(True, linestyle="--", alpha=0.3)

ax.set_xlim(-5, 65)
ax.set_ylim(-5, 12)

ax.legend(
    loc="upper left",
    fontsize=10
)

# ------------------------------------------------------------
# 12. GUARDAR IMAGEN
# ------------------------------------------------------------

plt.tight_layout()

plt.savefig(
    "mapa_cobertura_wifi.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("Mapa generado correctamente:")
print("mapa_cobertura_wifi.png")