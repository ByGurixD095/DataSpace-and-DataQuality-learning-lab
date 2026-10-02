"""
Carga ontologia.ttl + datos.ttl, aplica razonamiento RDFS/OWL-RL y ejecuta consultas SPARQL.

    pip install rdflib owlrl
    python ejecutar.py 02-Caso-Practico                      # todas las consultas, CON inferencia
    python ejecutar.py 02-Caso-Practico --sin-inferencia     # SIN inferencia (compara resultados)
    python ejecutar.py 02-Caso-Practico 03-relacionados.rq   # una consulta concreta
    python ejecutar.py 01-RDF-RDFS-OWL-SPARQL
"""
import sys
from pathlib import Path

import owlrl
from rdflib import Graph

BASE = Path(__file__).parent
corto = lambda x: str(x).replace("http://example.org/", "ex:").replace(
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#", "rdf:")


def cargar(carpeta: Path, inferir: bool) -> Graph:
    g = Graph()
    for archivo in ("ontologia.ttl", "datos.ttl"):
        g.parse(carpeta / archivo, format="turtle")
    antes = len(g)
    if inferir:
        owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)
    print(f"Triples: {antes} originales" + (f" → {len(g)} tras la inferencia (RDFS + OWL-RL)\n" if inferir
                                            else " (sin inferencia)\n"))
    return g


def ejecutar(g: Graph, nombre: str, texto: str) -> None:
    print(f"{'=' * 70}\n📄 {nombre}\n{'=' * 70}")
    print("\n".join(l for l in texto.splitlines() if l.startswith("#")), "\n")
    res = g.query(texto)
    if res.type == "ASK":
        print("→", str(res.askAnswer).lower(), "\n")
    elif res.type == "CONSTRUCT":
        print(res.graph.serialize(format="turtle").replace("http://example.org/", "ex:"))
        print(f"→ {len(res.graph)} triple(s)\n")
    else:
        vars_ = [str(v) for v in res.vars]
        filas = [["-" if c is None else corto(c) for c in f] for f in res]
        anchos = [max([len(v)] + [len(f[i]) for f in filas]) for i, v in enumerate(vars_)]
        print(" | ".join(v.ljust(anchos[i]) for i, v in enumerate(vars_)))
        print("-+-".join("-" * a for a in anchos))
        for f in filas:
            print(" | ".join(c.ljust(anchos[i]) for i, c in enumerate(f)))
        print(f"\n→ {len(filas)} resultado(s)\n")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    carpeta = BASE / args[0]
    grafo = cargar(carpeta, "--sin-inferencia" not in sys.argv)

    if (carpeta / "consultas.rq").exists():
        archivos = [carpeta / "consultas.rq"]
    elif len(args) > 1:
        archivos = [carpeta / "consultas" / a for a in args[1:]]
    else:
        archivos = sorted((carpeta / "consultas").glob("*.rq"))
    for a in archivos:
        ejecutar(grafo, a.name, a.read_text(encoding="utf-8"))
