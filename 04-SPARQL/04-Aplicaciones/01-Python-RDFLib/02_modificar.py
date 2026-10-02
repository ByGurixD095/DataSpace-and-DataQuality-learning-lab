"""
02 — Modificar un grafo (API de Python y SPARQL Update), ASK y CONSTRUCT.

    python 02_modificar.py
Los cambios son en memoria: el archivo .ttl no se modifica.
"""
from pathlib import Path

from rdflib import RDF, Graph, Literal, Namespace

EX = Namespace("http://example.org/")
g = Graph()
g.parse(Path(__file__).parent.parent / "datos" / "personas.ttl", format="turtle")
print(f"Triples iniciales: {len(g)}")

# 1) Modificar con la API de Python
g.add((EX.laura, RDF.type, EX.Persona))
g.add((EX.laura, EX.nombre, Literal("Laura Gil")))
g.add((EX.laura, EX.edad, Literal(25)))
g.add((EX.laura, EX.viveEn, EX.Madrid))
print(f"Tras g.add(...):   {len(g)}")

# 2) Modificar con SPARQL Update
g.update("""
    PREFIX ex: <http://example.org/>
    DELETE { ex:laura ex:viveEn ex:Madrid }
    INSERT { ex:laura ex:viveEn ex:Valencia }
    WHERE  { ex:laura ex:viveEn ex:Madrid }
""")
print(f"Tras DELETE/INSERT: {len(g)} (mismo nº: se quitó 1 y se añadió 1)")

# 3) ASK: comprobar el cambio
vive_en_valencia = g.query("ASK { <http://example.org/laura> <http://example.org/viveEn> <http://example.org/Valencia> }")
print(f"¿Laura vive en Valencia? {vive_en_valencia.askAnswer}")

# 4) CONSTRUCT: generar un nuevo grafo a partir de otro
nuevo = g.query("""
    PREFIX ex:   <http://example.org/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    CONSTRUCT { ?p foaf:name ?n }
    WHERE     { ?p a ex:Persona ; ex:nombre ?n . FILTER(?n = "Laura Gil") }
""").graph
nuevo.bind("foaf", "http://xmlns.com/foaf/0.1/")
print("\nGrafo construido (Turtle):")
print(nuevo.serialize(format="turtle"))
