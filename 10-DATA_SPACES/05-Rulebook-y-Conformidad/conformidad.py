#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
05 · Rulebook y conformidad: el rulebook como validación automática (SHACL).

  python conformidad.py                      # valida ofertas y participantes, cruza con el rulebook en Python
  python conformidad.py --participante empresa-movilidad

Dos niveles de validación:
  A) OFERTAS: ¿puede cada dataset publicarse en el espacio? (shapes/ofertas.shacl.ttl)
  B) PARTICIPANTES: ¿cumple cada uno el rulebook? (shapes/participantes.shacl.ttl)
     Las reglas R05, R06 y R07 se DERIVAN del resultado de A: no se declaran, se demuestran.
La decisión que sale de SHACL se compara con la del rulebook en Python (comun/espacio.py): deben coincidir.

Requiere: rdflib, pyshacl.  Sale con código 1 si hay violaciones.
"""
import argparse, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "comun"))
import espacio as e
from rdflib import Graph, Literal, Namespace, RDF, XSD
from pyshacl import validate

ap = argparse.ArgumentParser(); ap.add_argument("--participante")
a = ap.parse_args()
SH, ESP, EX, DCT = Namespace("http://www.w3.org/ns/shacl#"), Namespace(e.ESP_NS), Namespace(e.EX_NS), Namespace("http://purl.org/dc/terms/")


def resultados(rg):
    out = []
    for r in rg.subjects(RDF.type, SH.ValidationResult):
        sev = "Violation" if rg.value(r, SH.resultSeverity) == SH.Violation else "Warning"
        out.append((rg.value(r, SH.focusNode), sev, str(rg.value(r, SH.resultMessage))))
    return out


# ── A. Ofertas ──────────────────────────────────────────────────────────────────
filas = e.ofertas()
g = Graph()
for prov in sorted({f["proveedor"] for f in filas}):
    e.catalogo_rdf(filas, prov, g)
_, rg, _ = validate(g, shacl_graph=str(AQUI / "shapes" / "ofertas.shacl.ttl"), inference="none")
res_o = resultados(rg)
print(f"\n📦 A. OFERTAS · {len(filas)} datasets en {len({f['proveedor'] for f in filas})} catálogos\n" + "─" * 70)
por_ds = {}
for foco, sev, msg in res_o:
    por_ds.setdefault(str(foco).replace(e.EX_NS, ""), []).append((sev, msg))
for f in filas:
    probs = por_ds.get(f"dataset-{f['id']}", [])
    estado = "✅ publicable" if not probs else ("❌ NO publicable" if any(s == "Violation" for s, _ in probs) else "⚠️  publicable con avisos")
    print(f"   {f['id']:<22} {estado}")
    for s, m in probs:
        print(f"        {'🚨' if s == 'Violation' else '⚠️ '} {m}")

# ── Derivar R05/R06/R07 de A ───────────────────────────────────────────────────
def derivado(prov, texto):
    for foco, _, msg in res_o:
        pub = next(g.objects(foco, DCT.publisher), None)
        if pub == EX[prov] and texto in msg:
            return False
    return any(f["proveedor"] == prov for f in filas)

# ── B. Participantes ───────────────────────────────────────────────────────────
gp = Graph(); gp.bind("esp", ESP)
CAMPOS = {"trata_datos_personales": "tratamientoDatosPersonales", "adhesion_firmada": "adhesionFirmada",
          "contacto_institucional": "contactoInstitucional", "dpd": "dpd", "catalogo_dcat": "catalogoDcat",
          "conector": "conector", "acepta_politicas": "aceptaPoliticas", "registro_usos": "registroUsos"}
for p in e.participantes():
    n = EX[p["id"]]
    gp.add((n, RDF.type, ESP.Participante)); gp.add((n, RDF.type, ESP.Proveedor if p["rol"] == "proveedor" else ESP.Consumidor))
    for col, prop in CAMPOS.items():
        if p[col] in ("si", "no"):
            gp.add((n, ESP[prop], Literal(p[col] == "si", datatype=XSD.boolean)))
    if p["rol"] == "proveedor":
        gp.add((n, ESP.clasificacionCompleta, Literal(derivado(p["id"], "clasificación"), datatype=XSD.boolean)))
        gp.add((n, ESP.politicasOdrl, Literal(derivado(p["id"], "oferta ODRL"), datatype=XSD.boolean)))
        gp.add((n, ESP.calidadPublicada, Literal(derivado(p["id"], "calidad"), datatype=XSD.boolean)))
_, rgp, _ = validate(gp, shacl_graph=str(AQUI / "shapes" / "participantes.shacl.ttl"), inference="none")
res_p = resultados(rgp)

print("\n\n🏛️  B. PARTICIPANTES (rulebook como SHACL)\n" + "─" * 70)
n_viol, coherente = 0, True
plan = []
for p in e.participantes():
    if a.participante and p["id"] != a.participante:
        continue
    mios = [(s, m) for foco, s, m in res_p if str(foco) == e.EX_NS + p["id"]]
    viol = [m for s, m in mios if s == "Violation"]; avis = [m for s, m in mios if s == "Warning"]
    n_viol += len(viol)
    dec_shacl = "no admitido" if viol else ("admitido con recomendaciones" if avis else "admitido")
    dec_py, _ = e.evaluar_participante(p)
    coherente &= dec_shacl == dec_py
    print(f"{e.ICONO_DECISION[dec_shacl]} {p['nombre']:<26} {p['rol']:<11} {dec_shacl}"
          f"   [Python: {'coincide' if dec_shacl == dec_py else 'DISCREPA → ' + dec_py}]")
    for m in viol: print(f"      🚨 {m}"); plan.append((0, p["id"], m))
    for m in avis: print(f"      ⚠️  {m}"); plan.append((1, p["id"], m))

print("\n🔁 VERIFICACIÓN CRUZADA: " + ("la decisión de SHACL coincide con la del rulebook en Python ✅" if coherente
      else "hay discrepancias entre SHACL y el rulebook ❌ (revisa shapes o reglas)"))
print("\n🛠️  PLAN DE REMEDIACIÓN (primero lo que bloquea)\n" + "─" * 70)
for _, pid, m in sorted(plan):
    print(f"   {pid:<20} {m}")
print("\n💡 Las reglas R05–R07 no se declaran: salen de validar lo que el proveedor publica de verdad."
      "\n   Así el rulebook deja de ser un cuestionario de buena fe y pasa a ser una comprobación.")
sys.exit(1 if n_viol else 0)
