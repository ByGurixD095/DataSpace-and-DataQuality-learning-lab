#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
03 · Oferta y acuerdo: una odrl:Offer es una PROPUESTA; un odrl:Agreement es un CONTRATO con partes.

  python oferta_acuerdo.py                                   # 5 peticiones de ejemplo
  python oferta_acuerdo.py --dataset calidad-aire --finalidad investigacion --consumidor universidad

Genera ofertas.ttl (catálogo con ofertas) y acuerdos.ttl (los acuerdos de las peticiones aceptadas)
y un registro de usos (el deber «inform» de las ofertas).
ODRL describe las reglas; el evaluador de aquí es solo una demostración de cómo un motor las aplicaría.

Requiere: rdflib
"""
import argparse, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "comun"))
import espacio as e
from rdflib import Graph

ap = argparse.ArgumentParser()
ap.add_argument("--dataset"); ap.add_argument("--finalidad"); ap.add_argument("--consumidor", default="universidad")
a = ap.parse_args()

filas = e.ofertas()
g = Graph()
for prov in sorted({f["proveedor"] for f in filas}):
    e.catalogo_rdf(filas, prov, g)
g.serialize(destination=str(AQUI / "ofertas.ttl"), format="turtle")

PETICIONES = [("universidad", "calidad-aire", "investigacion"),
              ("universidad", "calidad-aire", "comercial"),
              ("universidad", "ruido-urbano", "docencia"),
              ("universidad", "trafico-horario", "docencia"),
              ("universidad", "padron-resumen", "investigacion")]
if a.dataset:
    PETICIONES = [(a.consumidor, a.dataset, a.finalidad or "investigacion")]

print("\n🤝 PETICIONES CONTRA OFERTAS (ODRL)\n" + "─" * 78)
acuerdos, registro = Graph(), []
e._bind(acuerdos)
for c, ds, fin in PETICIONES:
    ok, motivo, deberes = e.evaluar_peticion(g, ds, fin)
    print(f"{'✅' if ok else '❌'} {c} → {ds} para «{fin}»: {motivo}")
    if ok:
        n = len(registro) + 1
        acuerdos += e.acuerdo_rdf(g, ds, c, fin, n)
        for d in deberes:
            registro.append(f"acuerdo-{n:03d} · deber «{d}»: {c} debe informar del uso de {ds} (finalidad: {fin})")
        if not deberes:
            registro.append(f"acuerdo-{n:03d} · sin deberes")
        print(f"      → nace el acuerdo-{n:03d}: assigner {e.participante(next(f['proveedor'] for f in filas if f['id'] == ds))['id']}, assignee {c}")
acuerdos.serialize(destination=str(AQUI / "acuerdos.ttl"), format="turtle")

print("\n🧾 REGISTRO DE DEBERES\n" + "─" * 78)
for r in registro:
    print("   · " + r)
print("\n💡 Oferta ≠ acuerdo: la oferta no tiene assignee; el acuerdo sí, y fija la finalidad concreta."
      "\n   Un deber como «inform» no lo cumple ODRL: lo cumple (y lo audita) el conector y el marco de gobierno.")
