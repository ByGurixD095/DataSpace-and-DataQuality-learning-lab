#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 DCAT Lab — laboratorio interactivo de 07-DCAT
=================================================

Un recorrido por los tres niveles de la carpeta (DCAT → DCAT-AP → DCAT-AP-ES)
en el que la teoría de los README se convierte en práctica:

  • validas catálogos reales contra las reglas de cada perfil,
  • ves QUÉ cambia al pasar de un perfil a otro (y por qué),
  • migras a mano (con ayuda) un catálogo NTI-RISP 2013 a DCAT-AP-ES,
  • rompes un catálogo a propósito y adivinas qué dirá el validador.

Cada regla del validador es una consulta SPARQL (conecta con 04-SPARQL) y
puede mostrarse junto a su equivalente en SHACL (conecta con 05-SHACL).

Uso:
    python dcat_lab.py                    # menú interactivo
    python dcat_lab.py --recorrido        # recorrido guiado completo
    python dcat_lab.py --migracion        # solo la migración asistida
    python dcat_lab.py --validar f.ttl    # valida un fichero (no interactivo)
    python dcat_lab.py --auto             # sin pausas ni preguntas

Requisitos: Python 3.9+ y rdflib  (pip install rdflib)

⚠️ Las reglas son una versión DIDÁCTICA de los perfiles, basada en lo que se
explica en los README. La fuente de verdad son las especificaciones y las
shapes SHACL oficiales: valida con ellas antes de federar un catálogo real.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import textwrap
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path

try:
    from rdflib import BNode, Graph, Literal, Namespace, URIRef, RDF, XSD
    from rdflib.namespace import DC, DCAT, DCTERMS, FOAF
except ImportError:  # pragma: no cover
    sys.exit("Falta rdflib. Instálalo con:  pip install rdflib")

# ----------------------------------------------------------------------------
# Rutas y espacios de nombres
# ----------------------------------------------------------------------------
BASE = Path(__file__).resolve().parent
EXAMPLES = {
    "dcat": BASE / "01-DCAT" / "ejemplo-dcat.ttl",
    "ap": BASE / "02-DCAT-AP" / "ejemplo-dcat-ap.ttl",
    "nti": BASE / "03-DCAT-AP-ES" / "ejemplo-nti-risp-2013.ttl",
    "es": BASE / "03-DCAT-AP-ES" / "ejemplo-dcat-ap-es.ttl",
}
EXAMPLE_LABELS = {
    "dcat": "🟢 01-DCAT      ejemplo-dcat.ttl",
    "ap": "🟡 02-DCAT-AP   ejemplo-dcat-ap.ttl",
    "nti": "📜 03 (antes)   ejemplo-nti-risp-2013.ttl",
    "es": "🔴 03 (después) ejemplo-dcat-ap-es.ttl",
}

VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")
DCATAP = Namespace("http://data.europa.eu/r5r/")
ODRL = Namespace("http://www.w3.org/ns/odrl/2/")
TIME = Namespace("http://www.w3.org/2006/time#")
NAL = "http://publications.europa.eu/resource/authority/"
IANA = "https://www.iana.org/assignments/media-types/"
SECTOR = "http://datos.gob.es/kos/sector-publico/sector/"
DIR3 = "http://datos.gob.es/recurso/sector-publico/org/Organismo/"
TERRITORIO = "http://datos.gob.es/recurso/sector-publico/territorio/"

PROFILES = {
    "dcat": "🟢 DCAT (W3C)",
    "ap": "🟡 DCAT-AP (Europa)",
    "es": "🔴 DCAT-AP-ES (España)",
}

PFX = """PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
PREFIX dcatap: <http://data.europa.eu/r5r/>
PREFIX odrl: <http://www.w3.org/ns/odrl/2/>
PREFIX time: <http://www.w3.org/2006/time#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
"""

# ----------------------------------------------------------------------------
# Utilidades de terminal (colores, pausas, preguntas)
# ----------------------------------------------------------------------------
if os.name == "nt":  # activa ANSI en consolas de Windows modernas
    os.system("")

USE_COLOR = sys.stdout.isatty() and not os.environ.get("NO_COLOR")
AUTO = False  # modo sin preguntas (se activa con --auto)


def c(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text


def bold(t): return c(t, "1")
def dim(t): return c(t, "2")
def red(t): return c(t, "31")
def green(t): return c(t, "32")
def yellow(t): return c(t, "33")
def blue(t): return c(t, "34")
def magenta(t): return c(t, "35")
def cyan(t): return c(t, "36")


def width() -> int:
    return max(60, min(shutil.get_terminal_size((100, 24)).columns, 96))


def say(text: str = "", indent: int = 0, color=None) -> None:
    if not text:
        print()
        return
    for para in text.split("\n"):
        wrapped = textwrap.fill(para, width() - indent,
                                initial_indent=" " * indent,
                                subsequent_indent=" " * indent) or ""
        print(color(wrapped) if color else wrapped)


def rule_line(char="─") -> None:
    print(dim(char * width()))


def title(text: str) -> None:
    print()
    print(bold(cyan("═" * width())))
    print(bold(cyan(f"  {text}")))
    print(bold(cyan("═" * width())))


def subtitle(text: str) -> None:
    print()
    print(bold(f"▌ {text}"))
    rule_line()


def box(heading: str, body: str, color=cyan) -> None:
    """Recuadro para destacar la TEORÍA frente a la práctica."""
    w = width() - 4
    print(color("┌─ " + heading + " " + "─" * max(1, w - len(heading) - 2) + "┐"))
    for para in body.split("\n"):
        for line in (textwrap.wrap(para, w - 2) or [""]):
            print(color("│ ") + line)
    print(color("└" + "─" * (w + 1) + "┘"))


def pause(msg: str = "Pulsa ENTER para continuar…") -> None:
    if AUTO:
        return
    try:
        input(dim(f"\n  ⏎  {msg} "))
    except EOFError:
        pass
    except KeyboardInterrupt:
        goodbye()


def ask(prompt: str, default: str = "") -> str:
    if AUTO:
        return default
    try:
        ans = input(f"  {prompt} ").strip()
    except EOFError:
        return default
    except KeyboardInterrupt:
        goodbye()
    return ans or default


def confirm(prompt: str, default: bool = True) -> bool:
    if AUTO:
        return default
    hint = "[S/n]" if default else "[s/N]"
    ans = ask(f"{prompt} {hint}", "").lower()
    if not ans:
        return default
    return ans in ("s", "si", "sí", "y", "yes", "1")


def menu(heading: str, options: list[tuple[str, str]], back: str = "Volver") -> str:
    """Devuelve la clave elegida ('0' = volver)."""
    print()
    print(bold(heading))
    for key, label in options:
        print(f"   {cyan(key):>12}  {label}")
    print(f"   {cyan('0'):>12}  {back}")
    valid = {k for k, _ in options} | {"0"}
    while True:
        ans = ask("➤", "0")
        if ans in valid:
            return ans
        print(red("   Opción no válida."))


SCORE = {"hits": 0, "total": 0}


def predict(question: str, truth: bool) -> None:
    """Pide una predicción al usuario y la compara con la realidad."""
    if AUTO:
        return
    ans = confirm(f"🤔 {question}", default=True)
    SCORE["total"] += 1
    if ans == truth:
        SCORE["hits"] += 1
        print(green("   ✔ ¡Acertaste!"))
    else:
        print(yellow("   ✘ No exactamente… ahora lo vemos."))


def goodbye() -> None:
    print()
    if SCORE["total"]:
        print(f"  🎯 Predicciones acertadas: {SCORE['hits']}/{SCORE['total']}")
    print(bold("\n  ¡Hasta la próxima! Sigue con 08-Data-Quality 👋\n"))
    sys.exit(0)


# ----------------------------------------------------------------------------
# Carga de grafos y formato de términos
# ----------------------------------------------------------------------------
def load(path: Path | str) -> Graph:
    g = Graph()
    g.parse(location=path.as_uri(), format="turtle")
    g.bind("dcat", DCAT)
    g.bind("dct", DCTERMS)
    g.bind("dc", DC)
    g.bind("vcard", VCARD)
    g.bind("dcatap", DCATAP)
    g.bind("odrl", ODRL)
    g.bind("time", TIME)
    g.bind("lang", Namespace(NAL + "language/"))
    g.bind("ft", Namespace(NAL + "file-type/"))
    g.bind("lic", Namespace(NAL + "licence/"))
    return g


def fmt(g: Graph, term) -> str:
    """Término en forma corta y legible."""
    if term is None:
        return "—"
    try:
        s = term.n3(g.namespace_manager)
    except Exception:
        s = str(term)
    return s if len(s) <= 70 else s[:67] + "…"


def first(g: Graph, cls):
    xs = sorted(g.subjects(RDF.type, cls), key=str)
    return xs[0] if xs else None


def label(g: Graph, node) -> str:
    """Título legible de un recurso."""
    titles = list(g.objects(node, DCTERMS.title))
    if titles:
        es = [t for t in titles if getattr(t, "language", None) == "es"]
        return str((es or titles)[0])
    return fmt(g, node)


# ----------------------------------------------------------------------------
# Reglas de validación (cada regla = una consulta SPARQL)
# ----------------------------------------------------------------------------
SEV_ORDER = {"ERROR": 3, "WARN": 2, "INFO": 1}
SEV_ICON = {"ERROR": "❌", "WARN": "⚠️ ", "INFO": "ℹ️ "}
SEV_COLOR = {"ERROR": red, "WARN": yellow, "INFO": blue}


@dataclass
class Rule:
    id: str
    title: str
    theory: str          # explicación teórica (lo que dice el README)
    body: str            # consulta SPARQL SELECT ?focus ?detail → violaciones
    levels: dict         # perfil → severidad (si falta, la regla no aplica)
    fix: str
    ref: str = ""
    shacl: str = ""      # equivalente SHACL (opcional)


def missing_body(cls: str, props: list[str]) -> str:
    return f"""SELECT ?focus ?detail WHERE {{
  ?focus a {cls} .
  VALUES ?p {{ {' '.join(props)} }}
  FILTER NOT EXISTS {{ ?focus ?p ?x }}
  BIND(CONCAT("falta ", REPLACE(STR(?p), "^.*[#/]", "")) AS ?detail)
}}"""


def missing_shacl(cls: str, props: list[str]) -> str:
    parts = [f"  sh:property [ sh:path {p} ; sh:minCount 1 ]" for p in props]
    return (f"ex:Shape a sh:NodeShape ;\n  sh:targetClass {cls} ;\n"
            + " ;\n".join(parts) + " .")


def not_in_vocab_body(prop: str, prefix: str, extra: str = "") -> str:
    return f"""SELECT ?focus ?detail WHERE {{
  ?focus {prop} ?v .
  FILTER( isLiteral(?v) || isBlank(?v) || !STRSTARTS(STR(?v), "{prefix}") {extra} )
  BIND(CONCAT("valor: ", IF(isBlank(?v), "(nodo en blanco)", STR(?v))) AS ?detail)
}}"""


RULES: list[Rule] = [
    # ---------------------------------------------------------------- DCAT
    Rule(
        "DCAT-01", "Existe al menos un catálogo",
        "Un grafo DCAT describe recursos DENTRO de un catálogo (dcat:Catalog). "
        "En DCAT base es una buena práctica; en DCAT-AP las clases obligatorias "
        "incluyen el catálogo.",
        """SELECT ?focus ?detail WHERE {
  BIND("(grafo)" AS ?focus) BIND("no hay ningún dcat:Catalog" AS ?detail)
  FILTER NOT EXISTS { ?c a dcat:Catalog }
}""",
        {"dcat": "WARN", "ap": "ERROR", "es": "ERROR"},
        "Declara un recurso `a dcat:Catalog` y enlázalo con dcat:dataset.",
        "07-DCAT/README.md · El modelo mínimo"),
    Rule(
        "DCAT-02", "Todo dataset tiene una forma de acceso",
        "Un dcat:Dataset es la IDEA de los datos; sin distribución (fichero) ni "
        "servicio (API) no se pueden reutilizar. En España (convención de "
        "migración) debe mantenerse al menos una distribución.",
        """SELECT ?focus ?detail WHERE {
  ?focus a dcat:Dataset .
  FILTER NOT EXISTS { ?focus dcat:distribution ?d }
  FILTER NOT EXISTS { ?s dcat:servesDataset ?focus }
  BIND("sin distribución ni servicio" AS ?detail)
}""",
        {"dcat": "WARN", "ap": "WARN", "es": "ERROR"},
        "Añade dcat:distribution (o un dcat:DataService con dcat:servesDataset).",
        "01-DCAT/README.md · Dataset vs Distribution vs DataService"),
    Rule(
        "DCAT-03", "La distribución tiene alguna URL (acceso o descarga)",
        "En DCAT base basta con que la distribución tenga accessURL O downloadURL. "
        "(En DCAT-AP se endurece: ver AP-ACC.)",
        """SELECT ?focus ?detail WHERE {
  ?focus a dcat:Distribution .
  FILTER NOT EXISTS { ?focus dcat:accessURL ?a }
  FILTER NOT EXISTS { ?focus dcat:downloadURL ?d }
  BIND("sin accessURL ni downloadURL" AS ?detail)
}""",
        {"dcat": "WARN"},
        "Añade dcat:accessURL o dcat:downloadURL a la distribución.",
        "01-DCAT/README.md · accessURL vs downloadURL"),
    Rule(
        "DCAT-04", "Las URLs de acceso/descarga van en la Distribution, no en el Dataset",
        "El dataset es abstracto; la forma concreta de obtenerlo (URL) pertenece a "
        "la distribución. Error muy frecuente en catálogos caseros.",
        """SELECT ?focus ?detail WHERE {
  ?focus a dcat:Dataset ; ?p ?u .
  VALUES ?p { dcat:accessURL dcat:downloadURL }
  BIND(CONCAT("URL en el dataset: ", STR(?u)) AS ?detail)
}""",
        {"dcat": "WARN", "ap": "WARN", "es": "WARN"},
        "Mueve la URL a un nodo dcat:Distribution enlazado con dcat:distribution.",
        "01-DCAT/README.md · Errores frecuentes"),
    Rule(
        "DCAT-05", "Dublin Core Elements (dc:language) obsoleto",
        "dc: (Dublin Core Elements) está obsoleto frente a dct: (Terms). En la "
        "migración NTI-RISP → DCAT-AP-ES es el primer ajuste mínimo: dc:language "
        "con literales pasa a dct:language con URIs.",
        """SELECT ?focus ?detail WHERE {
  ?focus dc:language ?v .
  BIND(CONCAT("dc:language ", STR(?v)) AS ?detail)
}""",
        {"dcat": "WARN", "ap": "WARN", "es": "ERROR"},
        "Sustituye dc:language \"es\" por dct:language <.../authority/language/SPA>.",
        "03-DCAT-AP-ES/README.md · Los tres ajustes mínimos"),

    # ------------------------------------------------------------ DCAT-AP
    Rule(
        "AP-CAT", "Catálogo: título, descripción y publicador obligatorios",
        "DCAT-AP exige tres propiedades en el catálogo: dct:title, "
        "dct:description y dct:publisher.",
        missing_body("dcat:Catalog", ["dct:title", "dct:description", "dct:publisher"]),
        {"ap": "ERROR", "es": "ERROR"},
        "Añade la propiedad que falta al dcat:Catalog.",
        "02-DCAT-AP/README.md · Obligatorio, recomendado y opcional",
        missing_shacl("dcat:Catalog", ["dct:title", "dct:description", "dct:publisher"])),
    Rule(
        "AP-DS", "Dataset: título y descripción obligatorios",
        "En DCAT-AP un dataset exige muy poco: título y descripción. "
        "La parte exigente está en los VALORES, no en el número de propiedades.",
        missing_body("dcat:Dataset", ["dct:title", "dct:description"]),
        {"ap": "ERROR", "es": "ERROR"},
        "Añade dct:title y dct:description (ideal: en español e inglés).",
        "02-DCAT-AP/README.md · Propiedades obligatorias",
        missing_shacl("dcat:Dataset", ["dct:title", "dct:description"])),
    Rule(
        "AP-ACC", "Distribución: dcat:accessURL obligatoria",
        "En DCAT basta con downloadURL; DCAT-AP exige accessURL (una URL que da "
        "acceso a la distribución). DCAT-AP-ES mantiene el requisito.",
        """SELECT ?focus ?detail WHERE {
  ?focus a dcat:Distribution .
  FILTER NOT EXISTS { ?focus dcat:accessURL ?a }
  BIND("falta accessURL" AS ?detail)
}""",
        {"ap": "ERROR", "es": "ERROR"},
        "Añade dcat:accessURL (puede coincidir con la downloadURL).",
        "02-DCAT-AP/README.md · Propiedades obligatorias",
        missing_shacl("dcat:Distribution", ["dcat:accessURL"])),
    Rule(
        "AP-AGENT", "Agente (foaf:Agent): foaf:name obligatorio",
        "Si describes al publicador como foaf:Agent en el propio grafo, el "
        "nombre es obligatorio.",
        missing_body("foaf:Agent", ["foaf:name"]),
        {"ap": "ERROR", "es": "ERROR"},
        "Añade foaf:name al agente.",
        "02-DCAT-AP/README.md · Propiedades obligatorias",
        missing_shacl("foaf:Agent", ["foaf:name"])),
    Rule(
        "AP-LANG", "dct:language: URI de la lista europea de idiomas",
        "Es el ejemplo estrella de vocabulario controlado: nada de \"es\" o "
        "\"Español\"; se usa la URI de la lista de idiomas de la UE.",
        not_in_vocab_body("dct:language", NAL + "language/"),
        {"ap": "ERROR", "es": "ERROR"},
        "Usa <http://publications.europa.eu/resource/authority/language/SPA>.",
        "07-DCAT/README.md · Texto libre vs vocabulario controlado",
        "ex:Shape a sh:PropertyShape ;\n  sh:path dct:language ;\n  sh:nodeKind sh:IRI ;\n"
        "  sh:pattern \"^http://publications.europa.eu/resource/authority/language/\" ."),
    Rule(
        "AP-MIME", "dcat:mediaType: URI de IANA",
        "El tipo MIME debe expresarse como URI del registro de IANA, no como "
        "texto libre.",
        not_in_vocab_body("dcat:mediaType", "http", """&& !CONTAINS(STR(?v), "iana.org/assignments/media-types/")"""),
        {"ap": "ERROR", "es": "ERROR"},
        "Usa <https://www.iana.org/assignments/media-types/text/csv>.",
        "02-DCAT-AP/README.md · Vocabularios controlados"),
    Rule(
        "AP-THEME", "dcat:theme: nunca texto libre",
        "El tema debe ser la URI de un concepto de un vocabulario, no una "
        "cadena de texto.",
        """SELECT ?focus ?detail WHERE {
  ?focus dcat:theme ?v . FILTER(isLiteral(?v))
  BIND(CONCAT("texto libre: ", STR(?v)) AS ?detail)
}""",
        {"ap": "ERROR", "es": "ERROR"},
        "Sustituye el literal por una URI de data-theme (UE) o de la taxonomía de sectores (ES).",
        "02-DCAT-AP/README.md · Vocabularios controlados"),
    Rule(
        "AP-THEME-EU", "dcat:theme del vocabulario europeo data-theme",
        "DCAT-AP usa la lista europea de temas (data-theme). OJO: DCAT-AP-ES "
        "usa su propia taxonomía de sectores; por eso aquí es solo un aviso y "
        "conviene comprobar cómo lo resuelven las shapes oficiales y el federador.",
        not_in_vocab_body("dcat:theme", NAL + "data-theme/"),
        {"ap": "WARN"},
        "Usa una URI de <.../authority/data-theme/…> (p. ej. ENVI).",
        "03-DCAT-AP-ES/README.md · Taxonomías españolas"),
    Rule(
        "AP-FORMAT", "dct:format: URI de file-type, no texto ni nodo en blanco",
        "El formato se declara con una URI de la lista europea de tipos de "
        "fichero. El modelo NTI-RISP 2013 usaba un nodo dct:IMT con texto.",
        """SELECT ?focus ?detail WHERE {
  ?focus dct:format ?v . FILTER(isLiteral(?v) || isBlank(?v))
  BIND("formato como texto/nodo en blanco" AS ?detail)
}""",
        {"ap": "WARN", "es": "WARN"},
        "Usa <.../authority/file-type/CSV> + dcat:mediaType de IANA.",
        "03-DCAT-AP-ES/README.md · Diferencias a simple vista"),
    Rule(
        "AP-DS-REC", "Dataset: propiedades recomendadas",
        "DCAT-AP recomienda en el dataset: punto de contacto, palabras clave, "
        "tema, cobertura espacial y temporal, y publicador.",
        missing_body("dcat:Dataset", ["dcat:contactPoint", "dcat:keyword", "dcat:theme",
                                      "dct:spatial", "dct:temporal", "dct:publisher"]),
        {"ap": "WARN", "es": "WARN"},
        "Añade las propiedades recomendadas que falten.",
        "02-DCAT-AP/README.md · Recomendadas en el Dataset"),
    Rule(
        "AP-DIST-REC", "Distribución: descripción, formato y licencia recomendados",
        "Son las tres recomendadas de la distribución. En DCAT-AP-ES la "
        "licencia vive AQUÍ.",
        missing_body("dcat:Distribution", ["dct:description", "dct:format", "dct:license"]),
        {"ap": "WARN", "es": "WARN"},
        "Añade dct:description, dct:format y dct:license a la distribución.",
        "02-DCAT-AP/README.md · Recomendadas en la Distribution"),
    Rule(
        "AP-TEMPORAL", "Cobertura temporal con dcat:startDate / dcat:endDate",
        "dct:temporal usa dct:PeriodOfTime con dcat:startDate y dcat:endDate. "
        "El modelo antiguo usaba la ontología Time (time:Interval).",
        """SELECT ?focus ?detail WHERE {
  ?s dct:temporal ?focus . ?focus time:hasBeginning ?b .
  BIND("usa time:hasBeginning en vez de dcat:startDate" AS ?detail)
}""",
        {"ap": "WARN", "es": "WARN"},
        "Sustituye el time:Interval por dct:PeriodOfTime con dcat:startDate/endDate.",
        "03-DCAT-AP-ES/README.md · Diferencias a simple vista"),
    Rule(
        "AP-SVC-URL", "Servicio de datos: dcat:endpointURL obligatoria",
        "Un dcat:DataService (API, WMS, endpoint SPARQL…) necesita su URL de acceso.",
        missing_body("dcat:DataService", ["dcat:endpointURL"]),
        {"ap": "ERROR", "es": "ERROR"},
        "Añade dcat:endpointURL al servicio.",
        "03-DCAT-AP-ES/README.md · Servicios de datos",
        missing_shacl("dcat:DataService", ["dcat:endpointURL"])),
    Rule(
        "AP-SVC-TITLE", "Servicio de datos: título",
        "En DCAT-AP-ES el título del servicio es obligatorio; en DCAT-AP "
        "(según la versión) es muy recomendable.",
        missing_body("dcat:DataService", ["dct:title"]),
        {"ap": "WARN", "es": "ERROR"},
        "Añade dct:title al servicio.",
        "03-DCAT-AP-ES/README.md · Servicios de datos"),
    Rule(
        "AP-SVC-SERVES", "Servicio de datos: indica qué dataset sirve",
        "dcat:servesDataset enlaza el servicio con los datos que ofrece.",
        missing_body("dcat:DataService", ["dcat:servesDataset"]),
        {"ap": "WARN", "es": "WARN"},
        "Añade dcat:servesDataset apuntando al dataset.",
        "03-DCAT-AP-ES/README.md · Servicios de datos"),

    # --------------------------------------------------------- DCAT-AP-ES
    Rule(
        "ES-SVC", "Servicio de datos: tema y publicador obligatorios (España)",
        "DCAT-AP-ES exige en el servicio: título, endpointURL, tema y "
        "publicador. Aquí se comprueban las dos últimas.",
        missing_body("dcat:DataService", ["dcat:theme", "dct:publisher"]),
        {"es": "ERROR"},
        "Copia dcat:theme y dct:publisher del dataset que sirve.",
        "03-DCAT-AP-ES/README.md · Servicios de datos"),
    Rule(
        "ES-LIC-DS", "La licencia se declara en la distribución, no en el dataset",
        "Segundo ajuste mínimo de la migración: si quieres indicar las "
        "condiciones de uso, dct:license se traslada a cada distribución.",
        """SELECT ?focus ?detail WHERE {
  ?focus a dcat:Dataset ; dct:license ?l .
  BIND(CONCAT("licencia en el dataset: ", STR(?l)) AS ?detail)
}""",
        {"ap": "WARN", "es": "ERROR"},
        "Mueve dct:license del dataset a sus dcat:Distribution.",
        "03-DCAT-AP-ES/README.md · Los tres ajustes mínimos"),
    Rule(
        "ES-IDENT", "Identificador estable del dataset (dct:identifier)",
        "Tercer ajuste mínimo: preservar identificadores estables. Cambiarlos "
        "rompe enlaces y federación.",
        missing_body("dcat:Dataset", ["dct:identifier"]),
        {"ap": "INFO", "es": "ERROR"},
        "Añade dct:identifier con un identificador persistente.",
        "03-DCAT-AP-ES/README.md · Errores frecuentes",
        missing_shacl("dcat:Dataset", ["dct:identifier"])),
    Rule(
        "ES-THEME", "Tema de la taxonomía de sectores de datos.gob.es",
        "En España los temas siguen la taxonomía de sectores primarios "
        "(http://datos.gob.es/kos/sector-publico/sector/…).",
        not_in_vocab_body("dcat:theme", SECTOR),
        {"es": "WARN"},
        "Usa p. ej. <http://datos.gob.es/kos/sector-publico/sector/medio-ambiente>.",
        "03-DCAT-AP-ES/README.md · Taxonomías y identificadores españoles"),
    Rule(
        "ES-PUBLISHER", "Publicador identificado con el código DIR3",
        "El publicador es una URI del catálogo de organismos (DIR3), no un "
        "agente inventado.",
        not_in_vocab_body("dct:publisher", DIR3),
        {"es": "WARN"},
        "Usa <http://datos.gob.es/recurso/sector-publico/org/Organismo/{DIR3}>.",
        "03-DCAT-AP-ES/README.md · Taxonomías y identificadores españoles"),
    Rule(
        "ES-SPATIAL", "Cobertura geográfica con la taxonomía de territorios",
        "Los territorios se identifican con URIs de "
        "http://datos.gob.es/recurso/sector-publico/territorio/…",
        not_in_vocab_body("dct:spatial", TERRITORIO),
        {"es": "WARN"},
        "Usa p. ej. <…/territorio/Pais/España>.",
        "03-DCAT-AP-ES/README.md · Taxonomías y identificadores españoles"),
    Rule(
        "ES-CONTACT", "Punto de contacto como vcard:Organization",
        "El contacto es la «tarjeta de visita» de la institución: un "
        "vcard:Organization con datos institucionales y persistentes.",
        """SELECT ?focus ?detail WHERE {
  ?s dcat:contactPoint ?focus .
  FILTER NOT EXISTS { ?focus a vcard:Organization }
  BIND("el contacto no es un vcard:Organization" AS ?detail)
}""",
        {"es": "WARN"},
        "Declara el contacto como `a vcard:Organization` con vcard:hasEmail.",
        "03-DCAT-AP-ES/README.md · Punto de contacto"),
    Rule(
        "ES-VALID", "Propiedades abandonadas (dct:valid, dct:references)",
        "El modelo antiguo las usaba; DCAT-AP-ES las sustituye por "
        "propiedades más claras.",
        """SELECT ?focus ?detail WHERE {
  ?focus ?p ?v . VALUES ?p { dct:valid dct:references }
  BIND(CONCAT("usa ", REPLACE(STR(?p), "^.*[#/]", "")) AS ?detail)
}""",
        {"es": "WARN"},
        "Sustitúyelas por dct:temporal / dct:relation según el caso.",
        "03-DCAT-AP-ES/README.md · Qué ha cambiado, entidad por entidad"),

    # ------------------------------------------------------------------ HVD
    Rule(
        "HVD-LEG", "HVD: legislación aplicable obligatoria",
        "Un dataset de alto valor (dcatap:hvdCategory) debe indicar la "
        "legislación aplicable (Reglamento de ejecución (UE) 2023/138).",
        """SELECT ?focus ?detail WHERE {
  ?focus dcatap:hvdCategory ?c .
  FILTER NOT EXISTS { ?focus dcatap:applicableLegislation ?l }
  BIND("HVD sin applicableLegislation" AS ?detail)
}""",
        {"es": "ERROR"},
        "Añade dcatap:applicableLegislation con la URI del reglamento.",
        "03-DCAT-AP-ES/README.md · Datos de alto valor (HVD)"),
    Rule(
        "HVD-CONTACT", "HVD: punto de contacto obligatorio",
        "En los datos de alto valor el punto de contacto es obligatorio.",
        """SELECT ?focus ?detail WHERE {
  ?focus dcatap:hvdCategory ?c .
  FILTER NOT EXISTS { ?focus dcat:contactPoint ?k }
  BIND("HVD sin contactPoint" AS ?detail)
}""",
        {"es": "ERROR"},
        "Añade dcat:contactPoint (vcard:Organization con email o URL).",
        "03-DCAT-AP-ES/README.md · Datos de alto valor (HVD)"),
    Rule(
        "HVD-SERVICE", "HVD: debe haber un servicio de datos que lo sirva",
        "Los HVD requieren acceso programático: al menos un dcat:DataService "
        "con dcat:servesDataset.",
        """SELECT ?focus ?detail WHERE {
  ?focus a dcat:Dataset ; dcatap:hvdCategory ?c .
  FILTER NOT EXISTS { ?s dcat:servesDataset ?focus }
  BIND("HVD sin servicio de datos" AS ?detail)
}""",
        {"es": "ERROR"},
        "Describe la API como dcat:DataService y enlázala con dcat:servesDataset.",
        "03-DCAT-AP-ES/README.md · Datos de alto valor (HVD)"),
    Rule(
        "HVD-BULK", "HVD: distribución para descarga masiva",
        "Se recomienda al menos una distribución con dcat:downloadURL "
        "(descarga masiva) para los HVD.",
        """SELECT ?focus ?detail WHERE {
  ?focus a dcat:Dataset ; dcatap:hvdCategory ?c .
  FILTER NOT EXISTS { ?focus dcat:distribution ?d . ?d dcat:downloadURL ?u }
  BIND("HVD sin distribución de descarga masiva" AS ?detail)
}""",
        {"es": "WARN"},
        "Añade una dcat:Distribution con dcat:downloadURL.",
        "03-DCAT-AP-ES/README.md · Datos de alto valor (HVD)"),
]
RULES_BY_ID = {r.id: r for r in RULES}


@dataclass(frozen=True)
class Finding:
    rule_id: str
    sev: str
    focus: str
    detail: str


def run_query(g: Graph, body: str):
    return g.query(PFX + body)


def validate(g: Graph, profile: str) -> list[Finding]:
    out: list[Finding] = []
    for r in RULES:
        sev = r.levels.get(profile)
        if not sev:
            continue
        for row in run_query(g, r.body):
            out.append(Finding(r.id, sev, fmt(g, row.focus),
                               str(row.detail) if row.detail is not None else ""))
    return out


def counts(findings: list[Finding]) -> dict:
    d = {"ERROR": 0, "WARN": 0, "INFO": 0}
    for f in findings:
        d[f.sev] += 1
    return d


def verdict(findings: list[Finding]) -> bool:
    return counts(findings)["ERROR"] == 0


# ----------------------------------------------------------------------------
# Presentación de informes y explicaciones
# ----------------------------------------------------------------------------
def show_report(g: Graph, profile: str, name: str, findings: list[Finding] | None = None,
                interactive: bool = True) -> list[Finding]:
    findings = validate(g, profile) if findings is None else findings
    cnt = counts(findings)
    subtitle(f"Informe · {PROFILES[profile]} · {name}")
    if not findings:
        say("Sin hallazgos: el catálogo cumple todas las reglas de este perfil.", color=green)
    by_rule: dict[str, list[Finding]] = {}
    for f in findings:
        by_rule.setdefault(f.rule_id, []).append(f)
    ordered = sorted(by_rule.items(),
                     key=lambda kv: (-SEV_ORDER[kv[1][0].sev], kv[0]))
    for rid, fs in ordered:
        r = RULES_BY_ID[rid]
        col = SEV_COLOR[fs[0].sev]
        print(f"  {SEV_ICON[fs[0].sev]} {col(bold(rid)):<24} {r.title}")
        for f in fs[:6]:
            print(dim(f"        ↳ {f.focus} — {f.detail}"))
        if len(fs) > 6:
            print(dim(f"        ↳ … y {len(fs) - 6} más"))
    rule_line()
    if cnt["ERROR"]:
        head = red(bold("❌ NO CONFORME"))
    else:
        head = green(bold("✅ CONFORME"))
    print(f"  {head} · {cnt['ERROR']} errores · {cnt['WARN']} avisos · {cnt['INFO']} notas")
    if interactive and findings and not AUTO:
        inspector(g, profile, [rid for rid, _ in ordered])
    return findings


def inspector(g: Graph, profile: str, rule_ids: list[str]) -> None:
    """Bucle: el usuario elige una regla y ve teoría + consulta + SHACL."""
    while True:
        ans = ask(dim("🔍 Escribe el id de una regla para ver su teoría (o ENTER para seguir):"), "")
        if not ans:
            return
        rid = ans.upper()
        if rid not in RULES_BY_ID:
            print(red(f"   No conozco la regla «{ans}». Ids disponibles: {', '.join(rule_ids)}"))
            continue
        explain(g, RULES_BY_ID[rid], profile)


def explain(g: Graph, r: Rule, profile: str | None = None, ask_run: bool = True) -> None:
    sev = r.levels.get(profile) if profile else None
    head = f"📖 {r.id} · {r.title}" + (f"  [{sev} en {PROFILES[profile]}]" if sev else "")
    box(head, r.theory, magenta)
    say(f"🔧 Cómo se arregla: {r.fix}", 2, green)
    if r.ref:
        say(f"📚 Dónde verlo: {r.ref}", 2, dim)
    print()
    print(bold("  🔎 Así lo detecta el script (SPARQL, como en 04-SPARQL):"))
    for line in r.body.splitlines():
        print(cyan("     " + line))
    if r.shacl:
        print()
        print(bold("  🛡️  Y esto mismo en SHACL (como en 05-SHACL):"))
        for line in r.shacl.splitlines():
            print(blue("     " + line))
    if ask_run and not AUTO and confirm("¿Ejecutar la consulta sobre el catálogo y ver las filas?", False):
        show_rows(g, r.body)


def table(headers: list[str], rows: list[list[str]], max_rows: int = 30) -> None:
    if not rows:
        print(dim("   (sin resultados)"))
        return
    shown = rows[:max_rows]
    w = [max(len(str(h)), *(len(str(r[i])) for r in shown)) for i, h in enumerate(headers)]
    w = [min(x, 46) for x in w]
    line = "   " + "  ".join(bold(str(h).ljust(w[i])) for i, h in enumerate(headers))
    print(line)
    print(dim("   " + "  ".join("─" * x for x in w)))
    for r in shown:
        print("   " + "  ".join(str(v)[:w[i]].ljust(w[i]) for i, v in enumerate(r)))
    if len(rows) > max_rows:
        print(dim(f"   … {len(rows) - max_rows} filas más"))


def show_rows(g: Graph, body: str) -> None:
    try:
        res = run_query(g, body)
        heads = [str(v) for v in res.vars]
        rows = [[fmt(g, x) if x is not None else "—" for x in row] for row in res]
        table(heads, rows)
    except Exception as e:  # noqa: BLE001
        print(red(f"   Error en la consulta: {e}"))


# ----------------------------------------------------------------------------
# Radiografía, matriz y diff entre catálogos
# ----------------------------------------------------------------------------
def radiografia(g: Graph, name: str) -> None:
    subtitle(f"Radiografía · {name}")
    classes = [(DCAT.Catalog, "Catalog"), (DCAT.Dataset, "Dataset"),
               (DCAT.Distribution, "Distribution"), (DCAT.DataService, "DataService")]
    resumen = " · ".join(f"{sum(1 for _ in g.subjects(RDF.type, k))} {n}" for k, n in classes)
    print(f"  {len(g)} tripletas · {resumen}")
    print()
    cats = sorted(g.subjects(RDF.type, DCAT.Catalog), key=str)
    for cat in cats:
        print(f"  📚 {bold(label(g, cat))}")
        for ds in sorted(g.objects(cat, DCAT.dataset), key=str):
            print(f"     └─ 🗃️  {label(g, ds)}")
            for d in sorted(g.objects(ds, DCAT.distribution), key=str):
                fmt_ = next(iter(g.objects(d, DCTERMS.format)), None)
                print(f"         └─ 📄 {label(g, d)}" + dim(f"   (formato: {fmt(g, fmt_)})" if fmt_ else ""))
        for sv in sorted(g.objects(cat, DCAT.service), key=str):
            print(f"     └─ 🔌 {label(g, sv)}")
    if not cats:
        print(red("  No hay ningún dcat:Catalog en el grafo."))


def matriz(graphs: dict[str, Graph]) -> None:
    """Semáforo: cada fichero evaluado contra los tres perfiles."""
    subtitle("Semáforo: el mismo fichero cambia de veredicto según el perfil")
    heads = ["Fichero"] + [PROFILES[p].split(" (")[0] for p in PROFILES]
    rows = []
    for key, g in graphs.items():
        row = [EXAMPLE_LABELS.get(key, key)]
        for p in PROFILES:
            cnt = counts(validate(g, p))
            mark = "✅" if cnt["ERROR"] == 0 else "❌"
            row.append(f"{mark} {cnt['ERROR']}E/{cnt['WARN']}A")
        rows.append(row)
    table(heads, rows)
    print(dim("   E = errores · A = avisos"))


KEY_CLASSES = [
    (DCAT.Catalog, "📚 Catalog"), (DCAT.Dataset, "🗃️  Dataset"),
    (DCAT.Distribution, "📄 Distribution"), (DCAT.DataService, "🔌 DataService"),
    (VCARD.Organization, "☎️  vcard:Organization"), (FOAF.Agent, "🏢 foaf:Agent"),
    (DCTERMS.PeriodOfTime, "🗺️  PeriodOfTime"),
]


def kinds_by_class(g: Graph) -> dict:
    res: dict[str, dict] = {}
    for cls, name in KEY_CLASSES:
        for s in g.subjects(RDF.type, cls):
            for p, o in g.predicate_objects(s):
                if p == RDF.type:
                    continue
                kind = "literal" if isinstance(o, Literal) else ("bnode" if isinstance(o, BNode) else "iri")
                res.setdefault(name, {}).setdefault(p, set()).add(kind)
    return res


def diff_graphs(ga: Graph, gb: Graph, na: str, nb: str) -> None:
    subtitle(f"Qué cambia: {na}  →  {nb}")
    ka, kb = kinds_by_class(ga), kinds_by_class(gb)
    total = 0
    for _, name in KEY_CLASSES:
        pa, pb = ka.get(name, {}), kb.get(name, {})
        if not pa and not pb:
            continue
        lines = []
        for p in sorted(set(pb) - set(pa), key=str):
            lines.append(green(f"     ➕ {fmt(gb, p):<26}") + dim(f" ({'/'.join(sorted(pb[p]))})"))
        for p in sorted(set(pa) - set(pb), key=str):
            lines.append(red(f"     ➖ {fmt(ga, p):<26}") + dim(f" ({'/'.join(sorted(pa[p]))})"))
        for p in sorted(set(pa) & set(pb), key=str):
            if pa[p] != pb[p]:
                lines.append(yellow(f"     🔄 {fmt(gb, p):<26}") +
                             dim(f" {'/'.join(sorted(pa[p]))} → {'/'.join(sorted(pb[p]))}"))
        if not pa:
            lines.insert(0, green("     (clase nueva en el segundo catálogo)"))
        if not pb:
            lines.insert(0, red("     (clase que desaparece en el segundo catálogo)"))
        if lines:
            print(f"  {bold(name)}")
            for ln in lines:
                print(ln)
            total += len(lines)
    if not total:
        print(dim("   Los dos catálogos usan las mismas propiedades en cada clase."))
    print(dim("\n   ➕ propiedad nueva · ➖ propiedad que desaparece · 🔄 cambia el tipo de valor"))


# ----------------------------------------------------------------------------
# Migración asistida NTI-RISP 2013 → DCAT-AP-ES
# ----------------------------------------------------------------------------
@dataclass
class Change:
    removed: list = field(default_factory=list)
    added: list = field(default_factory=list)
    notes: list = field(default_factory=list)

    @property
    def empty(self) -> bool:
        return not self.removed and not self.added


LANG_MAP = {"es": "SPA", "en": "ENG", "ca": "CAT", "gl": "GLG", "eu": "EUS",
            "fr": "FRA", "de": "DEU", "it": "ITA", "pt": "POR"}
FILETYPE_MAP = {"text/csv": "CSV", "application/json": "JSON", "application/xml": "XML",
                "text/xml": "XML", "application/pdf": "PDF", "application/zip": "ZIP",
                "application/geo+json": "GEOJSON"}


def bnode_closure(g: Graph, node) -> list:
    """Todas las tripletas de un nodo en blanco (y de los anidados)."""
    out, stack, seen = [], [node], set()
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        for p, o in g.predicate_objects(n):
            out.append((n, p, o))
            if isinstance(o, BNode):
                stack.append(o)
    return out


def apply_change(g: Graph, ch: Change) -> None:
    for t in ch.removed:
        g.remove(t)
    for t in ch.added:
        g.add(t)


def show_change(g_before: Graph, ch: Change) -> None:
    nm = g_before.namespace_manager

    def f(t):
        return " ".join(x.n3(nm) if hasattr(x, "n3") else str(x) for x in t)

    for t in ch.removed[:12]:
        print(red(f"     - {f(t)}"))
    if len(ch.removed) > 12:
        print(dim(f"     … y {len(ch.removed) - 12} más"))
    for t in ch.added[:12]:
        print(green(f"     + {f(t)}"))
    if len(ch.added) > 12:
        print(dim(f"     … y {len(ch.added) - 12} más"))
    for n in ch.notes:
        say(f"ℹ️  {n}", 5, yellow)


def mig_language(g: Graph) -> Change:
    ch = Change()
    for s, o in list(g.subject_objects(DC.language)):
        code = str(o).strip().lower()[:2]
        if code in LANG_MAP:
            ch.removed.append((s, DC.language, o))
            ch.added.append((s, DCTERMS.language, URIRef(NAL + "language/" + LANG_MAP[code])))
        else:
            ch.notes.append(f"Idioma «{o}» sin correspondencia automática: revísalo a mano.")
    return ch


def mig_license(g: Graph) -> Change:
    ch = Change()
    for ds in g.subjects(RDF.type, DCAT.Dataset):
        lics = list(g.objects(ds, DCTERMS.license))
        dists = list(g.objects(ds, DCAT.distribution))
        if not lics:
            continue
        if not dists:
            ch.notes.append(f"{fmt(g, ds)} tiene licencia pero NO tiene distribuciones: "
                            "no se puede trasladar (¡y además incumple DCAT-02!).")
            continue
        for lic in lics:
            for d in dists:
                if (d, DCTERMS.license, lic) not in g:
                    ch.added.append((d, DCTERMS.license, lic))
            ch.removed.append((ds, DCTERMS.license, lic))
    return ch


def mig_minimos(g: Graph) -> Change:
    """Tercer ajuste: ≥1 distribución con accessURL e identificador estable."""
    ch = Change()
    for ds in g.subjects(RDF.type, DCAT.Dataset):
        dists = list(g.objects(ds, DCAT.distribution))
        if not dists:
            ch.notes.append(f"{fmt(g, ds)} no tiene distribuciones: hay que crearlas a mano "
                            "(esto no se puede inventar).")
        for d in dists:
            if not list(g.objects(d, DCAT.accessURL)):
                dl = next(iter(g.objects(d, DCAT.downloadURL)), None)
                if dl is not None:
                    ch.added.append((d, DCAT.accessURL, dl))
                else:
                    ch.notes.append(f"{fmt(g, d)} no tiene ninguna URL: añádela a mano.")
        if not list(g.objects(ds, DCTERMS.identifier)):
            ch.added.append((ds, DCTERMS.identifier, Literal(str(ds))))
    return ch


def mig_format(g: Graph) -> Change:
    ch = Change()
    for d in g.subjects(RDF.type, DCAT.Distribution):
        for node in list(g.objects(d, DCTERMS.format)):
            if not isinstance(node, BNode):
                continue
            mime = next(iter(g.objects(node, RDF.value)), None)
            code = FILETYPE_MAP.get(str(mime).lower()) if mime else None
            if code:
                ch.removed.append((d, DCTERMS.format, node))
                ch.removed.extend(bnode_closure(g, node))
                ch.added.append((d, DCTERMS.format, URIRef(NAL + "file-type/" + code)))
                ch.added.append((d, DCAT.mediaType, URIRef(IANA + str(mime))))
            else:
                ch.notes.append(f"Formato «{mime}» sin correspondencia automática.")
    return ch


def mig_temporal(g: Graph) -> Change:
    ch = Change()
    for s, node in list(g.subject_objects(DCTERMS.temporal)):
        if not isinstance(node, BNode) or (node, TIME.hasBeginning, None) not in g:
            continue

        def instant(prop):
            inst = next(iter(g.objects(node, prop)), None)
            return next(iter(g.objects(inst, TIME.inXSDDateTime)), None) if inst else None

        ini, fin = instant(TIME.hasBeginning), instant(TIME.hasEnd)
        new = BNode()
        ch.removed.append((s, DCTERMS.temporal, node))
        ch.removed.extend(bnode_closure(g, node))
        ch.added.append((s, DCTERMS.temporal, new))
        ch.added.append((new, RDF.type, DCTERMS.PeriodOfTime))
        if ini is not None:
            ch.added.append((new, DCAT.startDate, Literal(str(ini), datatype=XSD.dateTime)))
        if fin is not None:
            ch.added.append((new, DCAT.endDate, Literal(str(fin), datatype=XSD.dateTime)))
    return ch


def mig_contact(g: Graph, email: str, nombre: str) -> Change:
    ch = Change()
    ds = first(g, DCAT.Dataset)
    if ds is None:
        return ch
    pub = next(iter(g.objects(ds, DCTERMS.publisher)), None)
    k = BNode()
    ch.added += [(k, RDF.type, VCARD.Organization),
                 (k, VCARD.fn, Literal(nombre, lang="es")),
                 (k, VCARD.hasEmail, URIRef("mailto:" + email)),
                 (ds, DCAT.contactPoint, k)]
    if isinstance(pub, URIRef):
        ch.added.append((k, VCARD.hasUID, pub))
    return ch


def mig_service(g: Graph, endpoint: str) -> Change:
    ch = Change()
    ds, cat = first(g, DCAT.Dataset), first(g, DCAT.Catalog)
    if ds is None:
        return ch
    sv = URIRef(str(ds) + "-servicio")
    ch.added += [(sv, RDF.type, DCAT.DataService),
                 (sv, DCTERMS.title, Literal(f"Servicio de datos: {label(g, ds)}", lang="es")),
                 (sv, DCAT.endpointURL, URIRef(endpoint)),
                 (sv, DCAT.servesDataset, ds)]
    for th in g.objects(ds, DCAT.theme):
        ch.added.append((sv, DCAT.theme, th))
    for pub in g.objects(ds, DCTERMS.publisher):
        ch.added.append((sv, DCTERMS.publisher, pub))
    for k in g.objects(ds, DCAT.contactPoint):
        ch.added.append((sv, DCAT.contactPoint, k))
    if cat is not None:
        ch.added.append((cat, DCAT.service, sv))
    return ch


def migracion_asistida() -> Graph:
    title("🔄 Migración asistida: NTI-RISP 2013 → DCAT-AP-ES")
    box("🧠 Teoría (03-DCAT-AP-ES)",
        "Si tu catálogo ya cumplía NTI-RISP 2013, el mínimo para migrar son TRES ajustes:\n"
        "  1️⃣ dc:language \"es\"  →  dct:language <…/language/SPA>\n"
        "  2️⃣ la licencia pasa del dataset a la distribución\n"
        "  3️⃣ mantener ≥1 distribución con accessURL e identificadores estables\n"
        "Después, de forma gradual: formato, cobertura temporal, contacto y servicios.")
    g = load(EXAMPLES["nti"])
    original = deepcopy_graph(g)
    radiografia(g, "ejemplo-nti-risp-2013.ttl (el «antes»)")
    pause()

    f0 = show_report(g, "es", "antes de migrar", interactive=True)
    errores0 = counts(f0)["ERROR"]
    say(f"\nPunto de partida: {errores0} errores contra DCAT-AP-ES. "
        "Vamos a hacerlos desaparecer uno a uno.", color=bold)
    pause()

    steps = [
        ("1️⃣  dc:language → dct:language con URIs", mig_language,
         "Las URIs de la lista europea evitan ambigüedades («es», «ES», «Español»…) y "
         "permiten federar sin transformaciones."),
        ("2️⃣  La licencia pasa a la distribución", mig_license,
         "En DCAT-AP la licencia es una propiedad de la distribución: puede haber "
         "ficheros con condiciones distintas dentro del mismo dataset."),
        ("3️⃣  Distribución con accessURL + identificador estable", mig_minimos,
         "Sin accessURL la distribución no es conforme; sin identificador estable se "
         "rompen los enlaces y la federación."),
    ]
    for i, (name, fn, why) in enumerate(steps, 1):
        subtitle(f"Ajuste mínimo {name}")
        box("🧠 Por qué", why, magenta)
        ch = fn(g)
        if ch.empty:
            print(green("\n   ✔ Ya estaba cumplido: no hay nada que cambiar."))
            for n in ch.notes:
                say(f"ℹ️  {n}", 5, yellow)
        else:
            print("\n   Cambios que voy a aplicar sobre el grafo:")
            show_change(g, ch)
            if confirm("\n   ¿Aplicar este ajuste?", True):
                apply_change(g, ch)
            else:
                print(yellow("   Ajuste omitido (verás que el validador lo sigue notando)."))
        fs = validate(g, "es")
        cnt = counts(fs)
        print(f"\n   📉 Errores contra DCAT-AP-ES: {bold(str(cnt['ERROR']))}   "
              f"avisos: {cnt['WARN']}")
        pause()

    subtitle("Resultado de los tres ajustes mínimos")
    show_report(g, "es", "tras los 3 ajustes", interactive=False)
    if verdict(validate(g, "es")):
        print(green("\n   🎉 El catálogo ya es federable. Lo que queda son AVISOS: mejoras graduales."))
    pause()

    # ---- ampliaciones graduales
    subtitle("Ampliaciones graduales (opcionales)")
    say("La guía recomienda una ruta iterativa: arranca con el mínimo y enriquece después. "
        "Elige qué ampliaciones aplicar:")
    ext = [
        ("Formato: nodo dct:IMT → URI file-type + dcat:mediaType", lambda: mig_format(g)),
        ("Cobertura temporal: time:Interval → dct:PeriodOfTime", lambda: mig_temporal(g)),
    ]
    for name, fn in ext:
        ch = fn()
        if ch.empty:
            continue
        print(f"\n   ➕ {bold(name)}")
        show_change(g, ch)
        if confirm("   ¿Aplicar?", True):
            apply_change(g, ch)

    if confirm("\n   ➕ Añadir un punto de contacto institucional (vcard:Organization)?", True):
        nombre = ask("   Nombre de la unidad [Oficina del dato]:", "Oficina del dato")
        email = ask("   Email institucional [datos@example.org]:", "datos@example.org")
        ch = mig_contact(g, email, nombre)
        show_change(g, ch)
        apply_change(g, ch)
    if confirm("\n   ➕ Describir tu API como dcat:DataService?", True):
        url = ask("   URL del endpoint [http://example.org/api/calidad-aire]:",
                  "http://example.org/api/calidad-aire")
        ch = mig_service(g, url)
        show_change(g, ch)
        apply_change(g, ch)

    show_report(g, "es", "migrado", interactive=True)
    diff_graphs(original, g, "antes (NTI-RISP 2013)", "después (DCAT-AP-ES)")

    if not AUTO and confirm("\n💾 ¿Guardar el catálogo migrado como «migrado_dcat_ap_es.ttl»?", False):
        out = Path.cwd() / "migrado_dcat_ap_es.ttl"
        g.serialize(destination=str(out), format="turtle")
        print(green(f"   Guardado en {out}"))
    return g


def deepcopy_graph(g: Graph) -> Graph:
    h = Graph()
    for t in g:
        h.add(t)
    for p, n in g.namespaces():
        h.bind(p, n, override=True)
    return h


# ----------------------------------------------------------------------------
# «Rompe el catálogo»: mutaciones + predicción
# ----------------------------------------------------------------------------
def m_title(g):
    ds = first(g, DCAT.Dataset)
    if ds is None: return "No hay dataset."
    g.remove((ds, DCTERMS.title, None)); return "Quitado dct:title del dataset."


def m_lang(g):
    cat = first(g, DCAT.Catalog)
    if cat is None: return "No hay catálogo."
    g.remove((cat, DCTERMS.language, None)); g.add((cat, DCTERMS.language, Literal("es")))
    return 'Idioma del catálogo cambiado a un literal "es".'


def m_accessurl(g):
    n = 0
    for d in g.subjects(RDF.type, DCAT.Distribution):
        for o in list(g.objects(d, DCAT.accessURL)):
            g.remove((d, DCAT.accessURL, o)); n += 1
    return f"Quitada dcat:accessURL de {n} distribución(es)." if n else \
        "Tu fichero no tenía accessURL: no se ha cambiado nada."


def m_license(g):
    ds = first(g, DCAT.Dataset)
    if ds is None: return "No hay dataset."
    moved = False
    for d in g.objects(ds, DCAT.distribution):
        for lic in list(g.objects(d, DCTERMS.license)):
            g.remove((d, DCTERMS.license, lic)); g.add((ds, DCTERMS.license, lic)); moved = True
    if not moved:
        g.add((ds, DCTERMS.license, URIRef(NAL + "licence/CC_BY_4_0")))
    return "Licencia trasladada de la distribución al dataset."


def m_mime(g):
    for d in g.subjects(RDF.type, DCAT.Distribution):
        g.remove((d, DCAT.mediaType, None)); g.add((d, DCAT.mediaType, Literal("text/csv")))
    return 'dcat:mediaType sustituido por el literal "text/csv".'


def m_publisher(g):
    cat = first(g, DCAT.Catalog)
    if cat is None: return "No hay catálogo."
    g.remove((cat, DCTERMS.publisher, None)); return "Quitado dct:publisher del catálogo."


def m_contact(g):
    n = len(list(g.subject_objects(DCAT.contactPoint)))
    g.remove((None, DCAT.contactPoint, None))
    return f"Quitados {n} dcat:contactPoint."


def m_hvd(g):
    ds = first(g, DCAT.Dataset)
    if ds is None: return "No hay dataset."
    g.add((ds, DCATAP.hvdCategory, URIRef("http://data.europa.eu/bna/c_b7f6a4f3")))
    return "Dataset marcado como dato de alto valor (URI de categoría de ejemplo), sin más."


def m_service(g):
    svs = list(g.subjects(RDF.type, DCAT.DataService))
    if not svs:
        sv = URIRef("http://example.org/api-incompleta")
        g.add((sv, RDF.type, DCAT.DataService))
        g.add((sv, DCTERMS.title, Literal("API incompleta", lang="es")))
        g.add((sv, DCAT.endpointURL, URIRef("http://example.org/api")))
        return "Añadido un servicio con solo título y endpoint."
    for sv in svs:
        g.remove((sv, DCAT.theme, None)); g.remove((sv, DCTERMS.publisher, None))
    return "Quitados dcat:theme y dct:publisher de los servicios de datos."


def m_agent(g):
    ags = list(g.subjects(RDF.type, FOAF.Agent))
    if not ags:
        ag = URIRef("http://example.org/agente-anonimo")
        g.add((ag, RDF.type, FOAF.Agent))
        return "Añadido un foaf:Agent sin nombre."
    for a in ags:
        g.remove((a, FOAF.name, None))
    return "Quitado foaf:name de los agentes."


def m_dc(g):
    ds = first(g, DCAT.Dataset)
    if ds is None: return "No hay dataset."
    g.add((ds, DC.language, Literal("es"))); return 'Añadido dc:language "es" al dataset.'


def m_nodist(g):
    ds = first(g, DCAT.Dataset)
    if ds is None: return "No hay dataset."
    g.remove((ds, DCAT.distribution, None)); return "Quitadas las distribuciones del dataset."


MUTATIONS = [
    ("Quitar el título del dataset", m_title),
    ("Poner el idioma del catálogo como texto libre (\"es\")", m_lang),
    ("Quitar dcat:accessURL de las distribuciones", m_accessurl),
    ("Mover la licencia de la distribución al dataset", m_license),
    ("Poner el tipo MIME como texto libre", m_mime),
    ("Quitar el publicador del catálogo", m_publisher),
    ("Quitar el punto de contacto", m_contact),
    ("Marcar el dataset como dato de alto valor (HVD) sin más", m_hvd),
    ("Dejar el servicio de datos incompleto (sin tema ni publicador)", m_service),
    ("Dejar un foaf:Agent sin nombre", m_agent),
    ("Añadir dc:language (modelo antiguo) al dataset", m_dc),
    ("Quitar las distribuciones del dataset", m_nodist),
]


def pick_profile(prompt="¿Contra qué perfil?") -> str:
    key = menu(prompt, [("1", PROFILES["dcat"]), ("2", PROFILES["ap"]), ("3", PROFILES["es"])], "Cancelar")
    return {"1": "dcat", "2": "ap", "3": "es", "0": ""}[key]


def rompe_catalogo(profile: str | None = None) -> None:
    title("💥 Rompe el catálogo (y adivina qué dirá el validador)")
    box("🎯 Cómo funciona",
        "Eliges un perfil: se carga su catálogo de ejemplo (conforme).\n"
        "Eliges un «destrozo». ANTES de ejecutarlo, apuesta: ¿seguirá siendo conforme?\n"
        "Después verás qué reglas saltan y cómo el MISMO cambio puede ser grave en un "
        "perfil y irrelevante en otro.")
    profile = profile or pick_profile("¿Qué perfil quieres poner a prueba?")
    if not profile:
        return
    src = {"dcat": "dcat", "ap": "ap", "es": "es"}[profile]
    while True:
        g = load(EXAMPLES[src])
        base = validate(g, profile)
        print(green(f"\n   Catálogo base ({EXAMPLE_LABELS[src].strip()}) contra {PROFILES[profile]}: "
                    f"{counts(base)['ERROR']} errores."))
        opts = [(str(i), name) for i, (name, _) in enumerate(MUTATIONS, 1)]
        ans = menu("Elige un destrozo:", opts, "Terminar")
        if ans == "0":
            return
        name, fn = MUTATIONS[int(ans) - 1]
        subtitle(f"Destrozo: {name}")
        # el veredicto real se calcula en una copia, antes de preguntar
        probe = deepcopy_graph(g)
        fn(probe)
        truth = verdict(validate(probe, profile))
        predict(f"¿Seguirá el catálogo CONFORME con {PROFILES[profile]} tras este cambio?", truth)
        what = fn(g)
        print(f"\n   🔧 {what}")
        after = validate(g, profile)
        new = [f for f in after if f not in set(base)]
        if new:
            print(bold("\n   Hallazgos NUEVOS provocados por el cambio:"))
            seen = set()
            for f in new:
                r = RULES_BY_ID[f.rule_id]
                if f.rule_id not in seen:
                    seen.add(f.rule_id)
                    print(f"   {SEV_ICON[f.sev]} {SEV_COLOR[f.sev](bold(f.rule_id))}  {r.title}")
                print(dim(f"        ↳ {f.focus} — {f.detail}"))
        else:
            print(green("\n   No aparece ningún hallazgo nuevo en este perfil."))
        print(("\n   " + (green("✅ Sigue CONFORME") if verdict(after) else red("❌ Ya NO es conforme"))) +
              f" con {PROFILES[profile]}.")
        # misma rotura, los tres perfiles
        print(bold("\n   El mismo catálogo roto, visto por los tres perfiles:"))
        row = []
        for p in PROFILES:
            cnt = counts(validate(g, p))
            row.append([PROFILES[p], ("✅" if cnt["ERROR"] == 0 else "❌"), cnt["ERROR"], cnt["WARN"]])
        table(["Perfil", "OK", "Errores", "Avisos"], row)
        if new and not AUTO:
            inspector(g, profile, sorted({f.rule_id for f in new}))
        if AUTO or not confirm("\n   ¿Otro destrozo?", True):
            return


# ----------------------------------------------------------------------------
# Laboratorio SPARQL
# ----------------------------------------------------------------------------
PRESETS = [
    ("Datasets y sus títulos",
     "SELECT ?dataset ?titulo WHERE { ?dataset a dcat:Dataset ; dct:title ?titulo }"),
    ("Distribuciones SIN licencia",
     "SELECT ?dist WHERE { ?dist a dcat:Distribution . FILTER NOT EXISTS { ?dist dct:license ?l } }"),
    ("Datasets con más de una distribución",
     "SELECT ?dataset (COUNT(?d) AS ?n) WHERE { ?dataset dcat:distribution ?d } "
     "GROUP BY ?dataset HAVING (COUNT(?d) > 1)"),
    ("Propiedades usadas por cada clase",
     "SELECT DISTINCT ?clase ?propiedad WHERE { ?s a ?clase ; ?propiedad ?o . "
     "VALUES ?clase { dcat:Catalog dcat:Dataset dcat:Distribution dcat:DataService } "
     "FILTER(?propiedad != rdf:type) } ORDER BY ?clase ?propiedad"),
    ("Idiomas declarados y si son URI o texto",
     "SELECT ?recurso ?idioma (isIRI(?idioma) AS ?esURI) WHERE { "
     "{ ?recurso dct:language ?idioma } UNION { ?recurso dc:language ?idioma } }"),
    ("Qué formatos y tipos MIME hay",
     "SELECT ?dist ?formato ?mime WHERE { ?dist a dcat:Distribution . "
     "OPTIONAL { ?dist dct:format ?formato } OPTIONAL { ?dist dcat:mediaType ?mime } }"),
]


def choose_graph() -> tuple[Graph, str] | None:
    opts = [(str(i), lbl) for i, (k, lbl) in enumerate(EXAMPLE_LABELS.items(), 1)]
    opts.append(("5", "📂 Otro fichero .ttl (indica la ruta)"))
    ans = menu("¿Sobre qué catálogo?", opts, "Cancelar")
    if ans == "0":
        return None
    if ans == "5":
        path = ask("Ruta del fichero .ttl:", "")
        return load_safe(path)
    key = list(EXAMPLE_LABELS)[int(ans) - 1]
    return load(EXAMPLES[key]), Path(EXAMPLES[key]).name


def load_safe(path: str):
    p = Path(path).expanduser()
    if not p.exists():
        print(red(f"   No encuentro «{path}»."))
        return None
    try:
        return load(p), p.name
    except Exception as e:  # noqa: BLE001
        print(red(f"   No se pudo leer el Turtle: {e}"))
        return None


def laboratorio_sparql() -> None:
    title("🔎 Laboratorio SPARQL sobre catálogos DCAT")
    box("🧠 Idea",
        "Un catálogo DCAT es un grafo RDF, así que se interroga con SPARQL (04-SPARQL). "
        "Todas las reglas del validador son consultas como estas.")
    res = choose_graph()
    if not res:
        return
    g, name = res
    while True:
        opts = [(str(i), q[0]) for i, q in enumerate(PRESETS, 1)]
        opts.append((str(len(PRESETS) + 1), "✍️  Escribir mi propia consulta"))
        ans = menu(f"Consultas sobre {name}:", opts, "Terminar")
        if ans == "0":
            return
        idx = int(ans) - 1
        if idx < len(PRESETS):
            body = PRESETS[idx][1]
        else:
            say("Escribe tu SELECT (los prefijos dcat, dct, dc, foaf, vcard, dcatap, odrl, time, xsd, rdf "
                "ya están declarados). Línea vacía para ejecutar:")
            lines = []
            while True:
                ln = ask("…", "")
                if not ln:
                    break
                lines.append(ln)
            body = "\n".join(lines)
            if not body.strip():
                continue
        print(cyan("\n   " + body.replace("\n", "\n   ")))
        print()
        show_rows(g, body)


# ----------------------------------------------------------------------------
# Catálogo de reglas
# ----------------------------------------------------------------------------
def ver_reglas() -> None:
    title("📚 Catálogo de reglas por perfil")
    p = pick_profile("¿Qué perfil quieres consultar?")
    if not p:
        return
    rows = []
    for r in RULES:
        sev = r.levels.get(p)
        if sev:
            rows.append((SEV_ORDER[sev], r.id, sev, r.title))
    rows.sort(key=lambda x: (-x[0], x[1]))
    table(["Regla", "Severidad", "Qué comprueba"], [[r[1], f"{SEV_ICON[r[2]]}{r[2]}", r[3]] for r in rows], 60)
    say(f"\n{len(rows)} reglas aplican en {PROFILES[p]}.")
    g = load(EXAMPLES[p if p != 'es' else 'es'])
    while True:
        ans = ask(dim("Escribe un id para ver su teoría (ENTER para volver):"), "")
        if not ans:
            return
        if ans.upper() in RULES_BY_ID:
            explain(g, RULES_BY_ID[ans.upper()], p)
        else:
            print(red("   Id desconocido."))


# ----------------------------------------------------------------------------
# Validar un fichero propio
# ----------------------------------------------------------------------------
def validar_fichero(path: str | None = None, perfil: str | None = None) -> int:
    if path is None:
        res = choose_graph()
        if not res:
            return 0
        g, name = res
    else:
        res = load_safe(path)
        if not res:
            return 2
        g, name = res
    radiografia(g, name)
    subtitle("Veredicto por perfil")
    rows = []
    for p in PROFILES:
        cnt = counts(validate(g, p))
        rows.append([PROFILES[p], "✅" if cnt["ERROR"] == 0 else "❌", cnt["ERROR"], cnt["WARN"], cnt["INFO"]])
    table(["Perfil", "OK", "Errores", "Avisos", "Notas"], rows)
    chosen = perfil
    if chosen is None:
        chosen = pick_profile("¿Qué informe detallado quieres ver?")
    if chosen and chosen != "todos":
        show_report(g, chosen, name)
    elif chosen == "todos":
        for p in PROFILES:
            show_report(g, p, name, interactive=False)
    final = "es" if perfil in (None, "todos") else perfil
    return 0 if verdict(validate(g, final if final in PROFILES else "es")) else 1


# ----------------------------------------------------------------------------
# Recorrido guiado
# ----------------------------------------------------------------------------
def recorrido() -> None:
    title("🧪 DCAT Lab · Recorrido guiado")
    say("Vas a ver cómo UN MISMO dataset (la calidad del aire de un ayuntamiento) se describe "
        "en tres niveles cada vez más exigentes, y cómo un validador lo comprueba en cada uno.")
    print()
    print(f"   {green('🟢 DCAT')}  ──▶  {yellow('🟡 DCAT-AP')}  ──▶  {red('🔴 DCAT-AP-ES')}")
    print(dim("   vocabulario base      perfil europeo       perfil español (+ NTI-RISP)"))
    say("\nEn cada etapa habrá teoría (recuadros), práctica (el script trabajando) y, a veces, "
        "una apuesta para ti. Puedes escribir el id de una regla para ver su consulta SPARQL y "
        "su equivalente SHACL.")
    missing = [str(p) for p in EXAMPLES.values() if not p.exists()]
    if missing:
        print(red("\n   Faltan ficheros de ejemplo:\n   " + "\n   ".join(missing)))
        return
    pause("ENTER para empezar…")

    gs = {k: load(p) for k, p in EXAMPLES.items()}

    # --- Etapa 1: DCAT
    title("🟢 Etapa 1 · DCAT: el vocabulario base")
    box("🧠 Teoría (01-DCAT)",
        "DCAT te da las clases (Catalog, Dataset, Distribution, DataService) y las propiedades, "
        "pero casi todo es OPCIONAL. Dos catálogos pueden ser DCAT «válidos» y, aun así, "
        "incompatibles entre sí.")
    radiografia(gs["dcat"], "ejemplo-dcat.ttl")
    pause()
    show_report(gs["dcat"], "dcat", "ejemplo-dcat.ttl")
    say("\nFíjate: con DCAT base casi no hay quejas. Todo lo que ves son buenas prácticas.")
    pause()

    # --- Etapa 2: el mismo fichero contra DCAT-AP
    title("🟡 Etapa 2 · Subimos el listón: DCAT-AP")
    box("🧠 Teoría (02-DCAT-AP)",
        "Un perfil de aplicación toma DCAT y lo ACOTA: propiedades obligatorias, "
        "cardinalidades y vocabularios controlados. Es lo que permite que data.europa.eu "
        "federe catálogos de todos los países.")
    f = validate(gs["dcat"], "ap")
    predict("El MISMO fichero del paso anterior, ¿pasará la validación DCAT-AP?", verdict(f))
    show_report(gs["dcat"], "ap", "ejemplo-dcat.ttl (mismo fichero)", f)
    say("\nEl catálogo no cambió: cambió el listón. Las propiedades obligatorias que faltaban "
        "(descripción y publicador del catálogo, accessURL) son justo las de la tabla del README.")
    pause()

    subtitle("Pasamos al catálogo escrito para DCAT-AP")
    diff_graphs(gs["dcat"], gs["ap"], "01-DCAT", "02-DCAT-AP")
    pause()
    show_report(gs["ap"], "ap", "ejemplo-dcat-ap.ttl")
    say("\n✅ Conforme. Los idiomas, temas y formatos ahora son URIs de listas oficiales: "
        "eso es lo que de verdad cambia entre DCAT y DCAT-AP.")
    pause()

    # --- Etapa 3: España
    title("🔴 Etapa 3 · España: DCAT-AP-ES")
    box("🧠 Teoría (03-DCAT-AP-ES)",
        "DCAT-AP-ES es el perfil español de DCAT-AP (alineado con DCAT-AP 2.1.1 + HVD 2.2.0). "
        "Añade taxonomías nacionales (sectores, territorios, organismos DIR3), exige más "
        "cosas a los servicios de datos y tiene requisitos para datos de alto valor. "
        "Es la evolución del modelo NTI-RISP 2013, y la nueva NTI-RISP lo adoptará como "
        "modelo de referencia (comprueba el estado actual de su tramitación).")
    f = validate(gs["ap"], "es")
    predict("El catálogo que acaba de ser CONFORME con DCAT-AP, ¿lo será también con DCAT-AP-ES?", verdict(f))
    show_report(gs["ap"], "es", "ejemplo-dcat-ap.ttl contra DCAT-AP-ES", f)
    say("\nOjo al contraste: errores = lo que España EXIGE además de Europa (servicio de datos con "
        "tema y publicador). Avisos = convenciones nacionales (DIR3, territorios, sectores).")
    pause()
    diff_graphs(gs["ap"], gs["es"], "02-DCAT-AP", "03-DCAT-AP-ES (después)")
    pause()
    show_report(gs["es"], "es", "ejemplo-dcat-ap-es.ttl")
    pause()

    # --- Etapa 4: migración
    title("📜 Etapa 4 · De dónde venimos: NTI-RISP 2013")
    say("En la práctica casi nadie parte de cero: hay catálogos hechos con la norma de 2013. "
        "Veamos cómo se comportan contra cada perfil.")
    matriz({k: gs[k] for k in ("dcat", "ap", "nti", "es")})
    say("\nLee la matriz por columnas: el catálogo NTI-RISP no tiene problemas contra DCAT base, "
        "tiene alguno contra DCAT-AP y tres errores contra DCAT-AP-ES.")
    pause()
    if confirm("¿Hacemos la migración asistida paso a paso?", True):
        migracion_asistida()
        pause()

    # --- Etapa 5: romper
    title("💥 Etapa 5 · Aprende rompiendo cosas")
    if confirm("¿Jugamos a romper un catálogo y adivinar qué dirá el validador?", True):
        rompe_catalogo("ap")

    # --- Cierre
    title("🏁 Resumen")
    matriz(gs)
    box("🧠 Lo que te llevas",
        "• DCAT describe; los PERFILES acotan. El mismo catálogo cambia de veredicto según el perfil.\n"
        "• DCAT-AP convierte «texto libre» en URIs de vocabularios controlados.\n"
        "• DCAT-AP-ES añade taxonomías nacionales, servicios de datos y requisitos HVD.\n"
        "• Migrar desde NTI-RISP 2013 empieza por tres ajustes mínimos y sigue de forma gradual.\n"
        "• Una regla de validación es una consulta SPARQL (04) o una shape SHACL (05).")
    if SCORE["total"]:
        say(f"🎯 Tus predicciones: {SCORE['hits']}/{SCORE['total']} aciertos.")
    say("\nPara seguir: valida TU catálogo (opción 5 del menú) o pasa a 08-Data-Quality, donde la "
        "calidad de los metadatos es un caso práctico de calidad del dato.")


# ----------------------------------------------------------------------------
# Menú principal
# ----------------------------------------------------------------------------
def main_menu() -> None:
    title("🧪 DCAT Lab — 07-DCAT")
    say("Laboratorio interactivo para DCAT, DCAT-AP y DCAT-AP-ES.")
    while True:
        k = menu("¿Qué quieres hacer?", [
            ("1", "🧭 Recorrido guiado completo (recomendado la primera vez)"),
            ("2", "🔄 Migración asistida NTI-RISP 2013 → DCAT-AP-ES"),
            ("3", "💥 Rompe el catálogo y adivina qué dirá el validador"),
            ("4", "🔀 Compara dos catálogos (qué cambia entre perfiles)"),
            ("5", "✅ Valida un catálogo (los de ejemplo o el tuyo)"),
            ("6", "📚 Explora las reglas de cada perfil (teoría + SPARQL + SHACL)"),
            ("7", "🔎 Laboratorio SPARQL"),
            ("8", "🚦 Semáforo: 4 catálogos × 3 perfiles"),
        ], "Salir")
        if k == "0":
            goodbye()
        elif k == "1":
            recorrido()
        elif k == "2":
            migracion_asistida()
        elif k == "3":
            rompe_catalogo()
        elif k == "4":
            comparar()
        elif k == "5":
            validar_fichero()
        elif k == "6":
            ver_reglas()
        elif k == "7":
            laboratorio_sparql()
        elif k == "8":
            matriz({k_: load(p) for k_, p in EXAMPLES.items()})
            pause()


def comparar() -> None:
    k = menu("¿Qué comparación?", [
        ("1", "🟢 DCAT  →  🟡 DCAT-AP"),
        ("2", "🟡 DCAT-AP  →  🔴 DCAT-AP-ES"),
        ("3", "📜 NTI-RISP 2013  →  🔴 DCAT-AP-ES"),
    ], "Volver")
    pairs = {"1": ("dcat", "ap"), "2": ("ap", "es"), "3": ("nti", "es")}
    if k == "0":
        return
    a, b = pairs[k]
    diff_graphs(load(EXAMPLES[a]), load(EXAMPLES[b]),
                EXAMPLE_LABELS[a].strip().split("  ")[0], EXAMPLE_LABELS[b].strip().split("  ")[0])
    pause()


def main() -> None:
    global AUTO
    ap = argparse.ArgumentParser(description="Laboratorio interactivo de DCAT, DCAT-AP y DCAT-AP-ES")
    ap.add_argument("--recorrido", action="store_true", help="recorrido guiado completo")
    ap.add_argument("--migracion", action="store_true", help="migración asistida NTI-RISP → DCAT-AP-ES")
    ap.add_argument("--validar", metavar="FICHERO", help="valida un fichero .ttl (no interactivo)")
    ap.add_argument("--perfil", choices=["dcat", "ap", "es", "todos"], default="es",
                    help="perfil para --validar (por defecto: es)")
    ap.add_argument("--auto", action="store_true", help="sin pausas ni preguntas (usa valores por defecto)")
    args = ap.parse_args()
    AUTO = args.auto or bool(args.validar)

    try:
        if args.validar:
            sys.exit(validar_fichero(args.validar, args.perfil))
        elif args.recorrido:
            recorrido()
        elif args.migracion:
            migracion_asistida()
        else:
            main_menu()
    except KeyboardInterrupt:
        goodbye()


if __name__ == "__main__":
    main()