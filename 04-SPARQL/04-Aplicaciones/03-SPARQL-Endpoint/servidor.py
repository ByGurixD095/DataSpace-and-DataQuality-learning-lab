"""
Mini SPARQL endpoint (solo consultas) con RDFLib + biblioteca estándar.

    pip install rdflib
    python servidor.py            # → http://localhost:3030/sparql

Implementa lo esencial del protocolo SPARQL:
  GET  /sparql?query=...
  POST /sparql  (Content-Type: application/sparql-query  ó  application/x-www-form-urlencoded)
y elige el formato de salida según la cabecera Accept (JSON, CSV o XML).
Es un juguete didáctico: para uso real, utiliza Apache Jena Fuseki, GraphDB, Virtuoso, etc.
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from rdflib import Graph

PUERTO = 3030
FORMATOS = {  # Accept → (formato rdflib, Content-Type de respuesta)
    "application/sparql-results+json": ("json", "application/sparql-results+json"),
    "text/csv": ("csv", "text/csv"),
    "application/sparql-results+xml": ("xml", "application/sparql-results+xml"),
}

grafo = Graph()
grafo.parse(Path(__file__).parent.parent / "datos" / "personas.ttl", format="turtle")


class Endpoint(BaseHTTPRequestHandler):
    def _responder(self, codigo: int, cuerpo: bytes, tipo: str = "text/plain; charset=utf-8"):
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(cuerpo)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(cuerpo)

    def _ejecutar(self, consulta: str | None):
        if not consulta:
            return self._responder(400, "Falta la consulta (parámetro 'query').".encode())
        accept = self.headers.get("Accept", "")
        formato, tipo = next((v for k, v in FORMATOS.items() if k in accept), FORMATOS["application/sparql-results+json"])
        try:
            resultado = grafo.query(consulta)
            if resultado.type not in ("SELECT", "ASK"):
                return self._responder(400, b"Este endpoint solo admite SELECT y ASK.")
            self._responder(200, resultado.serialize(format=formato), tipo)
        except Exception as e:  # consulta mal formada, etc.
            self._responder(400, f"Error en la consulta: {e}".encode())

    def do_GET(self):
        url = urlparse(self.path)
        if url.path != "/sparql":
            return self._responder(404, b"Usa /sparql")
        self._ejecutar(parse_qs(url.query).get("query", [None])[0])

    def do_POST(self):
        if urlparse(self.path).path != "/sparql":
            return self._responder(404, b"Usa /sparql")
        cuerpo = self.rfile.read(int(self.headers.get("Content-Length", 0))).decode("utf-8")
        if "application/sparql-query" in self.headers.get("Content-Type", ""):
            self._ejecutar(cuerpo)
        else:
            self._ejecutar(parse_qs(cuerpo).get("query", [None])[0])

    def log_message(self, formato, *args):
        print(f"[{self.command}] {self.path[:80]} → {args[1]}")


if __name__ == "__main__":
    print(f"Grafo cargado: {len(grafo)} triples")
    print(f"Endpoint SPARQL en http://localhost:{PUERTO}/sparql  (Ctrl+C para parar)")
    HTTPServer(("localhost", PUERTO), Endpoint).serve_forever()
