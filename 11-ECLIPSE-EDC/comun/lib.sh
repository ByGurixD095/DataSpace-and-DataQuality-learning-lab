#!/usr/bin/env bash
# Funciones comunes. Se "source"-ea después de env.sh.

for cmd in curl jq; do
  command -v "$cmd" >/dev/null || { echo "❌ Falta '$cmd' (instálalo para ejecutar los scripts)"; exit 1; }
done

# mgmt_de <ayuntamiento|universidad|startup> → URL de su Management API
mgmt_de() {
  case "$1" in
    ayuntamiento|ayto) echo "$MGMT_AYTO" ;;
    universidad|uni)   echo "$MGMT_UNI" ;;
    startup)           echo "$MGMT_STARTUP" ;;
    *) echo "❌ Participante desconocido: '$1' (usa ayuntamiento, universidad o startup)" >&2; return 1 ;;
  esac
}

# render <plantilla.json> → la plantilla con las {{VARIABLES}} sustituidas
render() {
  sed -e "s#{{DSP_AYTO}}#${DSP_AYTO}#g" \
      -e "s#{{BACKEND_URL}}#${BACKEND_URL}#g" \
      -e "s#{{RECEPTOR_URL}}#${RECEPTOR_URL}#g" \
      -e "s#{{CONTRATO}}#${CONTRATO:-}#g" "$1"
}

# post <url> → lee el cuerpo por stdin, muestra la respuesta y falla si el HTTP es >= 400
post() {
  local url="$1" salida codigo
  salida="$(curl -sS -w '\n%{http_code}' -X POST -H 'content-type: application/json' -d @- "$url")" || return 1
  codigo="${salida##*$'\n'}"; salida="${salida%$'\n'*}"
  if [ "$codigo" -ge 400 ]; then
    echo "❌ HTTP $codigo en POST $url" >&2; echo "$salida" | jq . 2>/dev/null >&2 || echo "$salida" >&2
    return 1
  fi
  echo "$salida"
}

# esperar_estado <url> <regex de estados finales> [intentos] → imprime el JSON final; asíncrono: se CONSULTA
esperar_estado() {
  local url="$1" finales="$2" intentos="${3:-30}" cuerpo estado
  for _ in $(seq 1 "$intentos"); do
    cuerpo="$(curl -sS "$url")" || return 1
    estado="$(echo "$cuerpo" | jq -r '.state // empty')"
    echo "   · estado: ${estado:-?}" >&2
    if [[ "$estado" =~ ^($finales)$ ]]; then echo "$cuerpo"; return 0; fi
    sleep 1
  done
  echo "❌ Tiempo agotado esperando ($finales)" >&2; echo "$cuerpo"; return 1
}
