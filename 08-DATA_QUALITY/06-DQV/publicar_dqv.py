#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
06 · DQV: publicar las mediciones como RDF y consultarlas con SPARQL.

  python publicar_dqv.py
  python publicar_dqv.py --distribucion http://example.org/mi-distribucion

Genera calidad_aire.dqv.ttl: una dqv:QualityMeasurement por medida, con su métrica, su dimensión
(ISO/IEC 25012) y la fecha de la medición, colgada de la dcat:Distribution.

Requiere: rdflib   (pip install rdflib)
"""
import argparse, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "comun"))
import dq

ap = argparse.ArgumentParser()
ap.add_argument("--distribucion", default=dq.DISTRIBUCION_POR_DEFECTO)
ap.add_argument("--ahora")
a = ap.parse_args()
ahora = dq.parse_ahora(a.ahora)

medidas = dq.medir_todo(dq.cargar_csv(), ahora)
g = dq.construir_dqv(list(medidas.values()), a.distribucion, ahora)
destino = AQUI / "calidad_aire.dqv.ttl"
g.serialize(destination=str(destino), format="turtle")
print(f"\n📄 {destino.name}: {len(g)} tripletas · {len(medidas)} mediciones sobre <{a.distribucion}>\n")

PFX = """PREFIX dqv: <http://www.w3.org/ns/dqv#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX prov: <http://www.w3.org/ns/prov#>
"""
print("🔎 SPARQL 1 · ¿qué se ha medido, sobre qué dimensión y cuánto vale?\n")
q1 = PFX + """
SELECT ?dimension ?metrica ?valor WHERE {
  ?m a dqv:QualityMeasurement ; dqv:isMeasurementOf ?met ; dqv:value ?valor .
  ?met dqv:inDimension ?d . ?d skos:prefLabel ?dimension . FILTER(LANG(?dimension) = "es")
  BIND(REPLACE(STR(?met), "^.*metrica-", "") AS ?metrica)
} ORDER BY ?dimension ?metrica"""
for r in g.query(q1):
    print(f"   {str(r.dimension):<14} {str(r.metrica):<18} {float(r.valor):.4f}")

print("\n🔎 SPARQL 2 · ¿qué mediciones NO alcanzan el 95 %? (la pregunta de un consumidor)\n")
q2 = PFX + """
SELECT ?metrica ?valor ?cuando WHERE {
  ?m dqv:isMeasurementOf ?met ; dqv:value ?valor ; prov:generatedAtTime ?cuando .
  FILTER(?valor < 0.95)
  BIND(REPLACE(STR(?met), "^.*metrica-", "") AS ?metrica)
} ORDER BY ?valor"""
for r in g.query(q2):
    print(f"   {str(r.metrica):<18} {float(r.valor):.4f}   medido el {r.cuando}")

print("\n💡 Cada medición lleva su fecha: sin ella, el resultado caduca sin que nadie lo sepa.")
print("   Siguiente paso: colgar este grafo del catálogo DCAT → carpeta 07-Integracion.")
