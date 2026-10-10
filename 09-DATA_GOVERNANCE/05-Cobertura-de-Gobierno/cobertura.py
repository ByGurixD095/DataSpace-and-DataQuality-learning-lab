#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
05 · Cobertura de gobierno: ¿qué parte del catálogo está realmente gobernada?

  python cobertura.py                          # SHACL + SPARQL, barras, puntuación por dataset, plan de remediación
  python cobertura.py --asignar-por-defecto    # simula "arreglar" asignando un propietario genérico (¡y por qué no sirve!)
  python cobertura.py --fecha 2027-01-01       # cambia la fecha de referencia del indicador de revisión

Dos miradas al mismo problema:
  · SHACL  → ¿cumple CADA dataset las reglas?  (informe de no conformidades)
  · SPARQL → ¿qué PORCENTAJE las cumple?       (indicadores agregados)
Las dos deben contar la misma historia; si no, hay un fallo en las reglas o en las consultas.

Requiere: rdflib, pyshacl
"""
import argparse, sys
from datetime import date
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "comun"))
import gov
from rdflib import Graph, Namespace, RDF
from pyshacl import validate

ap = argparse.ArgumentParser()
ap.add_argument("--asignar-por-defecto", action="store_true")
ap.add_argument("--fecha", help="fecha de referencia (AAAA-MM-DD); por defecto 2026-10-08")
a = ap.parse_args()
ahora = gov.parse_fecha(a.fecha)

SH = Namespace("http://www.w3.org/ns/shacl#")
filas = gov.cargar_inventario()
if a.asignar_por_defecto:
    print("🧪 SIMULACIÓN: rellenar los huecos con valores genéricos para «mejorar» las cifras\n")
    for f in filas:
        for r in ("propietario", "steward"):
            f[r] = f[r] or "Por asignar"
g = gov.catalogo_rdf(filas)

shapes = Graph().parse(str(AQUI / "shapes" / "gobierno.shacl.ttl"))
if ahora != gov.AHORA_POR_DEFECTO:       # la fecha de las shapes también debe seguir a --fecha
    from rdflib import Literal, XSD
    for s, p, o in list(shapes.triples((None, SH.minInclusive, None))):
        shapes.set((s, p, Literal(ahora.isoformat(), datatype=XSD.date)))
_, rg, _ = validate(g, shacl_graph=shapes, inference="none")

# ── Indicadores (SPARQL) ───────────────────────────────────────────────────────
print(f"\n📊 COBERTURA DE GOBIERNO · {len(filas)} datasets · fecha de referencia {ahora}\n" + "─" * 66)
cob = gov.cobertura(g, ahora)
for c in cob:
    marca = "✅" if c["cumplen"] == c["total"] else ("⚠️ " if c["valor"] >= 0.7 else "🚨")
    print(f"{marca} {c['nombre']:<38} {c['cumplen']:>2}/{c['total']:<2} {gov.barra(c['valor'])} {c['valor']:>4.0%}")

# ── Informe SHACL: qué falla y dónde ───────────────────────────────────────────
fallos = {}   # dataset → [(severidad, mensaje)]
for r in rg.subjects(RDF.type, SH.ValidationResult):
    d = str(rg.value(r, SH.focusNode)).replace(gov.EX_NS + "dataset-", "")
    sev = "Violation" if rg.value(r, SH.resultSeverity) == SH.Violation else "Warning"
    fallos.setdefault(d, []).append((sev, str(rg.value(r, SH.resultMessage))))

print("\n🔎 VALIDACIÓN SHACL (reglas de gobierno)\n" + "─" * 66)
n_v = sum(1 for v in fallos.values() for s, _ in v if s == "Violation")
n_w = sum(1 for v in fallos.values() for s, _ in v if s == "Warning")
print(f"   {n_v} violaciones (bloquean) · {n_w} avisos (recomendaciones)")

# ── Verificación cruzada SPARQL ↔ SHACL ────────────────────────────────────────
# Cada indicador SPARQL "no cumple" debe corresponderse con un mensaje SHACL concreto.
MENSAJE = {"propietario": "propietario", "steward": "steward", "custodio": "custodio", "clasificacion": "clasificación",
           "politica": "política", "calidad": "calidad", "revision": "revisión"}
print("\n🔁 VERIFICACIÓN CRUZADA (SPARQL vs SHACL)")
coherente = True
for c in cob:
    fallan_sparql = c["total"] - c["cumplen"]
    fallan_shacl = sum(1 for v in fallos.values() if any(MENSAJE[c["id"]] in m.lower() for _, m in v))
    ok = fallan_sparql == fallan_shacl
    coherente &= ok
    print(f"   {'✅' if ok else '❌'} {c['id']:<14} SPARQL {fallan_sparql} · SHACL {fallan_shacl}")
if not coherente:
    print("   ⚠️  Discrepancia: revisa la consulta o la shape correspondiente.")

# ── Puntuación por dataset ─────────────────────────────────────────────────────
print("\n🏅 PUNTUACIÓN POR DATASET (7 criterios)\n" + "─" * 66)
puntos = {}
for c in cob:
    for d in c["datasets"]:
        puntos[d.replace(gov.EX_NS + "dataset-", "")] = puntos.get(d.replace(gov.EX_NS + "dataset-", ""), 0) + 1
for f in sorted(filas, key=lambda x: -puntos.get(x["id"], 0)):
    p = puntos.get(f["id"], 0)
    print(f"   {f['id']:<18} {p}/7 {gov.barra(p / 7, 14)}")

# ── Plan de remediación ────────────────────────────────────────────────────────
print("\n🛠️  PLAN DE REMEDIACIÓN (primero lo que bloquea)\n" + "─" * 66)
for sev, icono in (("Violation", "🚨"), ("Warning", "⚠️ ")):
    for d in sorted(fallos):
        for s, m in fallos[d]:
            if s == sev:
                print(f"   {icono} {d:<18} {m}")

if a.asignar_por_defecto:
    print("\n💡 Las cifras de «propietario» y «steward» suben al 100 %, pero «Por asignar» no es nadie:"
          "\n   el indicador mide que EXISTE un registro, no que la responsabilidad esté ASUMIDA."
          "\n   Un propietario lo designa quien tiene autoridad sobre el dato; no se inventa para cumplir un KPI.")
sys.exit(1 if n_v else 0)
