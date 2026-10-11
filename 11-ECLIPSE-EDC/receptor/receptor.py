#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Receptor de juguete para el flujo PROVIDER PUSH: el data plane del proveedor envía aquí los datos.

  python3 receptor.py [puerto]        # por defecto 4000

  POST/PUT cualquier ruta  → guarda el cuerpo recibido en receptor/recibido/ y lo muestra
  GET /ultimo              → devuelve el último cuerpo recibido
Solo biblioteca estándar. SOLO PARA APRENDER.
"""
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

DESTINO = Path(__file__).resolve().parent / "recibido"
ultimo = b""


class Manejador(BaseHTTPRequestHandler):
    def _recibir(self):
        global ultimo
        n = int(self.headers.get("Content-Length") or 0)
        cuerpo = self.rfile.read(n) if n else b""
        ultimo = cuerpo
        DESTINO.mkdir(exist_ok=True)
        fichero = DESTINO / f"push-{int(time.time() * 1000)}.json"
        fichero.write_bytes(cuerpo)
        print(f"[receptor] {self.command} {self.path}: {len(cuerpo)} bytes → {fichero.name}", flush=True)
        self.send_response(200); self.end_headers()

    do_POST = _recibir
    do_PUT = _recibir

    def do_GET(self):
        if self.path.startswith("/ultimo"):
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers()
            self.wfile.write(ultimo or b"{}")
        else:
            self.send_response(404); self.end_headers()

    def log_message(self, *_):
        pass


if __name__ == "__main__":
    puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
    print(f"receptor escuchando en http://0.0.0.0:{puerto}", flush=True)
    HTTPServer(("0.0.0.0", puerto), Manejador).serve_forever()
