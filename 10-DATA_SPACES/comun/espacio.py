# -*- coding: utf-8 -*-
"""
Biblioteca común del laboratorio 10-Data-Spaces.

  · datos ............ participantes, ofertas, rulebook y credenciales revocadas (carpeta datos/)
  · catálogos ........ cada proveedor publica un catálogo DCAT con ofertas ODRL y calidad DQV
  · admisión ......... el rulebook aplicado a cada participante (con reglas DERIVADAS de los metadatos)
  · credenciales ..... credencial de adhesión firmada con Ed25519 (simulada, didáctica)
  · ofertas/acuerdos . evaluación de una petición contra una odrl:Offer y creación del odrl:Agreement

⚠️ Material DIDÁCTICO: simula el ciclo de un espacio de datos. No es una implementación conforme del
Dataspace Protocol ni de ningún protocolo de confianza; la clave de la autoridad sale de una semilla fija
para que todo sea reproducible (en un sistema real NUNCA se hace así).
"""
from __future__ import annotations

import base64
import csv
import hashlib
import json
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATOS = RAIZ / "datos"
AHORA = date(2026, 10, 8)                       # fecha fija: resultados reproducibles
EX_NS = "http://example.org/"
ESP_NS = "http://example.org/espacio#"
AUTORIDAD = "autoridad-espacio"                 # quien emite las credenciales de adhesión
NIVELES = {"Público": "publico", "Interno": "interno", "Confidencial": "confidencial"}


# ============================================================================
# Datos
# ============================================================================
def cargar_csv(nombre: str) -> list[dict]:
    with open(DATOS / nombre, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def participantes() -> list[dict]:
    return cargar_csv("participantes.csv")


def ofertas() -> list[dict]:
    return cargar_csv("ofertas.csv")


def rulebook() -> dict:
    return json.loads((DATOS / "rulebook.json").read_text(encoding="utf-8"))


def revocadas() -> set[str]:
    return set(json.loads((DATOS / "revocadas.json").read_text(encoding="utf-8"))["revocadas"])


def participante(pid: str) -> dict | None:
    return next((p for p in participantes() if p["id"] == pid), None)


# ============================================================================
# RDF: catálogos de los proveedores (requiere rdflib)
# ============================================================================
def _ns():
    from rdflib import Namespace
    return {"EX": Namespace(EX_NS), "ESP": Namespace(ESP_NS),
            "DCAT": Namespace("http://www.w3.org/ns/dcat#"), "DCT": Namespace("http://purl.org/dc/terms/"),
            "ODRL": Namespace("http://www.w3.org/ns/odrl/2/"), "DQV": Namespace("http://www.w3.org/ns/dqv#")}


def _bind(g):
    n = _ns()
    for p, k in (("ex", "EX"), ("esp", "ESP"), ("dcat", "DCAT"), ("dct", "DCT"), ("odrl", "ODRL"), ("dqv", "DQV")):
        g.bind(p, n[k])


def catalogo_rdf(filas: list[dict], proveedor: str, g=None):
    """Catálogo DCAT de UN proveedor: datasets, servicio de acceso, calidad y oferta ODRL (si la tiene)."""
    from rdflib import Graph, Literal, RDF, XSD, BNode
    n = _ns(); EX, ESP, DCAT, DCT, ODRL, DQV = (n[k] for k in ("EX", "ESP", "DCAT", "DCT", "ODRL", "DQV"))
    g = g if g is not None else Graph(); _bind(g)
    cat = EX[f"catalogo-{proveedor}"]
    g.add((cat, RDF.type, DCAT.Catalog)); g.add((cat, DCT.publisher, EX[proveedor]))
    for f in filas:
        if f["proveedor"] != proveedor:
            continue
        ds = EX[f"dataset-{f['id']}"]
        g.add((cat, DCAT.dataset, ds)); g.add((ds, RDF.type, DCAT.Dataset))
        g.add((ds, DCT.title, Literal(f["titulo"], lang="es"))); g.add((ds, DCT.publisher, EX[proveedor]))
        if f["clasificacion"]:
            g.add((ds, ESP.nivelClasificacion, ESP[NIVELES[f["clasificacion"]]]))
        dist, srv = EX[f"distribucion-{f['id']}"], EX[f"servicio-{f['id']}"]
        g.add((ds, DCAT.distribution, dist)); g.add((dist, RDF.type, DCAT.Distribution)); g.add((dist, DCAT.accessService, srv))
        g.add((srv, RDF.type, DCAT.DataService))
        g.add((srv, DCAT.endpointURL, Literal(f["endpoint"], datatype=XSD.anyURI)))
        if f["calidad_completitud"]:
            m = EX[f"medicion-{f['id']}"]
            g.add((m, RDF.type, DQV.QualityMeasurement)); g.add((m, DQV.computedOn, dist))
            g.add((m, DQV.value, Literal(float(f["calidad_completitud"]), datatype=XSD.decimal)))
            g.add((dist, DQV.hasQualityMeasurement, m))
        if f["finalidades"]:
            of = EX[f"oferta-{f['id']}"]
            g.add((ds, ODRL.hasPolicy, of)); g.add((of, RDF.type, ODRL.Offer)); g.add((of, ODRL.uid, of))
            g.add((of, ODRL.assigner, EX[proveedor])); g.add((of, ODRL.target, ds))
            perm, c = BNode(), BNode()
            g.add((of, ODRL.permission, perm)); g.add((perm, ODRL.action, ODRL.use)); g.add((perm, ODRL.constraint, c))
            g.add((c, ODRL.leftOperand, ODRL.purpose)); g.add((c, ODRL.operator, ODRL.isAnyOf))
            for fin in f["finalidades"].split(";"):
                g.add((c, ODRL.rightOperand, Literal(fin)))
            if f["deber_informar"] == "si":
                d = BNode(); g.add((perm, ODRL.duty, d)); g.add((d, ODRL.action, ODRL.inform))
    return g


def catalogos_federados():
    """Un Dataset de rdflib con un GRAFO CON NOMBRE por proveedor: así se sabe de quién viene cada oferta."""
    from rdflib import Dataset, URIRef
    ds = Dataset(); _bind(ds)
    filas = ofertas()
    for prov in sorted({f["proveedor"] for f in filas}):
        catalogo_rdf(filas, prov, ds.graph(URIRef(f"urn:espacio:catalogo:{prov}")))
    return ds


# ============================================================================
# Admisión: el rulebook aplicado
# ============================================================================
def derivados_proveedor(pid: str) -> dict:
    """Reglas que NO se declaran: se calculan de lo que el proveedor realmente publica."""
    mias = [f for f in ofertas() if f["proveedor"] == pid]
    return {"clasificacion_completa": "si" if mias and all(f["clasificacion"] for f in mias) else "no",
            "politicas_odrl": "si" if mias and all(f["finalidades"] for f in mias) else "no",
            "calidad_publicada": "si" if mias and all(f["calidad_completitud"] for f in mias) else "no"}


def aplica(regla: dict, p: dict) -> bool:
    if p["rol"] not in regla["aplica_a"]:
        return False
    cond = regla.get("condicion")
    return not cond or p.get(cond) == "si"


def valor_campo(regla: dict, p: dict) -> str:
    if regla.get("origen") == "derivada":
        return derivados_proveedor(p["id"]).get(regla["campo"], "no")
    return p.get(regla["campo"], "")


def evaluar_participante(p: dict) -> tuple[str, list[tuple[dict, bool]]]:
    res = [(r, valor_campo(r, p) == "si") for r in rulebook()["reglas"] if aplica(r, p)]
    if any(not ok and r["nivel"] == "obligatoria" for r, ok in res):
        return "no admitido", res
    if any(not ok for _, ok in res):
        return "admitido con recomendaciones", res
    return "admitido", res


ICONO_DECISION = {"no admitido": "❌", "admitido con recomendaciones": "⚠️ ", "admitido": "✅"}


# ============================================================================
# Credenciales de adhesión firmadas con Ed25519 (simuladas)
# ============================================================================
def _clave(semilla: str):
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    return Ed25519PrivateKey.from_private_bytes(hashlib.sha256(semilla.encode()).digest())


def clave_autoridad():
    """Clave privada de la autoridad. Sale de una semilla FIJA solo para que el laboratorio sea reproducible."""
    return _clave("semilla-didactica-autoridad-espacio")


def clave_publica_hex(clave) -> str:
    from cryptography.hazmat.primitives import serialization as s
    return clave.public_key().public_bytes(s.Encoding.Raw, s.PublicFormat.Raw).hex()


def _canonico(cred: dict) -> bytes:
    return json.dumps({k: v for k, v in cred.items() if k != "firma"}, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":")).encode()


def firmar(cred: dict, clave) -> dict:
    out = dict(cred)
    out["firma"] = base64.b64encode(clave.sign(_canonico(cred))).decode()
    return out


def emitir_credencial(sujeto: str, clave=None, emisor: str = AUTORIDAD, emitida: date = AHORA,
                      caduca: date | None = None, cred_id: str | None = None, forzar: bool = False) -> dict:
    """La autoridad solo emite a quien el rulebook admite (salvo forzar=True, para fabricar casos de prueba)."""
    p = participante(sujeto)
    if not forzar:
        if p is None:
            raise ValueError(f"«{sujeto}» no es un participante conocido")
        decision, _ = evaluar_participante(p)
        if decision == "no admitido":
            raise PermissionError(f"el rulebook no admite a «{sujeto}»: no se emite credencial")
    caduca = caduca or date(emitida.year + 1, emitida.month, emitida.day)
    cred = {"id": cred_id or f"cred-{sujeto}-001", "tipo": "AdhesionCredential", "emisor": emisor,
            "sujeto": sujeto, "emitida": emitida.isoformat(), "caduca": caduca.isoformat(), "rulebook": "v1"}
    return firmar(cred, clave or clave_autoridad())


def verificar_credencial(cred: dict | None, pub_hex: str | None = None, ahora: date = AHORA) -> tuple[bool, str]:
    """Orden de comprobación: presencia → emisor reconocido → firma → vigencia → revocación."""
    from cryptography.exceptions import InvalidSignature
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    if not cred:
        return False, "no presenta credencial"
    if cred.get("emisor") != AUTORIDAD:
        return False, f"emisor no reconocido («{cred.get('emisor')}»)"
    pub = Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub_hex or clave_publica_hex(clave_autoridad())))
    try:
        pub.verify(base64.b64decode(cred.get("firma", "")), _canonico(cred))
    except (InvalidSignature, ValueError):
        return False, "firma inválida: la credencial no es auténtica o fue manipulada"
    if date.fromisoformat(cred["caduca"]) < ahora:
        return False, f"caducada el {cred['caduca']}"
    if cred["id"] in revocadas():
        return False, "revocada por la autoridad"
    return True, "credencial válida"


# ============================================================================
# Ofertas, evaluación y acuerdos
# ============================================================================
def evaluar_peticion(g, dataset_id: str, finalidad: str) -> tuple[bool, str, list[str]]:
    """Evalúa una petición de uso contra la odrl:Offer del dataset.
    ODRL describe; esto es una demostración mínima de cómo un motor la aplicaría."""
    from rdflib import Literal, URIRef
    n = _ns(); EX, ODRL = n["EX"], n["ODRL"]
    ds = URIRef(EX[f"dataset-{dataset_id}"])
    if (ds, None, None) not in g:
        return False, "el dataset no existe en el catálogo", []
    oferta = next(g.objects(ds, ODRL.hasPolicy), None)
    if oferta is None:
        return False, "el dataset no tiene oferta: nada que negociar", []
    for perm in g.objects(oferta, ODRL.permission):
        if (perm, ODRL.action, ODRL.use) not in g:
            continue
        for c in g.objects(perm, ODRL.constraint):
            if (c, ODRL.leftOperand, ODRL.purpose) in g:
                permitidas = {str(o) for o in g.objects(c, ODRL.rightOperand) if isinstance(o, Literal)}
                if finalidad not in permitidas:
                    return False, f"finalidad «{finalidad}» fuera de la oferta (permitidas: {', '.join(sorted(permitidas))})", []
        deberes = [str(a).split("/")[-1] for d in g.objects(perm, ODRL.duty) for a in g.objects(d, ODRL.action)]
        return True, "la petición cabe en la oferta", deberes
    return False, "la oferta no permite la acción «use»", []


def acuerdo_rdf(g_oferta, dataset_id: str, consumidor: str, finalidad: str, numero: int = 1):
    """Convierte la oferta en un odrl:Agreement: aparece el assignee y la finalidad queda fijada."""
    from rdflib import BNode, Graph, Literal, RDF, URIRef
    n = _ns(); EX, ODRL = n["EX"], n["ODRL"]
    ds = URIRef(EX[f"dataset-{dataset_id}"]); oferta = next(g_oferta.objects(ds, ODRL.hasPolicy))
    a = EX[f"acuerdo-{numero:03d}"]
    g = Graph(); _bind(g)
    g.add((a, RDF.type, ODRL.Agreement)); g.add((a, ODRL.uid, a)); g.add((a, ODRL.target, ds))
    g.add((a, ODRL.assigner, next(g_oferta.objects(oferta, ODRL.assigner)))); g.add((a, ODRL.assignee, EX[consumidor]))
    g.add((a, n["ESP"].derivadoDe, oferta))
    perm, c = BNode(), BNode()
    g.add((a, ODRL.permission, perm)); g.add((perm, ODRL.action, ODRL.use)); g.add((perm, ODRL.constraint, c))
    g.add((c, ODRL.leftOperand, ODRL.purpose)); g.add((c, ODRL.operator, ODRL.eq)); g.add((c, ODRL.rightOperand, Literal(finalidad)))
    for perm_o in g_oferta.objects(oferta, ODRL.permission):
        for d in g_oferta.objects(perm_o, ODRL.duty):
            for act in g_oferta.objects(d, ODRL.action):
                dd = BNode(); g.add((perm, ODRL.duty, dd)); g.add((dd, ODRL.action, act))
    return g
