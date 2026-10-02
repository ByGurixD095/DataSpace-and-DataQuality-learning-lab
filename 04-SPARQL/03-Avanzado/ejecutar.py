"""
Ejecuta consultas / actualizaciones SPARQL sobre datos/red.trig con rdflib.

Uso:
    python ejecutar.py                          # todas (salvo SERVICE, que requiere Internet)
    python ejecutar.py consultas/06-graph-join.rq

Requisito: pip install rdflib

Cada archivo se ejecuta sobre una copia limpia en memoria: los UPDATE
(INSERT/DELETE) no modifican red.trig.
"""
import sys
from pathlib import Path

from rdflib import Dataset

BASE = Path(__file__).parent
DATOS = BASE / "datos" / "red.trig"
corto = lambda x: str(x).replace("http://example.org/", "ex:")


def cargar() -> Dataset:
    ds = Dataset(default_union=True)
    ds.parse(DATOS, format="trig")
    return ds


def ejecutar(archivo: Path) -> None:
    texto = archivo.read_text(encoding="utf-8")
    ds = cargar()
    print("=" * 70, f"\n📄 {archivo.name}\n" + "=" * 70)
    print(texto.strip(), "\n")

    cuerpo = "\n".join(l for l in texto.splitlines() if not l.startswith("#")).upper()
    es_update = any(k in cuerpo for k in ("INSERT", "DELETE")) and "SELECT" not in cuerpo.split("WHERE")[0]

    if es_update:
        antes = set(ds.quads())
        ds.update(texto)
        despues = set(ds.quads())
        for q in sorted(despues - antes, key=str):
            print("+", *(corto(x) for x in q[:3]), "(grafo:", corto(q[3]) + ")")
        for q in sorted(antes - despues, key=str):
            print("-", *(corto(x) for x in q[:3]), "(grafo:", corto(q[3]) + ")")
        print(f"\n→ +{len(despues - antes)} / -{len(antes - despues)} triples\n")
        return

    res = ds.query(texto)
    if res.type == "ASK":
        print("→", str(res.askAnswer).lower(), "\n")
    elif res.type in ("CONSTRUCT", "DESCRIBE"):
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
    if len(sys.argv) > 1:
        archivos = [Path(a) for a in sys.argv[1:]]
    else:
        archivos = [a for a in sorted((BASE / "consultas").glob("*.rq")) if "service" not in a.name]
    for a in archivos:
        try:
            ejecutar(a)
        except Exception as e:
            print(f"❌ Error: {e}\n")