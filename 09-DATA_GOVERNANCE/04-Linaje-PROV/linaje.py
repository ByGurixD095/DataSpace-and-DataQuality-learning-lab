#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
04 · Linaje con PROV-O: de dónde viene cada dato y a qué afecta si cambia.

  python linaje.py                         # árbol de linaje + propagación de clasificación + cobertura de linaje
  python linaje.py --origen informe-movilidad   # aguas ARRIBA: ¿de qué depende?
  python linaje.py --impacto sensores-iot       # aguas ABAJO: ¿a qué afecta si cambia?

Genera linaje.ttl. Código de salida 1 si la propagación de clasificación detecta alertas.
Requiere: rdflib
"""
import argparse, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "comun"))
import gov
from rdflib import Graph, Literal, Namespace, RDF, URIRef

ap = argparse.ArgumentParser()
ap.add_argument("--origen"); ap.add_argument("--impacto")
a = ap.parse_args()

EX, GOV, PROV, DCT = (Namespace(x) for x in (gov.EX_NS, gov.GOV_NS, "http://www.w3.org/ns/prov#", "http://purl.org/dc/terms/"))
filas = gov.cargar_inventario()
g = gov.catalogo_rdf(filas)                      # el catálogo gobernado es la base: el linaje se SUPERPONE

# Entidades que NO están en el catálogo (fuentes e informes) y su clasificación
EXTRA = {
    "fuente-estaciones-calidad-aire": ("Estaciones de calidad del aire (fuente)", "publico"),
    "lecturas-validadas": ("Lecturas validadas", "publico"),
    "indicador-calidad-aire-mensual": ("Indicador mensual de calidad del aire", "publico"),
    "informe-cumplimiento-ambiental": ("Informe de cumplimiento ambiental", "publico"),
    "fuente-sensores-viaria": ("Sensores de la vía (fuente)", "interno"),
    "informe-movilidad": ("Informe de movilidad", "interno"),
    "fuente-sonometros": ("Sonómetros (fuente)", "publico"),
    "informe-demografico-publico": ("Informe demográfico público", "publico"),
    "tabla-demografica-anonimizada": ("Tabla demográfica anonimizada", "publico"),
}
# (salida, [entradas], actividad, ¿anonimiza?)
DERIVACIONES = [
    ("lecturas-validadas", ["fuente-estaciones-calidad-aire"], "validacion-lecturas", False),
    ("dataset-calidad-aire", ["lecturas-validadas"], "publicacion-calidad-aire", False),
    ("indicador-calidad-aire-mensual", ["dataset-calidad-aire"], "calculo-indicador-mensual", False),
    ("informe-cumplimiento-ambiental", ["indicador-calidad-aire-mensual"], "elaboracion-informe-ambiental", False),
    ("dataset-sensores-iot", ["fuente-sensores-viaria"], "ingesta-sensores", False),
    ("dataset-trafico-horario", ["dataset-sensores-iot"], "agregacion-horaria", False),
    ("informe-movilidad", ["dataset-trafico-horario", "dataset-aparcamientos"], "elaboracion-informe-movilidad", False),
    ("dataset-ruido-urbano", ["fuente-sonometros"], "ingesta-sonometros", False),
    ("informe-demografico-publico", ["dataset-padron-resumen"], "elaboracion-informe-demografico", False),
    ("tabla-demografica-anonimizada", ["dataset-padron-resumen"], "anonimizacion-padron", True),
]
RANGO = {"publico": 0, "interno": 1, "confidencial": 2}
NOMBRE = {c: es for c, es, _ in gov.CLASIFICACION}

for eid, (titulo, nivel) in EXTRA.items():
    e = EX[eid]
    g.add((e, RDF.type, PROV.Entity)); g.add((e, DCT.title, Literal(titulo, lang="es")))
    g.add((e, GOV.nivelClasificacion, GOV[nivel]))
for salida, entradas, act, anon in DERIVACIONES:
    ac = EX[f"actividad-{act}"]
    g.add((ac, RDF.type, PROV.Activity)); g.add((EX[salida], PROV.wasGeneratedBy, ac))
    if anon:
        g.add((ac, GOV.anonimiza, Literal(True)))
    for ent in entradas:
        g.add((ac, PROV.used, EX[ent])); g.add((EX[salida], PROV.wasDerivedFrom, EX[ent]))
g.serialize(destination=str(AQUI / "linaje.ttl"), format="turtle")

PFX = gov.PFX + "PREFIX prov: <http://www.w3.org/ns/prov#>\nPREFIX dct: <http://purl.org/dc/terms/>\n"


def corto(u): return str(u).replace(gov.EX_NS, "")
def nivel_de(u):
    n = next(g.objects(URIRef(u), GOV.nivelClasificacion), None)
    return str(n).split("#")[-1] if n else None
def etiqueta(u):
    n = nivel_de(u)
    return f"{corto(u)}  [{NOMBRE.get(n, 'sin clasificar')}]"


def resolver(nombre):
    for pref in ("", "dataset-"):
        if (EX[pref + nombre], None, None) in g:
            return EX[pref + nombre]
    sys.exit(f"No existe «{nombre}» en el grafo de linaje.")


def arbol(nodo, sentido, prof=0, vistos=()):
    """sentido='arriba' sigue wasDerivedFrom; 'abajo' lo recorre al revés."""
    if sentido == "arriba":
        sig = sorted(g.objects(nodo, PROV.wasDerivedFrom))
    else:
        sig = sorted(g.subjects(PROV.wasDerivedFrom, nodo))
    for i, s in enumerate(sig):
        if s in vistos:
            continue
        rama = "└─ " if i == len(sig) - 1 else "├─ "
        print("   " + "   " * prof + rama + etiqueta(s))
        arbol(s, sentido, prof + 1, vistos + (nodo,))


if a.origen or a.impacto:
    n = resolver(a.origen or a.impacto)
    sentido = "arriba" if a.origen else "abajo"
    q = ("?x prov:wasDerivedFrom+ <%s>" if sentido == "abajo" else "<%s> prov:wasDerivedFrom+ ?x") % n
    total = {str(r.x) for r in g.query(PFX + "SELECT DISTINCT ?x WHERE { %s }" % q)}
    print(f"\n🔗 {'ORIGEN (aguas arriba)' if sentido == 'arriba' else 'IMPACTO (aguas abajo)'} de {etiqueta(n)}\n")
    arbol(n, sentido)
    print(f"\n   {len(total)} elemento(s) en la cadena (consulta SPARQL con prov:wasDerivedFrom+).")
    if sentido == "abajo" and total:
        print("   → Si este dato cambia o se retira, hay que avisar a los responsables de esos elementos.")
    sys.exit(0)

# ── 1. Árbol de linaje desde cada elemento final ────────────────────────────────
finales = [r.x for r in g.query(PFX + """SELECT DISTINCT ?x WHERE { ?x prov:wasDerivedFrom ?y .
                                          FILTER NOT EXISTS { ?z prov:wasDerivedFrom ?x } } ORDER BY ?x""")]
print("\n🌳 LINAJE (de cada producto final hacia sus fuentes)\n" + "─" * 60)
for f in finales:
    print(f"\n● {etiqueta(f)}")
    arbol(f, "arriba")

# ── 2. Propagación de clasificación ─────────────────────────────────────────────
print("\n\n🔒 PROPAGACIÓN DE CLASIFICACIÓN\n" + "─" * 60)
print("Regla: un derivado no puede ser MENOS restrictivo que su origen, salvo que la actividad anonimice.")
alertas, ok = [], 0
for r in g.query(PFX + "SELECT ?s ?o ?ac WHERE { ?s prov:wasDerivedFrom ?o ; prov:wasGeneratedBy ?ac }"):
    ns, no = nivel_de(r.s), nivel_de(r.o)
    if ns is None or no is None:
        continue
    anon = (r.ac, GOV.anonimiza, Literal(True)) in g
    if RANGO[ns] < RANGO[no] and not anon:
        alertas.append((corto(r.s), ns, corto(r.o), no))
    else:
        ok += 1
print(f"   ✅ {ok} derivaciones coherentes (incluidas las que anonimizan de forma declarada)")
for s, ns, o, no in alertas:
    print(f"   🚨 {s} es «{NOMBRE[ns]}» pero deriva de {o} que es «{NOMBRE[no]}» y la actividad no anonimiza")

# ── 3. Cobertura de linaje sobre el inventario ──────────────────────────────────
print("\n\n📈 COBERTURA DE LINAJE (datasets del inventario con linaje documentado)\n" + "─" * 60)
todos = gov.todos_los_datasets(g)
con = {str(r.d) for r in g.query(PFX + """SELECT DISTINCT ?d WHERE { ?d a dcat:Dataset .
                                         { ?d prov:wasDerivedFrom ?x } UNION { ?y prov:wasDerivedFrom ?d } }""")}
print(f"   {len(con)}/{len(todos)}  {gov.barra(len(con) / len(todos))}  {len(con) / len(todos):.0%}")
for d in sorted(todos - con):
    print(f"   · sin linaje: {corto(d)}")

sys.exit(1 if alertas else 0)
