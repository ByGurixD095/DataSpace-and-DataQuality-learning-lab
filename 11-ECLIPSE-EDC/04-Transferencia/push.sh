#!/usr/bin/env bash
# PROVIDER PUSH: el proveedor ENVÍA los datos a un destino que indica el consumidor (el receptor de juguete).
#   ./push.sh [universidad] [asset]        (requiere negociar.sh antes)
set -euo pipefail
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$AQUI/../comun/env.sh"; source "$AQUI/../comun/lib.sh"
quien="${1:-universidad}"; asset="${2:-calidad-aire}"; mgmt="$(mgmt_de "$quien")"
f="$ESTADO/acuerdo-$quien-$asset.id"
[ -f "$f" ] || { echo "❌ No hay acuerdo de $quien sobre $asset: ejecuta antes 03-Catalogo-y-Negociacion/negociar.sh $quien $asset"; exit 1; }
export CONTRATO="$(cat "$f")"

echo "🚚 $quien inicia una transferencia PUSH → $RECEPTOR_URL"
tp_id="$(render "$AQUI/recursos/start-transfer-push.json" | post "$mgmt/transferprocesses" | jq -r '.["@id"]')"
echo "   transferencia: $tp_id"
esperar_estado "$mgmt/transferprocesses/$tp_id" 'COMPLETED|TERMINATED' 30 | jq '{state, "@id"}'

echo "📥 Lo que ha recibido el receptor:"
curl -sS "$RECEPTOR_ULTIMO" | jq .
