#!/usr/bin/env bash
# CONSUMER PULL: el consumidor pide la transferencia, recibe una EDR y recoge los datos él mismo.
#   ./pull.sh [universidad] [asset]        (por defecto: universidad calidad-aire; requiere negociar.sh antes)
set -euo pipefail
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$AQUI/../comun/env.sh"; source "$AQUI/../comun/lib.sh"
quien="${1:-universidad}"; asset="${2:-calidad-aire}"; mgmt="$(mgmt_de "$quien")"
f="$ESTADO/acuerdo-$quien-$asset.id"
[ -f "$f" ] || { echo "❌ No hay acuerdo de $quien sobre $asset: ejecuta antes 03-Catalogo-y-Negociacion/negociar.sh $quien $asset"; exit 1; }
export CONTRATO="$(cat "$f")"

echo "🚚 $quien inicia una transferencia PULL del acuerdo $CONTRATO"
tp_id="$(render "$AQUI/recursos/start-transfer-pull.json" | post "$mgmt/transferprocesses" | jq -r '.["@id"]')"
echo "   transferencia: $tp_id"
esperar_estado "$mgmt/transferprocesses/$tp_id" 'STARTED|COMPLETED|TERMINATED' 30 | jq '{state, "@id"}'

echo "🔑 EDR (Endpoint Data Reference) guardada por el consumidor:"
edr="$(curl -sS "$mgmt/edrs/$tp_id/dataaddress")"
endpoint="$(echo "$edr" | jq -r '.endpoint')"; token="$(echo "$edr" | jq -r '.authorization')"
echo "   endpoint: $endpoint"; echo "   token:    ${token:0:40}…"

echo "⬇️  El consumidor recoge los datos del data plane del proveedor:"
curl -sS "$endpoint/" -H "Authorization: $token" | jq .
