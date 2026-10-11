#!/usr/bin/env bash
# Arranca TODO en local (sin Docker): backend, receptor y los tres conectores como procesos Java.
# Requisitos: ./generar-claves.sh y ./compilar.sh ejecutados. Logs en .logs/, PIDs en .logs/pids.
set -euo pipefail
RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$RAIZ"
for f in keys/cert.pem runtime/connector/build/libs/connector.jar runtime/provider-proxy/build/libs/provider.jar; do
  [ -f "$f" ] || { echo "❌ Falta $f (¿has ejecutado generar-claves.sh y compilar.sh?)"; exit 1; }
done
mkdir -p .logs; : > .logs/pids
export LAB_KEYS_DIR="$RAIZ/keys"

arrancar() {   # arrancar <nombre> <comando...>
  local nombre="$1"; shift
  "$@" > ".logs/$nombre.log" 2>&1 &
  echo $! >> .logs/pids
  echo "▶️  $nombre (pid $!) → .logs/$nombre.log"
}

arrancar backend   python3 backend/servidor.py 8081
arrancar receptor  python3 receptor/receptor.py 4000
arrancar ayuntamiento java -Dedc.fs.config=config/local/ayuntamiento.properties -jar runtime/provider-proxy/build/libs/provider.jar
arrancar universidad  java -Dedc.fs.config=config/local/universidad.properties  -jar runtime/connector/build/libs/connector.jar
arrancar startup      java -Dedc.fs.config=config/local/startup.properties      -jar runtime/connector/build/libs/connector.jar

echo; echo "⏳ Los conectores tardan unos segundos en arrancar. Comprueba con: ./01-Entorno/estado.sh"
