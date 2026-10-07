#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
07 · Integración: CSV → RDF → SHACL → medidas → reglas → DQV → catálogo DCAT → SPARQL.

  python flujo_completo.py
  python flujo_completo.py --ahora 2026-10-06T10:00

El mismo dataset, medido de DOS maneras (Python puro y RDF+SHACL+SPARQL): los resultados deben coincidir.
Después se decide con reglas de negocio, se publica el resultado en DQV y se cuelga del catálogo DCAT
de 07-DCAT (si está al lado) para que un consumidor pueda filtrar por calidad.

Requiere: rdflib y pyshacl   (pip install rdflib pyshacl)
"""
import argparse, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "comun"))
import dq

try:
    from pyshacl import validate
    from rdflib import Graph, Literal, Namespace, RDF, URIRef, XSD
except ImportError:
    sys.exit("Faltan dependencias. Instálalas con:  pip install rdflib pyshacl")

ap = argparse.ArgumentParser()
ap.add_argument("--ahora")
a = ap.parse_args()
ahora = dq.parse_ahora(a.ahora)
EX, SH = Namespace("http://example.org/"), Namespace("http://www.w3.org/ns/shacl#")

def paso(n, texto):
    print(f"\n{'━' * 4} {n} · {texto} {'━' * max(2, 66 - len(texto))}")

# ── 1. CSV → RDF ───────────────────────────────────────────────────────────────
paso(1, "Los datos pasan de CSV a RDF")
filas = dq.cargar_csv()
datos = Graph(); datos.bind("ex", EX)
for i, f in enumerate(filas, 1):
    n = EX[f"lectura-{i:03d}"]                       # un nodo por FILA: los duplicados siguen visibles
    datos.add((n, RDF.type, EX.Lectura))
    datos.add((n, EX.estacion, Literal(f["estacion"])))
    datos.add((n, EX.fechaHora, Literal(f["fecha_hora"], datatype=XSD.dateTime)))
    for campo in ("no2", "pm10", "pm25"):
        if dq._num(f[campo]) is not None:
            datos.add((n, EX[campo], Literal(f[campo], datatype=XSD.decimal)))
print(f"   {len(filas)} filas → {len(datos)} tripletas")

# ── 2. SHACL ───────────────────────────────────────────────────────────────────
paso(2, "SHACL valida las reglas BR.DV")
shapes = Graph().parse(AQUI / "shapes" / "lectura.shacl.ttl", format="turtle")
conforma, informe, _ = validate(datos, shacl_graph=shapes, inference="none")
nodos_con_violacion = set(informe.objects(None, SH.focusNode))
mensajes = {}
for r in informe.subjects(RDF.type, SH.ValidationResult):
    m = str(next(informe.objects(r, SH.resultMessage), "(sin mensaje)"))
    mensajes[m] = mensajes.get(m, 0) + 1
print(f"   ¿Conforme? {conforma}  ·  nodos con alguna violación: {len(nodos_con_violacion)}")
for m, n in mensajes.items():
    print(f"     · {n} × {m}")

# ── 3. Dos caminos, un mismo resultado ─────────────────────────────────────────
paso(3, "Dos caminos para medir: ¿coinciden?")
total = len(filas)
con_no2 = int(next(iter(datos.query("SELECT (COUNT(?l) AS ?c) WHERE { ?l a <http://example.org/Lectura> ; <http://example.org/no2> ?v }")))[0])
extras = int(next(iter(datos.query("""
    SELECT (COALESCE(SUM(?n - 1), 0) AS ?extra) WHERE {
      SELECT ?e ?t (COUNT(?l) AS ?n) WHERE { ?l a <http://example.org/Lectura> ;
          <http://example.org/estacion> ?e ; <http://example.org/fechaHora> ?t }
      GROUP BY ?e ?t HAVING (COUNT(?l) > 1) }""")))[0])
medidas = dq.medir_todo(filas, ahora)
reglas = dq.cargar_reglas()
_, ratio_dv12 = dq.evaluar_registros(filas, reglas["br_dv"], solo=("DV1", "DV2"))
rdf_vs_py = [
    ("completitud (SPARQL: COUNT)", con_no2 / total, medidas["completitud_no2"].valor),
    ("unicidad (SPARQL: GROUP BY/HAVING)", (total - extras) / total, medidas["unicidad_clave"].valor),
    ("registros conformes (SHACL)", (total - len(nodos_con_violacion)) / total, ratio_dv12),
]
print(f"   {'medida':<38} {'RDF':>8} {'Python':>8}")
for nombre, rdf, py in rdf_vs_py:
    print(f"   {nombre:<38} {rdf:>8.1%} {py:>8.1%}   {'✅ coincide' if abs(rdf - py) < 1e-6 else '❌ DIFIERE'}")

# ── 4. Reglas de negocio: ¿es utilizable? ──────────────────────────────────────
paso(4, "Reglas de negocio: ¿es utilizable?")
_, ratio_todas = dq.evaluar_registros(filas, reglas["br_dv"])
valores = dq.valores_para_reglas(medidas, ratio_todas)
for nombre, ctx in reglas["contextos"].items():
    nivel, decision, _ = dq.evaluar_contexto(valores, ctx)
    print(f"   {nombre:<24} {nivel:<6} {decision}")

# ── 5. DQV + catálogo DCAT ─────────────────────────────────────────────────────
paso(5, "Publicar en DQV y colgar del catálogo DCAT")
lista = list(medidas.values())
lista.append(dq.Medida("conformidad_shacl", "Registros conformes con las shapes", "accuracy",
                       total - len(nodos_con_violacion), total, "Registros sin violaciones SHACL / registros"))
catalogo_07 = dq.RAIZ.parent / "07-DCAT" / "03-DCAT-AP-ES" / "ejemplo-dcat-ap-es.ttl"
catalogo = Graph()
if catalogo_07.exists():
    catalogo.parse(catalogo_07, format="turtle")
    print(f"   Catálogo DCAT-AP-ES cargado desde {catalogo_07.relative_to(dq.RAIZ.parent)}")
else:
    from rdflib import Namespace as NS
    DCAT, DCT = NS("http://www.w3.org/ns/dcat#"), NS("http://purl.org/dc/terms/")
    ds, dist = EX["dataset-calidad-aire"], URIRef(dq.DISTRIBUCION_POR_DEFECTO)
    catalogo.add((ds, RDF.type, DCAT.Dataset)); catalogo.add((ds, DCT.title, Literal("Calidad del aire", lang="es")))
    catalogo.add((ds, DCAT.distribution, dist)); catalogo.add((dist, RDF.type, DCAT.Distribution))
    print("   (No se encontró 07-DCAT al lado: uso un catálogo mínimo de ejemplo)")
dq.construir_dqv(lista, dq.DISTRIBUCION_POR_DEFECTO, ahora, g=catalogo)
salida = AQUI / "salida"; salida.mkdir(exist_ok=True)
catalogo.serialize(destination=str(salida / "catalogo_con_calidad.ttl"), format="turtle")
print(f"   Guardado en salida/catalogo_con_calidad.ttl ({len(catalogo)} tripletas)")

# ── 6. El consumidor filtra por calidad ────────────────────────────────────────
paso(6, "El consumidor filtra por calidad EN el catálogo")
consulta = """
PREFIX dcat: <http://www.w3.org/ns/dcat#>   PREFIX dct: <http://purl.org/dc/terms/>
PREFIX dqv: <http://www.w3.org/ns/dqv#>
SELECT ?titulo ?metrica ?valor WHERE {
  ?ds a dcat:Dataset ; dct:title ?titulo ; dcat:distribution ?dist .
  ?dist dqv:hasQualityMeasurement ?m . ?m dqv:isMeasurementOf ?met ; dqv:value ?valor .
  FILTER(LANG(?titulo) = "es" || LANG(?titulo) = "")
  FILTER(?valor >= 0.90)
  BIND(REPLACE(STR(?met), "^.*metrica-", "") AS ?metrica)
} ORDER BY DESC(?valor)"""
print("   «Dame los datasets con alguna medida ≥ 90 %»:\n")
for r in catalogo.query(consulta):
    print(f"     {str(r.titulo):<18} {str(r.metrica):<20} {float(r.valor):.1%}")
print("\n🏁 Flujo completo: dato → RDF → validación → medida → decisión → metadato publicado → consulta.")
