#!/usr/bin/env python3
"""Genera lecturas_calidad_aire.csv: datos SINTÉTICOS y reproducibles, con defectos conocidos.

Defectos introducidos a propósito (para que cada medida tenga algo que detectar):
  · 3 lecturas de NO2 vacías                         → completitud
  · 2 lecturas de NO2 fuera de rango (-5, 5000)      → validez / exactitud sintáctica
  · 2 filas con PM2,5 > PM10 (físicamente imposible) → consistencia
  · 2 filas duplicadas (misma estación y hora)       → unicidad
  · 3 valores de NO2 sin decimales                   → precisión
"""
import csv
from pathlib import Path

ESTACIONES = ["E01", "E02"]
filas = []
for e_idx, est in enumerate(ESTACIONES):
    for h in range(24):
        no2 = round(28 + 10 * ((h * 7 + e_idx * 5) % 9) / 3 + (6 if 7 <= h <= 9 or 18 <= h <= 20 else 0), 1)
        pm10 = round(18 + ((h * 5 + e_idx * 3) % 11), 1)
        pm25 = round(pm10 * 0.55, 1)
        filas.append({"estacion": est, "fecha_hora": f"2026-10-05T{h:02d}:00:00",
                      "no2": f"{no2:.1f}", "pm10": f"{pm10:.1f}", "pm25": f"{pm25:.1f}"})

def fila(est, h):
    return next(f for f in filas if f["estacion"] == est and f["fecha_hora"].endswith(f"T{h:02d}:00:00"))

for est, h in [("E01", 5), ("E01", 17), ("E02", 6)]:        # NO2 vacío
    fila(est, h)["no2"] = ""
fila("E01", 10)["no2"] = "-5.0"                              # fuera de rango
fila("E02", 15)["no2"] = "5000.0"
f = fila("E01", 11); f["pm10"], f["pm25"] = "22.0", "23.5"   # PM2,5 > PM10
f = fila("E02", 20); f["pm10"], f["pm25"] = "18.0", "19.2"
for est, h in [("E01", 2), ("E02", 12), ("E02", 22)]:        # sin decimales
    fila(est, h)["no2"] = str(int(float(fila(est, h)["no2"])))
filas.append(dict(fila("E02", 9)))                           # duplicados
filas.append(dict(fila("E01", 14)))

destino = Path(__file__).resolve().parent / "lecturas_calidad_aire.csv"
with open(destino, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["estacion", "fecha_hora", "no2", "pm10", "pm25"], lineterminator="\n")
    w.writeheader(); w.writerows(filas)
print(f"Escritas {len(filas)} filas en {destino}")
