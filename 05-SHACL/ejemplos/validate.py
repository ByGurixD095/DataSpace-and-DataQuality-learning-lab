"""
Valida los ejemplos de 05-SHACL con pyshacl.

Uso:
    pip install pyshacl rdflib
    python validate.py                 # ejecuta los tres niveles
    python validate.py 02              # solo el nivel cuyo nombre empieza por 02
"""
import re
import sys
from collections import Counter
from pathlib import Path

from pyshacl import validate
from rdflib import Graph, Namespace

SH = Namespace("http://www.w3.org/ns/shacl#")
BASE = Path(__file__).parent


def short(term):
    """ex:Bob en vez de http://example.com/Bob."""
    return str(term).rsplit("/", 1)[-1].rsplit("#", 1)[-1] if term else "-"


def run(level_dir: Path, data_file: str):
    shapes = Graph().parse(level_dir / "shapes.ttl")
    data = Graph().parse(level_dir / data_file)

    conforms, report, _ = validate(
        data,
        shacl_graph=shapes,
        advanced=True,          # necesario para sh:sparql (SHACL-SPARQL)
        allow_warnings=False,   # los Warning/Info también cuentan como resultado
        inference="none",
    )
    results = list(report.subjects(SH.resultSeverity, None))
    print(f"\n  {data_file:<14} conforms = {conforms}   ({len(results)} resultados)")

    severities, dimensions = Counter(), Counter()
    for r in results:
        severity = short(report.value(r, SH.resultSeverity))
        message = str(report.value(r, SH.resultMessage) or "")
        node = short(report.value(r, SH.focusNode))
        path = short(report.value(r, SH.resultPath))
        severities[severity] += 1
        match = re.match(r"\[(.+?)\]", message)
        if match:
            dimensions[match.group(1)] += 1
        print(f"    {severity:<9} {node:<10} {path:<12} {message}")

    if severities:
        print("    → por severidad:", dict(severities))
    if dimensions:
        print("    → por dimensión ISO 25012:", dict(dimensions))


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else ""
    levels = sorted(p for p in BASE.iterdir() if p.is_dir() and p.name.startswith(only))
    for level in levels:
        print(f"\n=== {level.name} " + "=" * (50 - len(level.name)))
        for data_file in ("valid.ttl", "invalid.ttl"):
            run(level, data_file)


if __name__ == "__main__":
    main()
