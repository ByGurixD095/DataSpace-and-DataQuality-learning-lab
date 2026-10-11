#!/usr/bin/env bash
# Variables comunes a todos los scripts. Se "source"-ea: no se ejecuta directamente.
#
#   Modo local  (por defecto): los conectores corren como procesos Java en tu máquina.
#   Modo Docker (EDC_LAB_DOCKER=1): corren con docker compose; cambian las direcciones INTERNAS (DSP, backend, receptor).
#
# La Management API se llama SIEMPRE desde tu máquina, así que sus URL no cambian entre modos.

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export RAIZ

# Management API de cada participante (versión v3: es la de EDC 0.18.1; la 1.0.0-RC4 la elimina)
export MGMT_AYTO="http://localhost:19193/management/v3"
export MGMT_UNI="http://localhost:29193/management/v3"
export MGMT_STARTUP="http://localhost:39193/management/v3"

if [ "${EDC_LAB_DOCKER:-0}" = "1" ]; then
  export DSP_AYTO="http://ayuntamiento:19194/protocol/2025-1"
  export BACKEND_URL="http://backend:8081"
  export RECEPTOR_URL="http://receptor:4000/api/consumer/store"
else
  export DSP_AYTO="http://localhost:19194/protocol/2025-1"
  export BACKEND_URL="http://localhost:8081"
  export RECEPTOR_URL="http://localhost:4000/api/consumer/store"
fi
export RECEPTOR_ULTIMO="http://localhost:4000/ultimo"      # lo consultas tú, desde tu máquina

export ESTADO="$RAIZ/.estado"                              # ids de ofertas, acuerdos y transferencias entre pasos
mkdir -p "$ESTADO"
