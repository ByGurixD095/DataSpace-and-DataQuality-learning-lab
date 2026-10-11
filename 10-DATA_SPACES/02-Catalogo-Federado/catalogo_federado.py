#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02 · Catálogo federado: varios catálogos de proveedores consultados con UNA sola SPARQL.

  python catalogo_federado.py                                  # todas las ofertas del espacio
  python catalogo_federado.py --finalidad docencia             # solo las que permiten esa finalidad
  python catalogo_federado.py --min-calidad 0.9                # solo las de calidad ≥ 0.9
  python catalogo_federado.py --clasificacion Público          # solo las de ese nivel
  python catalogo_federado.py --proveedor empresa-movilidad    # el catálogo de un único participante

Cada proveedor publica SU catálogo en un GRAFO CON NOMBRE. Una consulta con GRAPH ?g sabe de quién viene
cada resultado; sin grafos con nombre, al mezclar los catálogos se perdería el origen.
Genera federado.trig (el conjunto de grafos con nombre).

Requiere: rdflib
"""
import argparse, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "comun"))
import espacio as e

ap = argparse.ArgumentParser()
ap.add_argument("--finalidad"); ap.add_argument("--min-calidad", type=float)
ap.add_argument("--clasificacion"); ap.add_argument("--proveedor")
a = ap.parse_args()

ds = e.catalogos_federados()
ds.serialize(destination=str(AQUI / "federado.trig"), format="trig")

filtros = []
if a.min_calidad is not None:
    filtros.append(f"FILTER(?calidad >= {a.min_calidad})")
if a.clasificacion:
    filtros.append(f"FILTER(?clas = esp:{e.NIVELES[a.clasificacion]})")
if a.finalidad:
    filtros.append(f'?oferta odrl:permission/odrl:constraint/odrl:rightOperand "{a.finalidad}" .')
externos = []        # el filtro sobre ?g va FUERA del bloque GRAPH: dentro, ?g aún no está ligada
if a.proveedor:
    externos.append(f'FILTER(STR(?g) = "urn:espacio:catalogo:{a.proveedor}")')

QUERY = """
PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX dct:  <http://purl.org/dc/terms/>
PREFIX odrl: <http://www.w3.org/ns/odrl/2/>
PREFIX dqv:  <http://www.w3.org/ns/dqv#>
PREFIX esp:  <http://example.org/espacio#>
SELECT ?g ?id ?titulo ?clas ?calidad WHERE {
  GRAPH ?g {
    ?d a dcat:Dataset ; dct:title ?titulo ; esp:nivelClasificacion ?clas ; odrl:hasPolicy ?oferta ;
       dcat:distribution/dqv:hasQualityMeasurement/dqv:value ?calidad .
    BIND(STRAFTER(STR(?d), "dataset-") AS ?id)
    %s
  }
  %s
} ORDER BY DESC(?calidad)
""" % ("\n    ".join(filtros), "\n  ".join(externos))

filas = list(ds.query(QUERY))
print(f"\n📚 CATÁLOGO FEDERADO · {len(list(ds.graphs())) - 1} catálogos · {len(filas)} oferta(s) encontrada(s)\n" + "─" * 88)
print(f"   {'PROVEEDOR':<19} {'DATASET':<22} {'NIVEL':<13} {'CALIDAD':>7}  TÍTULO")
for r in filas:
    prov = str(r.g).replace("urn:espacio:catalogo:", "")
    print(f"   {prov:<19} {str(r.id):<22} {str(r.clas).split('#')[-1]:<13} {float(r.calidad):>7.2f}  {r.titulo}")

# Lo que NO aparece también cuenta: datasets del espacio sin oferta o sin clasificar
fuera = [f for f in e.ofertas() if not (f["finalidades"] and f["clasificacion"] and f["calidad_completitud"])]
if fuera and not (a.finalidad or a.min_calidad is not None or a.clasificacion or a.proveedor):
    print("\n🕳️  PUBLICADOS PERO NO DESCUBRIBLES (les falta clasificación, oferta o calidad):")
    for f in fuera:
        print(f"   · {f['proveedor']}/{f['id']}")
    print("   → La consulta exige estos tres metadatos: un dataset mal descrito es, en la práctica, invisible.")
