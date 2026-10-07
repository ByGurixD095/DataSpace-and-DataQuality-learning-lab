#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
05 · Reglas de negocio en cuatro niveles (estilo DMN4DQ).

  python motor_reglas.py
  python motor_reglas.py --ahora 2026-10-06T10:00     # ¡el contexto de alertas cambia de decisión!
  python motor_reglas.py --registros                   # lista los registros que fallan alguna regla

BR.DV  valores   → ¿es válido cada registro?        (reglas.json › br_dv)
BR.DQM medición  → ¿cuánta calidad tiene?           (medidas de comun/dq.py)
BR.DQA evaluación→ ¿qué nivel de calidad es?        (reglas.json › contextos › br_dqa)
BR.DUD decisión  → ¿es utilizable?                  (reglas.json › contextos › br_dud)

⚠️ No es un motor DMN real: es un evaluador de tablas de decisión (política «first hit») para
   entender la idea. Para producción, usa un motor DMN y la notación estándar de OMG.
"""
import argparse, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "comun"))
import dq

ap = argparse.ArgumentParser()
ap.add_argument("--ahora")
ap.add_argument("--registros", action="store_true")
a = ap.parse_args()

filas = dq.cargar_csv()
reglas = dq.cargar_reglas(AQUI / "reglas.json")
ahora = dq.parse_ahora(a.ahora)

print("\n━━ BR.DV · reglas sobre los valores ━━")
for r in reglas["br_dv"]:
    print(f"  {r['id']}  {r['descripcion']}")
fallos, ratio = dq.evaluar_registros(filas, reglas["br_dv"])
cuenta = {r["id"]: sum(1 for f in fallos if r["id"] in f) for r in reglas["br_dv"]}
print("  Registros que incumplen →", ", ".join(f"{k}: {v}" for k, v in cuenta.items()))
if a.registros:
    for i, f in enumerate(fallos):
        if f:
            fila = filas[i]
            print(f"   fila {i + 2:>3}  {fila['estacion']} {fila['fecha_hora']}  no2={fila['no2'] or '∅':<7} pm10={fila['pm10']:<5} pm25={fila['pm25']:<5} ✗ {', '.join(f)}")

print("\n━━ BR.DQM · medición ━━")
medidas = dq.medir_todo(filas, ahora)
valores = dq.valores_para_reglas(medidas, ratio)
for r in reglas["br_dqm"]:
    print(f"  {r['id']:<18} = {valores[r['id']]:.1%}   {r['descripcion']}")

print(f"\n━━ BR.DQA + BR.DUD · el mismo dato, tres contextos (ahora = {ahora:%Y-%m-%d %H:%M}) ━━")
for nombre, ctx in reglas["contextos"].items():
    nivel, decision, fila_regla = dq.evaluar_contexto(valores, ctx)
    cond = " y ".join(f"{m} {e}" for m, e in fila_regla["si"].items()) or "(en cualquier otro caso)"
    print(f"\n  📌 {nombre}: {ctx['descripcion']}")
    print(f"     nivel   : {nivel}   ← regla aplicada: {cond}")
    print(f"     decisión: {decision}")

print("\n💡 Mismos datos, decisiones distintas: la calidad depende del contexto de uso.")
