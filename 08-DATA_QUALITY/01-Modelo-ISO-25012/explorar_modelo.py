#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01 · Modelo ISO/IEC 25012: las 15 características como grafo RDF (DQV + SKOS) y consultas SPARQL.

  python explorar_modelo.py

Qué hace:
  1. Construye el modelo (categorías + dimensiones) y lo guarda en caracteristicas_25012.ttl
  2. Lo interroga con SPARQL: ¿cuántas características son inherentes, mixtas o del sistema?
  3. Cruza el modelo con las medidas del laboratorio: ¿qué características tenemos cubiertas?

Requiere: rdflib   (pip install rdflib)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "comun"))
import dq

PFX = """PREFIX dqv: <http://www.w3.org/ns/dqv#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dq: <http://example.org/dq#>
"""

g = dq.modelo_rdf()
destino = Path(__file__).resolve().parent / "caracteristicas_25012.ttl"
g.serialize(destination=str(destino), format="turtle")
print(f"📄 Modelo guardado en {destino.name}  ({len(g)} tripletas)\n")

# Una dimensión en UNA categoría → solo inherente o solo sistema; en DOS → mixta
consulta = PFX + """
SELECT ?tipo (COUNT(?d) AS ?n) (GROUP_CONCAT(?nombre; separator=", ") AS ?caracteristicas) WHERE {
  { SELECT ?d (COUNT(?c) AS ?ncat) (SAMPLE(?c) AS ?cat) WHERE { ?d a dqv:Dimension ; dqv:inCategory ?c } GROUP BY ?d }
  ?d skos:prefLabel ?nombre . FILTER(LANG(?nombre) = "es")
  BIND(IF(?ncat > 1, "🧬🖥️ mixtas", IF(?cat = dq:cat-inherente, "🧬 inherentes", "🖥️ del sistema")) AS ?tipo)
} GROUP BY ?tipo ORDER BY DESC(?n)
"""
print("Reparto de las 15 características (consulta SPARQL sobre el modelo):\n")
for fila in g.query(consulta):
    print(f"  {str(fila.tipo):<18} {int(fila.n):>2}   {fila.caracteristicas}")

medidas = dq.medir_todo(dq.cargar_csv())
cubiertas = {m.caracteristica for m in medidas.values()}
print(f"\n📏 Cobertura de este laboratorio: {len(cubiertas)} de {len(dq.CARACTERISTICAS)} características tienen alguna medida automática.\n")
for cid, es, en, persp, _ in dq.CARACTERISTICAS:
    marca = "✅" if cid in cubiertas else "·"
    print(f"  {marca} {es:<18} ({dq.tipo_perspectiva(persp)})")
print("\n💡 Las que quedan sin cubrir (credibilidad, trazabilidad, disponibilidad…) no se miden mirando solo")
print("   los valores: requieren inspección, metadatos o monitorización del sistema.")
