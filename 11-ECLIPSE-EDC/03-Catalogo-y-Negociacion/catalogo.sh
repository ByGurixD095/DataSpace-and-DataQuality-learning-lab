#!/usr/bin/env bash
# Pide el catálogo del ayuntamiento DESDE un consumidor (el catálogo se genera por consumidor, en el momento).
#   ./catalogo.sh [universidad|startup]        (por defecto: universidad)
# Guarda el catálogo en .estado/catalogo-<quien>.json: lo usa negociar.sh.
set -euo pipefail
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$AQUI/../comun/env.sh"; source "$AQUI/../comun/lib.sh"
quien="${1:-universidad}"; mgmt="$(mgmt_de "$quien")"

echo "📚 $quien pide el catálogo al ayuntamiento ($DSP_AYTO)"
catalogo="$(render "$AQUI/recursos/catalogo-request.json" | post "$mgmt/catalog/request")"
echo "$catalogo" > "$ESTADO/catalogo-$quien.json"

echo "$catalogo" | jq -r '
  (.["dcat:dataset"] // []) | if type=="array" then . else [.] end | .[] |
  "  • \(.["@id"])   oferta: \((.["odrl:hasPolicy"] | if type=="array" then .[0] else . end)["@id"])"'
echo "   (catálogo completo en .estado/catalogo-$quien.json)"
