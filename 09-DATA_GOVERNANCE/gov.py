# -*- coding: utf-8 -*-
"""
Biblioteca común del laboratorio 09-Data-Governance.

  · inventario .......... CSV con el gobierno de cada dataset (¡con huecos a propósito!)
  · vocabulario_rdf ..... roles de gobierno y esquema de clasificación como SKOS
  · catalogo_rdf ........ el inventario convertido en un catálogo DCAT con su gobierno visible
  · cobertura ........... indicadores de cobertura de gobierno calculados con SPARQL
  · politicas ........... políticas ODRL por nivel de clasificación + un evaluador mínimo

Los roles se asignan a UNIDADES o CARGOS, nunca a personas: así el registro sobrevive a la rotación
y no expone datos personales.

⚠️ Material DIDÁCTICO: ilustra los conceptos, no sustituye a las normas ni a una herramienta de gobierno.
"""
from __future__ import annotations

import csv
import re
import unicodedata
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
INVENTARIO = RAIZ / "datos" / "inventario_datasets.csv"
GLOSARIO = RAIZ / "datos" / "glosario.csv"
AHORA_POR_DEFECTO = date(2026, 10, 8)          # fecha fija para que todo sea reproducible

EX_NS = "http://example.org/"
GOV_NS = "http://example.org/gobierno#"
ROLES = [("propietario", "Propietario del dato", "Data owner"),
         ("steward", "Responsable de dominio (steward)", "Data steward"),
         ("custodio", "Custodio técnico", "Data custodian")]
CLASIFICACION = [("publico", "Público", "Public"),
                 ("interno", "Interno", "Internal"),
                 ("confidencial", "Confidencial", "Confidential")]
CLASIF_POR_NOMBRE = {es: cid for cid, es, _ in CLASIFICACION}


def slug(texto: str) -> str:
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def cargar_csv(ruta: Path | str) -> list[dict]:
    with open(ruta, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def cargar_inventario(ruta: Path | str = INVENTARIO) -> list[dict]:
    return cargar_csv(ruta)


def parse_fecha(texto: str | None) -> date:
    return date.fromisoformat(texto) if texto else AHORA_POR_DEFECTO


def barra(valor: float, ancho: int = 20) -> str:
    n = round(valor * ancho)
    return "█" * n + "░" * (ancho - n)


# ============================================================================
# RDF: vocabulario y catálogo gobernado  (requieren rdflib)
# ============================================================================
def _ns():
    from rdflib import Namespace
    return {"EX": Namespace(EX_NS), "GOV": Namespace(GOV_NS),
            "DCAT": Namespace("http://www.w3.org/ns/dcat#"),
            "DCT": Namespace("http://purl.org/dc/terms/"),
            "PROV": Namespace("http://www.w3.org/ns/prov#"),
            "SKOS": Namespace("http://www.w3.org/2004/02/skos/core#"),
            "ODRL": Namespace("http://www.w3.org/ns/odrl/2/"),
            "DQV": Namespace("http://www.w3.org/ns/dqv#")}


def _bind(g):
    n = _ns()
    for p, k in (("ex", "EX"), ("gov", "GOV"), ("dcat", "DCAT"), ("dct", "DCT"), ("prov", "PROV"),
                 ("skos", "SKOS"), ("odrl", "ODRL"), ("dqv", "DQV")):
        g.bind(p, n[k])


def vocabulario_rdf(g=None):
    """Roles de gobierno y esquema de clasificación como SKOS."""
    from rdflib import Graph, Literal, RDF
    n = _ns(); GOV, SKOS = n["GOV"], n["SKOS"]
    g = g if g is not None else Graph(); _bind(g)
    for rid, es, en in ROLES:
        c = GOV[f"rol-{rid}"]
        g.add((c, RDF.type, SKOS.Concept))
        g.add((c, SKOS.prefLabel, Literal(es, lang="es"))); g.add((c, SKOS.prefLabel, Literal(en, lang="en")))
    esq = GOV["esquema-clasificacion"]
    g.add((esq, RDF.type, SKOS.ConceptScheme))
    g.add((esq, SKOS.prefLabel, Literal("Clasificación de la información", lang="es")))
    for cid, es, en in CLASIFICACION:
        c = GOV[cid]
        g.add((c, RDF.type, SKOS.Concept)); g.add((c, SKOS.inScheme, esq))
        g.add((c, SKOS.prefLabel, Literal(es, lang="es"))); g.add((c, SKOS.prefLabel, Literal(en, lang="en")))
    return g


def catalogo_rdf(filas: list[dict], g=None):
    """Convierte el inventario en un catálogo DCAT con roles (PROV), clasificación, política y calidad."""
    from rdflib import Graph, Literal, RDF, URIRef, XSD, BNode
    n = _ns(); EX, GOV, DCAT, DCT, PROV, ODRL, DQV = (n[k] for k in ("EX", "GOV", "DCAT", "DCT", "PROV", "ODRL", "DQV"))
    g = g if g is not None else Graph(); _bind(g)
    vocabulario_rdf(g)
    cat = EX["catalogo-municipal"]
    g.add((cat, RDF.type, DCAT.Catalog)); g.add((cat, DCT.title, Literal("Catálogo de datos del Ayuntamiento", lang="es")))
    for f in filas:
        ds = EX[f"dataset-{f['id']}"]
        g.add((cat, DCAT.dataset, ds)); g.add((ds, RDF.type, DCAT.Dataset))
        g.add((ds, DCT.title, Literal(f["titulo"], lang="es")))
        g.add((ds, DCT.publisher, EX["ayuntamiento"]))
        g.add((ds, GOV.dominio, Literal(f["dominio"], lang="es")))
        for rid, _, _ in ROLES:
            if f.get(rid):
                att = BNode()
                g.add((ds, PROV.qualifiedAttribution, att)); g.add((att, RDF.type, PROV.Attribution))
                g.add((att, PROV.agent, EX[f"unidad-{slug(f[rid])}"])); g.add((att, DCAT.hadRole, GOV[f"rol-{rid}"]))
        if f.get("clasificacion"):
            g.add((ds, GOV.nivelClasificacion, GOV[CLASIF_POR_NOMBRE[f["clasificacion"]]]))
        if f.get("proxima_revision"):
            g.add((ds, GOV.proximaRevision, Literal(f["proxima_revision"], datatype=XSD.date)))
        dist = EX[f"distribucion-{f['id']}"]
        g.add((ds, DCAT.distribution, dist)); g.add((dist, RDF.type, DCAT.Distribution))
        if f.get("politica_uso") == "si":
            g.add((ds, ODRL.hasPolicy, EX[f"politica-{f['id']}"]))
        if f.get("calidad_evaluada") == "si":
            m = EX[f"medicion-{f['id']}-completitud"]
            g.add((m, RDF.type, DQV.QualityMeasurement)); g.add((m, DQV.computedOn, dist))
            g.add((dist, DQV.hasQualityMeasurement, m))
    return g


# ============================================================================
# Indicadores de cobertura (SPARQL)
# ============================================================================
PFX = """PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX dqv: <http://www.w3.org/ns/dqv#>
PREFIX odrl: <http://www.w3.org/ns/odrl/2/>
PREFIX gov: <http://example.org/gobierno#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""


def indicadores(ahora: date) -> list[tuple[str, str, str]]:
    """(id, nombre, consulta que devuelve ?d con los datasets que CUMPLEN el indicador)."""
    def rol(r): return f"?d prov:qualifiedAttribution/dcat:hadRole gov:rol-{r} ."
    return [
        ("propietario", "Con propietario", "SELECT DISTINCT ?d WHERE { ?d a dcat:Dataset . " + rol("propietario") + " }"),
        ("steward", "Con steward", "SELECT DISTINCT ?d WHERE { ?d a dcat:Dataset . " + rol("steward") + " }"),
        ("custodio", "Con custodio técnico", "SELECT DISTINCT ?d WHERE { ?d a dcat:Dataset . " + rol("custodio") + " }"),
        ("clasificacion", "Clasificados", "SELECT DISTINCT ?d WHERE { ?d a dcat:Dataset ; gov:nivelClasificacion ?c }"),
        ("politica", "Con política de uso (ODRL)", "SELECT DISTINCT ?d WHERE { ?d a dcat:Dataset ; odrl:hasPolicy ?p }"),
        ("calidad", "Con calidad evaluada (DQV)", "SELECT DISTINCT ?d WHERE { ?d a dcat:Dataset ; dcat:distribution/dqv:hasQualityMeasurement ?m }"),
        ("revision", f"Con revisión vigente (≥ {ahora})",
         f'SELECT DISTINCT ?d WHERE {{ ?d a dcat:Dataset ; gov:proximaRevision ?r . FILTER(?r >= "{ahora.isoformat()}"^^xsd:date) }}'),
    ]


def cobertura(g, ahora: date = AHORA_POR_DEFECTO) -> list[dict]:
    total = len(todos_los_datasets(g))
    out = []
    for iid, nombre, q in indicadores(ahora):
        cumplen = {str(r.d) for r in g.query(PFX + q)}
        out.append({"id": iid, "nombre": nombre, "cumplen": len(cumplen), "total": total,
                    "valor": round(len(cumplen) / total, 6) if total else 0.0, "datasets": cumplen})
    return out


def todos_los_datasets(g) -> set[str]:
    return {str(r.d) for r in g.query(PFX + "SELECT DISTINCT ?d WHERE { ?d a dcat:Dataset }")}


# ============================================================================
# Políticas ODRL por clasificación + evaluador mínimo
# ============================================================================
def politicas_rdf(g=None):
    """Una política ODRL por nivel de clasificación.
    OJO: gov:tipoSolicitante es un leftOperand PROPIO (no existe en ODRL core): un conector real
    necesitaría un perfil que lo defina y una función que sepa evaluarlo."""
    from rdflib import Graph, Literal, RDF, BNode
    n = _ns(); EX, GOV, ODRL = n["EX"], n["GOV"], n["ODRL"]
    g = g if g is not None else Graph(); _bind(g)

    def regla(pol, tipo, accion, solo_interno=False, duty=None):
        r = BNode(); g.add((pol, ODRL[tipo], r)); g.add((r, ODRL.action, ODRL[accion]))
        if solo_interno:
            c = BNode(); g.add((r, ODRL.constraint, c))
            g.add((c, ODRL.leftOperand, GOV.tipoSolicitante)); g.add((c, ODRL.operator, ODRL.eq))
            g.add((c, ODRL.rightOperand, Literal("interno")))
        if duty:
            d = BNode(); g.add((r, ODRL.duty, d)); g.add((d, ODRL.action, ODRL[duty]))

    for cid, es, _ in CLASIFICACION:
        p = EX[f"politica-nivel-{cid}"]
        g.add((p, RDF.type, ODRL.Set)); g.add((p, ODRL.uid, p))
        g.add((p, GOV.aplicaANivel, GOV[cid]))
        if cid == "publico":
            regla(p, "permission", "use"); regla(p, "permission", "distribute")
        elif cid == "interno":
            regla(p, "permission", "use", solo_interno=True); regla(p, "prohibition", "distribute")
        else:  # confidencial
            regla(p, "permission", "use", solo_interno=True, duty="inform"); regla(p, "prohibition", "distribute")
    return g


def evaluar(g_pol, nivel: str | None, accion: str, solicitante: str) -> tuple[bool, str, list[str]]:
    """Evaluación mínima: prohibición ⇒ deniega; permiso con restricciones cumplidas ⇒ permite; si no, deniega.
    ODRL describe; esto es solo una demostración de cómo un motor podría aplicar la política."""
    from rdflib import Literal
    n = _ns(); GOV, ODRL = n["GOV"], n["ODRL"]
    if not nivel:
        return False, "sin clasificación → denegado por defecto (lo no clasificado no se comparte)", []
    pol = next((p for p in g_pol.subjects(GOV.aplicaANivel, GOV[nivel])), None)
    if pol is None:
        return False, f"no hay política para el nivel «{nivel}»", []
    act = ODRL[accion]
    for pr in g_pol.objects(pol, ODRL.prohibition):
        if (pr, ODRL.action, act) in g_pol:
            return False, "prohibido por la política del nivel", []
    for pe in g_pol.objects(pol, ODRL.permission):
        if (pe, ODRL.action, act) not in g_pol:
            continue
        ok = True
        for c in g_pol.objects(pe, ODRL.constraint):
            if (c, ODRL.leftOperand, GOV.tipoSolicitante) in g_pol:
                esperado = next(g_pol.objects(c, ODRL.rightOperand))
                ok &= isinstance(esperado, Literal) and str(esperado) == solicitante
        if ok:
            deberes = [str(a).split("/")[-1] for d in g_pol.objects(pe, ODRL.duty) for a in g_pol.objects(d, ODRL.action)]
            return True, "permitido por la política del nivel", deberes
        return False, "el permiso existe pero no se cumplen sus restricciones", []
    return False, "ningún permiso aplica → denegado por defecto", []
