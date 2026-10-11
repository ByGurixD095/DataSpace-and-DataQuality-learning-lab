#!/usr/bin/env bash
# Para los procesos lanzados por arrancar-local.sh
RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
[ -f "$RAIZ/.logs/pids" ] || { echo "No hay procesos registrados."; exit 0; }
while read -r pid; do kill "$pid" 2>/dev/null && echo "⏹️  pid $pid"; done < "$RAIZ/.logs/pids"
rm -f "$RAIZ/.logs/pids"
