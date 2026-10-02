"""
Cliente Python de un endpoint SPARQL usando solo la biblioteca estándar.

    python cliente.py                                   # contra servidor.py
    python cliente.py http://localhost:3030/ds/sparql   # contra otro endpoint (p. ej. Fuseki)
"""
import json
import sys
import urllib.parse
import urllib.request

ENDPOINT = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3030/sparql"

CONSULTA = """
PREFIX ex: <http://example.org/>
SELECT ?nombre ?edad
WHERE { ?p a ex:Persona ; ex:nombre ?nombre ; ex:edad ?edad . }
ORDER BY DESC(?edad) LIMIT 3
"""


def consultar(consulta: str, accept: str = "application/sparql-results+json") -> str:
    """Envía la consulta por HTTP POST y devuelve el cuerpo de la respuesta."""
    peticion = urllib.request.Request(
        ENDPOINT,
        data=urllib.parse.urlencode({"query": consulta}).encode(),
        headers={"Accept": accept},
    )
    with urllib.request.urlopen(peticion) as respuesta:
        return respuesta.read().decode("utf-8")


# 1) Resultados en JSON → estructura Python
datos = json.loads(consultar(CONSULTA))
print("Variables:", datos["head"]["vars"])
for fila in datos["results"]["bindings"]:
    print(f"  {fila['nombre']['value']} — {fila['edad']['value']} años")

# 2) El mismo resultado en CSV (solo cambia la cabecera Accept)
print("\nEn CSV:")
print(consultar(CONSULTA, accept="text/csv"))

# 3) ASK devuelve {"boolean": true/false}
ask = json.loads(consultar("ASK { <http://example.org/ana> a <http://example.org/Persona> }"))
print("¿Existe Ana?", ask["boolean"])
