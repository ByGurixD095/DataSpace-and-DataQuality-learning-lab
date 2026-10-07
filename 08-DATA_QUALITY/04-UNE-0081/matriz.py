#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
04 · Matriz de evaluación (plantilla inspirada en el proceso de UNE 0081 / ISO 25040).

  python matriz.py

Lee matriz_evaluacion.csv (característica → métrica → umbral), ejecuta las medidas que se pueden
automatizar y deja marcadas las que requieren inspección. Termina con la COBERTURA de la evaluación.

⚠️ No reproduce el contenido de la especificación UNE 0081: es una plantilla de trabajo.
   Consulta la norma para el modelo y las métricas oficiales.
"""
import argparse, csv, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "comun"))
import dq

ap = argparse.ArgumentParser()
ap.add_argument("--ahora")
a = ap.parse_args()

medidas = dq.medir_todo(dq.cargar_csv(), dq.parse_ahora(a.ahora))
with open(AQUI / "matriz_evaluacion.csv", newline="", encoding="utf-8") as f:
    filas = list(csv.DictReader(f))

print(f"\n  {'característica':<18} {'prio':<6} {'métrica':<48} {'resultado'}")
print("  " + "─" * 100)
evaluadas = cumplen = 0
caract_cubiertas, caract_total = set(), set()
for r in filas:
    nombre = dq.CARACT_POR_ID[r["caracteristica"]][1]
    caract_total.add(r["caracteristica"])
    if r["medida_id"]:
        m = medidas[r["medida_id"]]
        ok = m.valor >= float(r["umbral"])
        evaluadas += 1; cumplen += ok; caract_cubiertas.add(r["caracteristica"])
        res = f"{'✅' if ok else '❌'} {m.valor:.1%} (≥ {float(r['umbral']):.0%})"
    else:
        res = f"🔎 pendiente: {r['como_se_obtiene']}"
    print(f"  {nombre:<18} {r['prioridad']:<6} {r['metrica'][:46]:<48} {res}")

print(f"\n  📊 Métricas evaluadas automáticamente: {evaluadas}/{len(filas)}  ·  cumplen: {cumplen}/{evaluadas}")
print(f"  🎯 Características priorizadas con al menos una medida: {len(caract_cubiertas)}/{len(caract_total)}")
print("\n  💡 Una evaluación honesta informa de lo que NO se ha podido medir:")
print("     un «todo OK» sobre el 50 % de las características no es un «todo OK».")
