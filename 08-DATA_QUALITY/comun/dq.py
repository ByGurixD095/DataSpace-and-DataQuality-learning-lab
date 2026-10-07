# -*- coding: utf-8 -*-
"""
Biblioteca común del laboratorio 08-Data-Quality.

Un único sitio con las piezas que comparten todas las carpetas:

  · CARACTERISTICAS ..... las 15 características de ISO/IEC 25012 (modelo)
  · medidas ............. funciones de medida al estilo ISO/IEC 25024 (ratios cumplen/total)
  · reglas .............. evaluador de reglas de negocio en cuatro niveles (estilo DMN4DQ)
  · DQV ................. construcción de mediciones en RDF (requiere rdflib)

Salvo la parte DQV, solo usa la biblioteca estándar de Python.

⚠️ Es material DIDÁCTICO: ilustra los conceptos de los estándares, no los sustituye.
"""
from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CSV_POR_DEFECTO = RAIZ / "datos" / "lecturas_calidad_aire.csv"
REGLAS_POR_DEFECTO = RAIZ / "05-Reglas-DMN4DQ" / "reglas.json"
# "Ahora" fijo para que todo sea reproducible (se puede cambiar con --ahora)
AHORA_POR_DEFECTO = datetime(2026, 10, 6, 0, 30)
DISTRIBUCION_POR_DEFECTO = "http://example.org/distribucion-calidad-aire-csv"


# ============================================================================
# 1) MODELO: las 15 características de ISO/IEC 25012
# ============================================================================
INH, SIS = "inherente", "sistema"

# (id, nombre ES, nombre EN, perspectivas, definición breve en palabras propias)
CARACTERISTICAS = [
    ("accuracy", "Exactitud", "Accuracy", (INH,),
     "El dato representa correctamente el valor real del atributo que describe."),
    ("completeness", "Completitud", "Completeness", (INH,),
     "Existen valores para todos los atributos y entidades esperados."),
    ("consistency", "Consistencia", "Consistency", (INH,),
     "El dato no se contradice y es coherente con otros datos de su contexto."),
    ("credibility", "Credibilidad", "Credibility", (INH,),
     "Quienes lo usan lo consideran cierto y creíble."),
    ("currentness", "Actualidad", "Currentness", (INH,),
     "El dato tiene la edad adecuada para el uso previsto."),
    ("accessibility", "Accesibilidad", "Accessibility", (INH, SIS),
     "Puede acceder a él quien lo necesita, incluidas personas con necesidades especiales."),
    ("compliance", "Conformidad", "Compliance", (INH, SIS),
     "Cumple las normas, convenciones y regulaciones aplicables."),
    ("confidentiality", "Confidencialidad", "Confidentiality", (INH, SIS),
     "Solo accede a él quien está autorizado."),
    ("efficiency", "Eficiencia", "Efficiency", (INH, SIS),
     "Se puede procesar con las prestaciones adecuadas y recursos razonables."),
    ("precision", "Precisión", "Precision", (INH, SIS),
     "Tiene el nivel de detalle que requiere su uso."),
    ("traceability", "Trazabilidad", "Traceability", (INH, SIS),
     "Se puede auditar quién lo accedió o modificó y de dónde procede."),
    ("understandability", "Comprensibilidad", "Understandability", (INH, SIS),
     "Los usuarios pueden leerlo e interpretarlo (lenguaje, símbolos, unidades)."),
    ("availability", "Disponibilidad", "Availability", (SIS,),
     "Está disponible y se puede recuperar cuando se necesita."),
    ("portability", "Portabilidad", "Portability", (SIS,),
     "Se puede instalar, sustituir o mover entre sistemas conservando su calidad."),
    ("recoverability", "Recuperabilidad", "Recoverability", (SIS,),
     "Mantiene el nivel de calidad incluso ante fallos."),
]
CARACT_POR_ID = {c[0]: c for c in CARACTERISTICAS}


def tipo_perspectiva(persp: tuple) -> str:
    if persp == (INH,):
        return "inherente"
    if persp == (SIS,):
        return "sistema"
    return "mixta"


# ============================================================================
# 2) DATOS
# ============================================================================
def cargar_csv(ruta: Path | str = CSV_POR_DEFECTO) -> list[dict]:
    with open(ruta, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _num(valor: str | None):
    """Convierte a float o devuelve None si está vacío o no es numérico."""
    if valor is None or str(valor).strip() == "":
        return None
    try:
        return float(valor)
    except ValueError:
        return None


def parse_ahora(texto: str | None) -> datetime:
    return datetime.fromisoformat(texto) if texto else AHORA_POR_DEFECTO


# ============================================================================
# 3) MEDIDAS (estilo ISO/IEC 25024): ratio = cumplen / total
# ============================================================================
@dataclass
class Medida:
    id: str
    nombre: str
    caracteristica: str          # id de CARACTERISTICAS
    cumplen: int
    total: int
    descripcion: str

    @property
    def valor(self) -> float:
        return round(self.cumplen / self.total, 6) if self.total else 0.0


def m_completitud(filas, campo="no2") -> Medida:
    ok = sum(1 for f in filas if _num(f.get(campo)) is not None)
    return Medida(f"completitud_{campo}", f"Completitud de {campo.upper()}", "completeness",
                  ok, len(filas), f"Valores de {campo} presentes / filas esperadas")


def m_validez(filas, campo="no2", minimo=0.0, maximo=1000.0) -> Medida:
    ok = sum(1 for f in filas if (v := _num(f.get(campo))) is not None and minimo <= v <= maximo)
    return Medida(f"validez_{campo}", f"Validez de {campo.upper()} ({minimo:g}–{maximo:g})", "accuracy",
                  ok, len(filas), f"Valores de {campo} presentes y dentro de [{minimo:g}, {maximo:g}] / filas")


def m_consistencia_pm(filas) -> Medida:
    ok = sum(1 for f in filas if (a := _num(f.get("pm25"))) is not None
             and (b := _num(f.get("pm10"))) is not None and a <= b)
    return Medida("consistencia_pm", "Consistencia PM2,5 ≤ PM10", "consistency",
                  ok, len(filas), "Filas con PM2,5 ≤ PM10 / filas")


def m_unicidad(filas, claves=("estacion", "fecha_hora")) -> Medida:
    vistos, ok = set(), 0
    for f in filas:
        k = tuple(f.get(c) for c in claves)
        if k not in vistos:
            vistos.add(k)
            ok += 1
    return Medida("unicidad_clave", "Unicidad de (estación, hora)", "consistency",
                  ok, len(filas), "Filas no duplicadas / filas (mapeo habitual a consistencia)")


def m_precision(filas, campo="no2", decimales=1) -> Medida:
    con_valor = [f[campo] for f in filas if _num(f.get(campo)) is not None]
    ok = sum(1 for v in con_valor if "." in v and len(v.split(".")[1]) >= decimales)
    return Medida(f"precision_{campo}", f"Precisión de {campo.upper()} (≥{decimales} decimal)", "precision",
                  ok, len(con_valor), f"Valores con al menos {decimales} decimal / valores presentes")


def m_actualidad(filas, ahora: datetime, horas: int = 24) -> Medida:
    ultima = max(datetime.fromisoformat(f["fecha_hora"]) for f in filas)
    edad_h = (ahora - ultima).total_seconds() / 3600
    return Medida(f"actualidad_{horas}h", f"Actualidad (última lectura ≤ {horas} h)", "currentness",
                  1 if edad_h <= horas else 0, 1,
                  f"¿La última lectura tiene ≤ {horas} h? (edad actual: {edad_h:.1f} h)")


def medir_todo(filas, ahora: datetime | None = None) -> dict[str, Medida]:
    ahora = ahora or AHORA_POR_DEFECTO
    medidas = [m_completitud(filas), m_validez(filas), m_consistencia_pm(filas),
               m_unicidad(filas), m_precision(filas),
               m_actualidad(filas, ahora, 24), m_actualidad(filas, ahora, 3)]
    return {m.id: m for m in medidas}


def barra(valor: float, ancho: int = 20) -> str:
    n = round(valor * ancho)
    return "█" * n + "░" * (ancho - n)


# ============================================================================
# 4) REGLAS DE NEGOCIO en cuatro niveles (estilo DMN4DQ)
#    BR.DV  valores   →  BR.DQM  medición  →  BR.DQA  evaluación  →  BR.DUD  decisión de uso
#    Las reglas viven en un JSON (declarativas): se leen, se discuten y se versionan.
# ============================================================================
def cargar_reglas(ruta: Path | str = REGLAS_POR_DEFECTO) -> dict:
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def _falla_dv(regla: dict, fila: dict, vistos: set) -> bool:
    t = regla["tipo"]
    if t == "rango":                        # el valor debe existir y estar en [min, max]
        v = _num(fila.get(regla["campo"]))
        return v is None or not (regla["min"] <= v <= regla["max"])
    if t == "menor_igual":                  # campo <= contra
        a, b = _num(fila.get(regla["campo"])), _num(fila.get(regla["contra"]))
        return a is None or b is None or a > b
    if t == "unico":                        # la clave no puede repetirse
        k = tuple(fila.get(c) for c in regla["claves"])
        repetido = k in vistos
        vistos.add(k)
        return repetido
    raise ValueError(f"Tipo de regla BR.DV desconocido: {t}")


def evaluar_registros(filas, reglas_dv: list[dict], solo: tuple | None = None):
    """BR.DV: evalúa cada registro. Devuelve (lista de ids fallidos por fila, ratio de registros válidos)."""
    activas = [r for r in reglas_dv if solo is None or r["id"] in solo]
    vistos: set = set()
    fallos = []
    for fila in filas:
        fallos.append([r["id"] for r in activas if _falla_dv(r, fila, vistos)])
    validos = sum(1 for f in fallos if not f)
    return fallos, (round(validos / len(filas), 6) if filas else 0.0)


_OPS = {">=": lambda a, b: a >= b, "<=": lambda a, b: a <= b, ">": lambda a, b: a > b,
        "<": lambda a, b: a < b, "==": lambda a, b: a == b}


def cumple_expr(valor: float | None, expr: str) -> bool:
    m = re.fullmatch(r"\s*(>=|<=|==|>|<)\s*([0-9.]+)\s*", expr)
    if not m or valor is None:
        return False
    return _OPS[m.group(1)](valor, float(m.group(2)))


def evaluar_contexto(valores: dict[str, float], contexto: dict) -> tuple[str, str, dict | None]:
    """BR.DQA + BR.DUD: primera fila de la tabla cuyas condiciones se cumplen (política *first hit*)."""
    for fila in contexto["br_dqa"]:
        if all(cumple_expr(valores.get(m), e) for m, e in fila["si"].items()):
            return fila["nivel"], contexto["br_dud"][fila["nivel"]], fila
    return "Sin nivel", "❓ Ninguna regla aplica", None


def valores_para_reglas(medidas: dict[str, Medida], ratio_registros: float) -> dict[str, float]:
    v = {k: m.valor for k, m in medidas.items()}
    v["registros_validos"] = ratio_registros
    return v


# ============================================================================
# 5) DQV: publicar las mediciones como RDF (requiere rdflib)
# ============================================================================
EX_DQ = "http://example.org/dq#"


def modelo_rdf(g=None):
    """Categorías y dimensiones (las 15 características de ISO/IEC 25012) como DQV + SKOS."""
    from rdflib import Graph, Literal, Namespace, RDF, URIRef
    DQV = Namespace("http://www.w3.org/ns/dqv#")
    SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
    DQ = Namespace(EX_DQ)
    g = g if g is not None else Graph()
    for p, n in (("dqv", DQV), ("skos", SKOS), ("dq", DQ)):
        g.bind(p, n)
    cats = {INH: (DQ["cat-inherente"], "Inherent data quality (ISO/IEC 25012)", "Calidad inherente al dato"),
            SIS: (DQ["cat-sistema"], "System-dependent data quality (ISO/IEC 25012)", "Calidad dependiente del sistema")}
    for uri, en, es in cats.values():
        g.add((uri, RDF.type, DQV.Category)); g.add((uri, RDF.type, SKOS.Concept))
        g.add((uri, SKOS.prefLabel, Literal(en, lang="en"))); g.add((uri, SKOS.prefLabel, Literal(es, lang="es")))
    for cid, es, en, persp, definicion in CARACTERISTICAS:
        d = DQ[f"dim-{cid}"]
        g.add((d, RDF.type, DQV.Dimension)); g.add((d, RDF.type, SKOS.Concept))
        g.add((d, SKOS.prefLabel, Literal(en, lang="en"))); g.add((d, SKOS.prefLabel, Literal(es, lang="es")))
        g.add((d, SKOS.definition, Literal(definicion, lang="es")))
        for p in persp:                      # DQV permite que una dimensión esté en más de una categoría
            g.add((d, DQV.inCategory, cats[p][0]))
    return g


def construir_dqv(medidas: list[Medida], distribucion: str = DISTRIBUCION_POR_DEFECTO,
                  ahora: datetime | None = None, g=None):
    """Una dqv:QualityMeasurement por medida, colgada de la distribución DCAT."""
    from rdflib import Graph, Literal, Namespace, RDF, URIRef, XSD
    DQV = Namespace("http://www.w3.org/ns/dqv#")
    SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
    PROV = Namespace("http://www.w3.org/ns/prov#")
    DQ = Namespace(EX_DQ)
    g = g if g is not None else Graph()
    modelo_rdf(g)
    g.bind("prov", PROV)
    dist = URIRef(distribucion)
    sello = Literal((ahora or AHORA_POR_DEFECTO).isoformat(), datatype=XSD.dateTime)
    for m in medidas:
        met, med = DQ[f"metrica-{m.id}"], DQ[f"medicion-{m.id}"]
        g.add((met, RDF.type, DQV.Metric))
        g.add((met, SKOS.definition, Literal(m.descripcion, lang="es")))
        g.add((met, DQV.expectedDataType, XSD.decimal))
        g.add((met, DQV.inDimension, DQ[f"dim-{m.caracteristica}"]))
        g.add((med, RDF.type, DQV.QualityMeasurement))
        g.add((med, DQV.computedOn, dist))
        g.add((med, DQV.isMeasurementOf, met))
        g.add((med, DQV.value, Literal(f"{m.valor:.4f}", datatype=XSD.decimal)))
        g.add((med, PROV.generatedAtTime, sello))     # una medición sin fecha caduca sin avisar
        g.add((dist, DQV.hasQualityMeasurement, med))
    return g
