#!/usr/bin/env bash
# Genera el par de claves (certificado + clave privada PKCS#8) con el que el data plane firma los tokens de acceso.
# Se crea en ./keys (ignorado por git). Claves de USAR Y TIRAR: solo para el laboratorio.
set -euo pipefail
RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
command -v openssl >/dev/null || { echo "❌ Falta openssl"; exit 1; }
mkdir -p "$RAIZ/keys"
openssl req -x509 -newkey rsa:2048 -nodes -days 365 -subj "/CN=edc-lab" \
  -keyout "$RAIZ/keys/private.pem" -out "$RAIZ/keys/cert.pem" 2>/dev/null
chmod 644 "$RAIZ/keys/private.pem" "$RAIZ/keys/cert.pem"   # legible desde los contenedores (laboratorio)
head -1 "$RAIZ/keys/private.pem"
echo "✅ Claves en $RAIZ/keys (cert.pem y private.pem)"
