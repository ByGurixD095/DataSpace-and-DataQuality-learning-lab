#!/usr/bin/env bash
# Negocia un contrato sobre un asset: se envía la OFERTA EXACTA que apareció en el catálogo.
#   ./negociar.sh <universidad|startup> <asset>        p. ej.  ./negociar.sh universidad calidad-aire
# Sale con código 0 si la negociación termina en FINALIZED y con 1 si termina en TERMINATED.
# La negociación es ASÍNCRONA: se lanza y se consulta su estado.
set -euo pipefail
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$AQUI/../comun/env.sh"; source "$AQUI/../comun/lib.sh"
quien="${1:?uso: negociar.sh <universidad|startup> <asset>}"; asset="${2:?uso: negociar.sh <universidad|startup> <asset>}"
mgmt="$(mgmt_de "$quien")"
cat_f="$ESTADO/catalogo-$quien.json"
[ -f "$cat_f" ] || "$AQUI/catalogo.sh" "$quien" >/dev/null

# La oferta del catálogo para ese asset (odrl:hasPolicy)
oferta="$(jq -c --arg a "$asset" '
  (.["dcat:dataset"] // []) | if type=="array" then . else [.] end
  | map(select(.["@id"]==$a)) | .[0] // empty
  | .["odrl:hasPolicy"] | if type=="array" then .[0] else . end' "$cat_f")"
[ -n "$oferta" ] || { echo "❌ '$asset' no aparece en el catálogo de $quien (¿publicado? ¿lo oculta la política de acceso?)"; exit 1; }

# Petición: la base + el @context del catálogo + la oferta exacta
cuerpo="$(render "$AQUI/recursos/contract-request.base.json" | jq -c \
  --argjson ctx "$(jq -c '.["@context"]' "$cat_f")" --argjson pol "$oferta" --arg a "$asset" \
  '{"@context": $ctx} + . + {policy: ($pol | .["odrl:assigner"] //= {"@id":"ayuntamiento"} | .["odrl:target"] //= {"@id":$a})}')"

echo "🤝 $quien negocia «$asset» con el ayuntamiento"
neg_id="$(echo "$cuerpo" | post "$mgmt/contractnegotiations" | jq -r '.["@id"]')"
echo "   negociación: $neg_id"
final="$(esperar_estado "$mgmt/contractnegotiations/$neg_id" 'FINALIZED|TERMINATED' 40)"
estado="$(echo "$final" | jq -r '.state')"

if [ "$estado" = "FINALIZED" ]; then
  acuerdo="$(echo "$final" | jq -r '.contractAgreementId')"
  echo "$acuerdo" > "$ESTADO/acuerdo-$quien-$asset.id"
  echo "✅ FINALIZED — acuerdo: $acuerdo"
else
  echo "❌ TERMINATED — $(echo "$final" | jq -r '.errorDetail // "sin detalle"')"
  echo "   (mira el log del ayuntamiento: ¿qué restricción evaluó y con qué resultado?)"
  exit 1
fi
