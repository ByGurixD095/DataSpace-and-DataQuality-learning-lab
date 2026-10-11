#!/usr/bin/env bash
# Publica en el proveedor (ayuntamiento) 2 assets, 2 políticas y 2 contract definitions.
#   calidad-aire → política de contrato «solo universidades» (restricción propia: ver 05)
#   ruido-urbano → política abierta
set -euo pipefail
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$AQUI/../comun/env.sh"; source "$AQUI/../comun/lib.sh"

echo "📦 Publicando en el ayuntamiento ($MGMT_AYTO)"
for item in "assets:asset-calidad-aire" "assets:asset-ruido-urbano" \
            "policydefinitions:politica-abierta" "policydefinitions:politica-universidades" \
            "contractdefinitions:contract-def-calidad-aire" "contractdefinitions:contract-def-ruido-urbano"; do
  ruta="${item%%:*}"; fichero="${item##*:}"
  printf "  → %-20s %-28s " "$ruta" "$fichero"
  if respuesta="$(render "$AQUI/recursos/$fichero.json" | post "$MGMT_AYTO/$ruta" 2>&1)"; then
    echo "✅ $(echo "$respuesta" | jq -r '.["@id"]')"
  else
    echo "❌"; echo "$respuesta"; echo "   (si el id ya existe, EDC responde 409: ya está publicado)"
  fi
done
