"""
01 — Cargar un grafo y ejecutar consultas SPARQL con RDFLib.

    pip install rdflib
    python 01_consulta.py
"""
import json
from pathlib import Path

from rdflib import Graph, Namespace
from rdflib.plugins.sparql import prepareQuery

DATOS = Path(__file__).parent.parent / "datos" / "personas.ttl"
EX = Namespace("http://example.org/")

# 1) Crear el grafo y cargar datos RDF
g = Graph()
g.parse(DATOS, format="turtle")
print(f"Grafo cargado: {len(g)} triples\n")

# 2) Ejecutar un SELECT y recorrer los resultados
consulta = """
PREFIX ex: <http://example.org/>
SELECT ?nombre ?edad
WHERE {
    ?p a ex:Persona ; ex:nombre ?nombre ; ex:edad ?edad .
}
ORDER BY DESC(?edad)
LIMIT 3
"""
print("Las 3 personas de mayor edad:")
for fila in g.query(consulta):
    # Se accede por nombre de variable; .toPython() convierte el literal RDF a tipo Python
    print(f"  {fila.nombre} — {fila.edad.toPython()} años")

# 3) Consulta parametrizada: se compila una vez y se le pasan valores (initBindings)
por_ciudad = prepareQuery(
    "SELECT ?nombre WHERE { ?p ex:nombre ?nombre ; ex:viveEn ?ciudad . }",
    initNs={"ex": EX},
)
for ciudad in (EX.Madrid, EX.Sevilla):
    nombres = [str(f.nombre) for f in g.query(por_ciudad, initBindings={"ciudad": ciudad})]
    print(f"\nViven en {ciudad.split('/')[-1]}: {', '.join(nombres)}")

# 4) Convertir resultados en estructuras Python / JSON para usarlos en una aplicación
resultado = g.query("""
    PREFIX ex: <http://example.org/>
    SELECT ?genero (COUNT(?l) AS ?libros) WHERE { ?l a ex:Libro ; ex:genero ?genero . }
    GROUP BY ?genero ORDER BY ?genero
""")
datos = [{str(k): v.toPython() for k, v in fila.asdict().items()} for fila in resultado]
print("\nLibros por género (JSON):")
print(json.dumps(datos, ensure_ascii=False, indent=2))
