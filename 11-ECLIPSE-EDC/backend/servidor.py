#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backend de juguete: la «fuente de datos» del ayuntamiento (lo que apunta la dataAddress del asset).

  python3 servidor.py [puerto]        # por defecto 8081

Sirve backend/data/<dataset>/index.json en GET /<dataset>/ (y también /<dataset>/index.json).
Solo biblioteca estándar. SOLO PARA APRENDER.
"""
import sys
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

DATOS = Path(__file__).resolve().parent / "data"


class Manejador(SimpleHTTPRequestHandler):
    extensions_map = {**SimpleHTTPRequestHandler.extensions_map, ".json": "application/json"}

    def do_GET(self):
        # /calidad-aire/ → /calidad-aire/index.json  (el proxy del data plane pide la «carpeta»)
        if self.path.split("?")[0].endswith("/"):
            self.path = self.path.split("?")[0] + "index.json"
        super().do_GET()


if __name__ == "__main__":
    puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 8081
    print(f"backend sirviendo {DATOS} en http://0.0.0.0:{puerto}", flush=True)
    HTTPServer(("0.0.0.0", puerto), partial(Manejador, directory=str(DATOS))).serve_forever()
