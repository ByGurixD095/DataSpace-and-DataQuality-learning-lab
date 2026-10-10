#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
03 · Catálogo y glosario: el inventario como catálogo DCAT con gobierno visible + un glosario SKOS.

  python catalogo_gobernado.py                              # genera ficheros y detecta conflictos de glosario
  python catalogo_gobernado.py --dataset trafico-horario    # ficha de gobierno de un dataset
  python catalogo_gobernado.py --termino "Estación activa"  # busca un término del glosario

Genera catalogo_gobernado.ttl y glosario.ttl.   Requiere: rdflib
"""
import argparse, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "comun"))
import gov
from rdflib import Graph, Literal, Namespace, RDF, URIRef

ap = argparse.ArgumentParser()
ap.add_argument("--dataset"); ap.add_argument("--termino")
a = ap.parse_args()

SKOS, GOV, PROV, EX = (Namespace(x) for x in ("http://www.w3.org/2004/02/skos/core#", gov.GOV_NS,
                                               "http://www.w3.org/ns/prov#", gov.EX_NS))
filas = gov.cargar_inventario()
cat = gov.catalogo_rdf(filas)
cat.serialize(destination=str(AQUI / "catalogo_gobernado.ttl"), format="turtle")

# ── Glosario SKOS: un concepto por (término, dominio) ────────────────────────────
glos = Graph(); glos.bind("skos", SKOS); glos.bind("gov", GOV); glos.bind("prov", PROV)
esq = GOV["glosario"]
glos.add((esq, RDF.type, SKOS.ConceptScheme)); glos.add((esq, SKOS.prefLabel, Literal("Glosario de datos municipal", lang="es")))
for t in gov.cargar_csv(gov.GLOSARIO):
    c = URIRef(f"http://example.org/glosario/{gov.slug(t['termino'])}--{gov.slug(t['dominio'])}")
    glos.add((c, RDF.type, SKOS.Concept)); glos.add((c, SKOS.inScheme, esq))
    glos.add((c, SKOS.prefLabel, Literal(t["termino"], lang="es")))
    glos.add((c, SKOS.definition, Literal(t["definicion"], lang="es")))
    glos.add((c, GOV.dominio, Literal(t["dominio"], lang="es")))
    glos.add((c, PROV.wasAttributedTo, EX[f"unidad-{gov.slug(t['propietario'])}"]))
glos.serialize(destination=str(AQUI / "glosario.ttl"), format="turtle")

PFX = "PREFIX skos: <http://www.w3.org/2004/02/skos/core#>\nPREFIX gov: <http://example.org/gobierno#>\n"

if a.termino:
    q = PFX + "SELECT ?dom ?def WHERE { ?c skos:prefLabel ?l ; skos:definition ?def ; gov:dominio ?dom . FILTER(LCASE(STR(?l)) = LCASE(\"%s\")) }" % a.termino.replace('"', "")
    res = list(glos.query(q))
    print(f"\n📖 «{a.termino}»: {len(res)} definición(es)")
    for r in res:
        print(f"   · [{r.dom}] {r['def']}")
    if len(res) > 1:
        print("\n⚠️  Hay más de una definición: es un conflicto de gobierno, no un detalle técnico.")
    sys.exit(0)

if a.dataset:
    f = next((x for x in filas if x["id"] == a.dataset), None)
    if not f:
        sys.exit(f"No existe el dataset «{a.dataset}».")
    print(f"\n📇 FICHA DE GOBIERNO · {f['titulo']}\n" + "─" * 52)
    for k, etiqueta in (("dominio", "Dominio"), ("propietario", "Propietario"), ("steward", "Steward"),
                        ("custodio", "Custodio técnico"), ("clasificacion", "Clasificación"),
                        ("proxima_revision", "Próxima revisión"), ("politica_uso", "Política de uso"),
                        ("calidad_evaluada", "Calidad evaluada")):
        v = f[k] or "— (¡falta!)"
        print(f"  {etiqueta:<18} {'❌ ' if v.startswith('—') else ''}{v}")
    sys.exit(0)

print(f"\n📚 Catálogo gobernado: {len(filas)} datasets · {len(cat)} tripletas  →  catalogo_gobernado.ttl")
print(f"📖 Glosario: {len(list(glos.subjects(RDF.type, SKOS.Concept)))} conceptos  →  glosario.ttl")

print("\n🔎 Conflictos de definición (mismo término, definiciones distintas):\n")
q = PFX + """SELECT ?l (COUNT(DISTINCT ?def) AS ?n) (GROUP_CONCAT(DISTINCT ?dom; separator=" vs ") AS ?doms) WHERE {
  ?c skos:prefLabel ?l ; skos:definition ?def ; gov:dominio ?dom . } GROUP BY ?l HAVING (COUNT(DISTINCT ?def) > 1)"""
hubo = False
for r in glos.query(q):
    hubo = True
    print(f"   ⚠️  «{r.l}» tiene {r.n} definiciones distintas ({r.doms})")
if hubo:
    print("\n💡 Esto es lo que hace que dos informes den cifras distintas para «lo mismo».")
    print("   Decisión de gobierno necesaria: unificar la definición o RENOMBRAR uno de los términos.")
    print("   Prueba:  python catalogo_gobernado.py --termino \"Estación activa\"")
