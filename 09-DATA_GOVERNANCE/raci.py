#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01 · Roles y RACI: una matriz RACI es un conjunto de reglas que se pueden comprobar.

  python raci.py                              # valida matriz_raci.csv
  python raci.py matriz_raci_con_errores.csv  # ¡mira qué detecta!

Reglas:
  · Cada actividad tiene UNA SOLA «A» (quien responde y decide). Con dos, nadie decide; con ninguna, nadie responde.
  · Cada actividad tiene AL MENOS una «R» (alguien que lo realiza).
En una celda pueden aparecer varias letras (p. ej. «A/R»: quien decide también ejecuta).

Solo biblioteca estándar. Sale con código 1 si hay errores.
"""
import csv, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ruta = Path(sys.argv[1]) if len(sys.argv) > 1 else AQUI / "matriz_raci.csv"
if not ruta.is_absolute() and not ruta.exists():
    ruta = AQUI / ruta
with open(ruta, newline="", encoding="utf-8") as f:
    filas = list(csv.DictReader(f))
roles = [c for c in filas[0] if c != "actividad"]
CORTO = {"propietario": "propiet.", "steward": "steward", "custodio": "custodio",
         "oficina_del_dato": "oficina", "comite": "comité", "juridico_dpd": "jur./DPD"}

def letras(celda: str) -> set:
    return {x for x in (celda or "").upper().replace(" ", "").split("/") if x}

print(f"\n📋 {ruta.name}\n")
print(f"  {'actividad':<44}" + "".join(f"{CORTO.get(r, r[:9]):>11}" for r in roles) + "   resultado")
print("  " + "─" * (44 + 11 * len(roles) + 14))
errores = 0
carga = {r: {"A": 0, "R": 0} for r in roles}
for f in filas:
    celdas = {r: letras(f[r]) for r in roles}
    n_a = sum("A" in c for c in celdas.values())
    n_r = sum("R" in c for c in celdas.values())
    problemas = []
    if n_a == 0: problemas.append("sin «A»: nadie responde")
    if n_a > 1:  problemas.append(f"{n_a} «A»: nadie decide")
    if n_r == 0: problemas.append("sin «R»: nadie lo realiza")
    errores += len(problemas)
    for r in roles:
        carga[r]["A"] += "A" in celdas[r]; carga[r]["R"] += "R" in celdas[r]
    celdas_txt = "".join(f"{(f[r] or '·'):>11}" for r in roles)
    print(f"  {f['actividad'][:43]:<44}{celdas_txt}   {'✅' if not problemas else '❌ ' + '; '.join(problemas)}")

print("\n⚖️  Carga por rol (cuántas actividades decide «A» y cuántas realiza «R»):")
for r in roles:
    print(f"   {r:<18} A={carga[r]['A']}  R={carga[r]['R']}  {'█' * (carga[r]['A'] + carga[r]['R'])}")
mas = max(roles, key=lambda r: carga[r]["A"] + carga[r]["R"])
print(f"\n💡 El rol más cargado es «{mas}»: un rol sobrecargado es un cuello de botella (o un riesgo si falta).")
print(f"{'✅ La matriz cumple las reglas.' if not errores else f'❌ {errores} problema(s) en la matriz.'}")
sys.exit(1 if errores else 0)
