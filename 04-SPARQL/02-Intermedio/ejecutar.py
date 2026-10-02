"""
Ejecuta consultas SPARQL sobre datos/personas-libros.ttl usando rdflib.

Uso:
    python ejecutar.py                              # ejecuta todas las consultas de consultas/
    python ejecutar.py consultas/03-filter-numerico.rq
    python ejecutar.py mi_consulta.rq otra.rq

Requisito:
    pip install rdflib
"""
import sys
from pathlib import Path

from rdflib import Graph

BASE = Path(__file__).parent
DATOS = BASE / "datos" / "personas-libros.ttl"


def mostrar(nombre: str, consulta: str, grafo: Graph) -> None:
    print("=" * 70)
    print(f"📄 {nombre}")
    print("=" * 70)
    print(consulta.strip(), "\n")

    resultado = grafo.query(consulta)
    variables = [str(v) for v in resultado.vars]
    filas = [
        ["-" if celda is None else str(celda).replace("http://example.org/", "ex:")
         for celda in fila]
        for fila in resultado
    ]

    anchos = [max(len(v), *(len(f[i]) for f in filas)) if filas else len(v)
              for i, v in enumerate(variables)]
    linea = " | ".join(v.ljust(anchos[i]) for i, v in enumerate(variables))
    print(linea)
    print("-+-".join("-" * a for a in anchos))
    for fila in filas:
        print(" | ".join(c.ljust(anchos[i]) for i, c in enumerate(fila)))
    print(f"\n→ {len(filas)} resultado(s)\n")


def main() -> None:
    grafo = Graph()
    grafo.parse(DATOS, format="turtle")
    print(f"Grafo cargado: {len(grafo)} triples\n")

    if len(sys.argv) > 1:
        archivos = [Path(a) for a in sys.argv[1:]]
    else:
        archivos = sorted((BASE / "consultas").glob("*.rq"))

    for archivo in archivos:
        mostrar(archivo.name, archivo.read_text(encoding="utf-8"), grafo)


if __name__ == "__main__":
    main()
