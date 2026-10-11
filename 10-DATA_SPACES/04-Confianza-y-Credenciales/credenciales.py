#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
04 · Confianza y credenciales: ¿cómo sabe un proveedor que quien llama es miembro del espacio?

  python credenciales.py                      # 6 casos: válida, sin credencial, caducada, revocada, manipulada, emisor falso
  python credenciales.py --emitir universidad # la autoridad emite (solo si el rulebook admite) y guarda credenciales/ID.json
  python credenciales.py --verificar credenciales/universidad.json

Una credencial de adhesión es la versión técnica del «acuerdo de adhesión» de 09: demuestra que el
participante aceptó el rulebook y fue admitido. Va FIRMADA con Ed25519: la autoridad firma con su clave
privada y cualquiera comprueba con su clave pública, sin un login central.

⚠️ Simulación didáctica: no usa DID ni credenciales verificables W3C; la clave sale de una semilla fija.
Requiere: cryptography
"""
import argparse, json, sys
from datetime import date
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "comun"))
import espacio as e

ap = argparse.ArgumentParser()
ap.add_argument("--emitir"); ap.add_argument("--verificar")
a = ap.parse_args()
PUB = e.clave_publica_hex(e.clave_autoridad())

if a.emitir:
    try:
        cred = e.emitir_credencial(a.emitir)
    except (PermissionError, ValueError) as err:
        sys.exit(f"❌ {err}")
    (AQUI / "credenciales").mkdir(exist_ok=True)
    ruta = AQUI / "credenciales" / f"{a.emitir}.json"
    ruta.write_text(json.dumps(cred, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Credencial emitida → {ruta.relative_to(AQUI)}\n" + json.dumps(cred, ensure_ascii=False, indent=2))
    sys.exit(0)

if a.verificar:
    cred = json.loads(Path(a.verificar).read_text(encoding="utf-8"))
    ok, motivo = e.verificar_credencial(cred, PUB)
    print(f"{'✅' if ok else '❌'} {motivo}")
    sys.exit(0 if ok else 1)

print(f"\n🔐 CLAVE PÚBLICA DE LA AUTORIDAD (la conoce todo el espacio)\n   {PUB}\n")
casos = []
casos.append(("Universidad, credencial emitida tras la admisión", e.emitir_credencial("universidad")))
try:
    e.emitir_credencial("startup-analitica")
except PermissionError as err:
    casos.append((f"Startup: {err}", None))
casos.append(("Credencial de la universidad caducada", e.emitir_credencial("universidad", emitida=date(2025, 9, 1), caduca=date(2026, 9, 1))))
casos.append(("Credencial antigua de la startup (ya revocada)",
              e.emitir_credencial("startup-analitica", cred_id="cred-startup-analitica-antigua", forzar=True)))
manip = e.emitir_credencial("universidad"); manip["sujeto"] = "startup-analitica"      # cambia el sujeto SIN volver a firmar
casos.append(("Universidad cambia el sujeto a «startup-analitica»", manip))
casos.append(("Credencial firmada por otra autoridad",
              e.emitir_credencial("universidad", clave=e._clave("otra-semilla"), emisor="autoridad-falsa", forzar=True)))

print("🧪 CASOS\n" + "─" * 86)
for desc, cred in casos:
    ok, motivo = e.verificar_credencial(cred, PUB)
    print(f"{'✅' if ok else '❌'} {desc}\n      → {motivo}")
print("\n💡 Orden de comprobación: presencia → emisor reconocido → firma → vigencia → revocación."
      "\n   La firma no oculta nada: protege la AUTENTICIDAD. El estado (caducidad, revocación) se comprueba aparte.")
