#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02 · Medidas ISO/IEC 25024: cada medida es un ratio cumplen / total.

  python medir.py
  python medir.py --csv otro.csv --ahora 2026-10-06T10:00
  python medir.py --json

Solo usa la biblioteca estándar.
"""
import argparse, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "comun"))
import dq

ap = argparse.ArgumentParser(description="Calcula las medidas de calidad de un CSV de lecturas")
ap.add_argument("--csv", default=str(dq.CSV_POR_DEFECTO))
ap.add_argument("--ahora", help="fecha de referencia ISO (por defecto, una fija para reproducibilidad)")
ap.add_argument("--json", action="store_true", help="salida en JSON")
a = ap.parse_args()

filas = dq.cargar_csv(a.csv)
ahora = dq.parse_ahora(a.ahora)
medidas = dq.medir_todo(filas, ahora)

if a.json:
    print(json.dumps({m.id: {"caracteristica": m.caracteristica, "cumplen": m.cumplen, "total": m.total,
                             "valor": m.valor} for m in medidas.values()}, indent=2, ensure_ascii=False))
    sys.exit(0)

print(f"\n📊 {len(filas)} filas · referencia temporal: {ahora:%Y-%m-%d %H:%M}\n")
print(f"  {'medida':<18} {'característica 25012':<15} {'cumplen/total':>13}  {'valor':>7}  gráfico")
print("  " + "─" * 80)
for m in medidas.values():
    nombre = dq.CARACT_POR_ID[m.caracteristica][1]
    print(f"  {m.id:<18} {nombre:<15} {m.cumplen:>6}/{m.total:<6}  {m.valor:>6.1%}  {dq.barra(m.valor)}")
print("\n📌 La norma NO dice qué valor es «suficiente»: eso es un criterio de decisión (ver carpeta 05).")
print("   Qué mide cada una:")
for m in medidas.values():
    print(f"   · {m.id}: {m.descripcion}")
