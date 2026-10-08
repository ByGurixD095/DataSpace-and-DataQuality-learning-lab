#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02 · Políticas y clasificación: una política ODRL por nivel de clasificación + un evaluador mínimo.

  python politicas.py                                                    # matriz completa
  python politicas.py --dataset trafico-horario --accion distribute --solicitante externo

Escribe politicas_por_clasificacion.ttl y esquema_clasificacion.ttl.
Recuerda: ODRL DESCRIBE las reglas; el evaluador de aquí es solo una demostración de cómo un motor las aplicaría.

Requiere: rdflib   (pip install rdflib)
"""
import argparse, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "comun"))
import gov

ap = argparse.ArgumentParser()
ap.add_argument("--dataset"); ap.add_argument("--accion", default="use", choices=["use", "distribute"])
ap.add_argument("--solicitante", default="externo", choices=["interno", "externo"])
a = ap.parse_args()

pol = gov.politicas_rdf()
pol.serialize(destination=str(AQUI / "politicas_por_clasificacion.ttl"), format="turtle")
gov.vocabulario_rdf().serialize(destination=str(AQUI / "esquema_clasificacion.ttl"), format="turtle")

if a.dataset:
    fila = next((f for f in gov.cargar_inventario() if f["id"] == a.dataset), None)
    if not fila:
        sys.exit(f"No existe el dataset «{a.dataset}» en el inventario.")
    nivel = gov.CLASIF_POR_NOMBRE.get(fila["clasificacion"])
    ok, motivo, deberes = gov.evaluar(pol, nivel, a.accion, a.solicitante)
    print(f"\n📦 {fila['titulo']}  ·  clasificación: {fila['clasificacion'] or '(sin clasificar)'}")
    print(f"🙋 Solicitante {a.solicitante} quiere «{a.accion}»  →  {'✅ PERMITIDO' if ok else '❌ DENEGADO'}")
    print(f"   motivo: {motivo}" + (f"\n   obligaciones: {', '.join(deberes)}" if deberes else ""))
    sys.exit(0)

print("\n🛡️  Matriz de decisión: la clasificación decide, la política lo aplica\n")
print(f"  {'nivel':<18}{'solicitante':<13}{'use':<22}{'distribute'}")
print("  " + "─" * 66)
for cid, nombre, _ in gov.CLASIFICACION + [(None, "(sin clasificar)", "")]:
    for sol in ("interno", "externo"):
        celdas = []
        for acc in ("use", "distribute"):
            ok, _, deberes = gov.evaluar(pol, cid, acc, sol)
            celdas.append(("✅" + (f" +{'/'.join(deberes)}" if deberes else "")) if ok else "❌")
        print(f"  {nombre if sol == 'interno' else '':<18}{sol:<13}{celdas[0]:<22}{celdas[1]}")
print("\n💡 Fíjate en la última fila: lo SIN CLASIFICAR queda denegado por defecto.")
print("   Una política de gobierno razonable es «si no sabes qué es, no lo compartas».")
print("\n📄 Escritos: politicas_por_clasificacion.ttl y esquema_clasificacion.ttl")
