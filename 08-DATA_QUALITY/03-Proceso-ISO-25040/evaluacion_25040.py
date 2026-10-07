#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
03 · Proceso ISO/IEC 25040: una evaluación completa, actividad por actividad.

  python evaluacion_25040.py
  python evaluacion_25040.py --ahora 2026-10-06T10:00

Las cinco actividades:
  1 Establecer los requisitos   2 Especificar   3 Diseñar   4 Ejecutar   5 Concluir
Genera informe_evaluacion.md con el resultado. Solo biblioteca estándar.
"""
import argparse, json, sys
from datetime import datetime
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "comun"))
import dq

ap = argparse.ArgumentParser()
ap.add_argument("--ahora")
a = ap.parse_args()
ahora = dq.parse_ahora(a.ahora)

def actividad(n, titulo):
    print(f"\n{'═' * 78}\n  Actividad {n} · {titulo}\n{'═' * 78}")

informe = ["# Informe de evaluación de calidad del dato", "",
           f"*Generado el {datetime.now():%Y-%m-%d} · referencia temporal de los datos: {ahora:%Y-%m-%d %H:%M}*", ""]

# ── 1 ── Establecer los requisitos de la evaluación
actividad(1, "Establecer los requisitos de la evaluación")
req = json.loads((AQUI / "requisitos.json").read_text(encoding="utf-8"))
print(f"  Propósito   : {req['proposito']}")
print(f"  Interesados : {', '.join(req['interesados'])}")
print(f"  Contexto    : {req['contexto']}   ·   Rigor: {req['rigor']}")
print(f"  Características priorizadas: {', '.join(dq.CARACT_POR_ID[c][1] for c in req['caracteristicas_priorizadas'])}")
informe += ["## 1. Requisitos de la evaluación", f"- **Propósito:** {req['proposito']}",
            f"- **Interesados:** {', '.join(req['interesados'])}",
            f"- **Contexto de uso:** `{req['contexto']}` · **Rigor:** {req['rigor']}",
            "- **Características priorizadas:** " + ", ".join(dq.CARACT_POR_ID[c][1] for c in req['caracteristicas_priorizadas']), ""]

# ── 2 ── Especificar la evaluación: medidas y criterios de decisión
actividad(2, "Especificar la evaluación (medidas y criterios)")
filas = dq.cargar_csv()
medidas = dq.medir_todo(filas, ahora)
seleccion = {k: m for k, m in medidas.items() if m.caracteristica in req["caracteristicas_priorizadas"] and k in req["umbrales"]}
print(f"  {'medida':<18} {'característica':<14} criterio de decisión")
for k, m in seleccion.items():
    print(f"  {k:<18} {dq.CARACT_POR_ID[m.caracteristica][1]:<14} valor ≥ {req['umbrales'][k]:.0%}")
informe += ["## 2. Especificación: medidas y criterios", "| Medida | Característica | Criterio |", "|---|---|---|"]
informe += [f"| `{k}` | {dq.CARACT_POR_ID[m.caracteristica][1]} | ≥ {req['umbrales'][k]:.0%} |" for k, m in seleccion.items()] + [""]

# ── 3 ── Diseñar la evaluación
actividad(3, "Diseñar la evaluación (plan)")
plan = [("Datos evaluados", f"datos/lecturas_calidad_aire.csv ({len(filas)} filas)"),
        ("Herramienta", "comun/dq.py (medidas ISO/IEC 25024 como ratios)"),
        ("Reproducibilidad", "fecha de referencia fija + datos y código versionados")]
for k, v in plan:
    print(f"  {k:<18}: {v}")
informe += ["## 3. Diseño"] + [f"- **{k}:** {v}" for k, v in plan] + [""]

# ── 4 ── Ejecutar la evaluación
actividad(4, "Ejecutar la evaluación")
resultados = []
for k, m in seleccion.items():
    ok = m.valor >= req["umbrales"][k]
    resultados.append((k, m, ok))
    print(f"  {'✅' if ok else '❌'} {k:<18} {m.valor:>7.1%}   (exigido ≥ {req['umbrales'][k]:.0%})   {dq.barra(m.valor, 16)}")
informe += ["## 4. Ejecución", "| Medida | Valor | Exigido | Resultado |", "|---|---|---|---|"]
informe += [f"| `{k}` | {m.valor:.1%} ({m.cumplen}/{m.total}) | ≥ {req['umbrales'][k]:.0%} | {'✅ cumple' if ok else '❌ no cumple'} |"
            for k, m, ok in resultados] + [""]

# ── 5 ── Concluir la evaluación
actividad(5, "Concluir la evaluación")
reglas = dq.cargar_reglas()
fallos, ratio = dq.evaluar_registros(filas, reglas["br_dv"])
nivel, decision, _ = dq.evaluar_contexto(dq.valores_para_reglas(medidas, ratio), reglas["contextos"][req["contexto"]])
incumplen = [k for k, _, ok in resultados if not ok]
print(f"  Medidas que NO cumplen su criterio: {', '.join(incumplen) if incumplen else 'ninguna'}")
print(f"  Nivel de calidad (contexto «{req['contexto']}»): {nivel}")
print(f"  Decisión de uso: {decision}")
informe += ["## 5. Conclusiones",
            f"- **Medidas que no cumplen:** {', '.join('`'+k+'`' for k in incumplen) if incumplen else 'ninguna'}",
            f"- **Nivel de calidad** (contexto `{req['contexto']}`): **{nivel}**",
            f"- **Decisión de uso:** {decision}", "",
            "> Los umbrales son ilustrativos. Una evaluación formal debe documentar por qué se eligieron.", ""]

destino = AQUI / "informe_evaluacion.md"
destino.write_text("\n".join(informe), encoding="utf-8")
print(f"\n📝 Informe escrito en {destino.name}")
