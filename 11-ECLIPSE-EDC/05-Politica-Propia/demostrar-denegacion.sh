#!/usr/bin/env bash
# La MISMA oferta, dos solicitantes: la universidad la consigue; la startup, no.
# Requiere publicar.sh ejecutado antes y los tres conectores en marcha.
set -uo pipefail
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NEG="$AQUI/../03-Catalogo-y-Negociacion/negociar.sh"

echo "════ 1) La universidad (tipoParticipante=universidad) pide «calidad-aire» ════"
"$NEG" universidad calidad-aire && r1="✅ FINALIZED" || r1="❌ TERMINATED"
echo
echo "════ 2) La startup (tipoParticipante=startup) pide «calidad-aire» ════"
"$NEG" startup calidad-aire && r2="✅ FINALIZED" || r2="❌ TERMINATED"
echo
echo "════ 3) La startup pide «ruido-urbano» (política abierta) ════"
"$NEG" startup ruido-urbano && r3="✅ FINALIZED" || r3="❌ TERMINATED"

echo; echo "RESUMEN   universidad/calidad-aire: $r1   startup/calidad-aire: $r2   startup/ruido-urbano: $r3"
echo "ESPERADO  universidad/calidad-aire: ✅ FINALIZED   startup/calidad-aire: ❌ TERMINATED   startup/ruido-urbano: ✅ FINALIZED"
echo "Mira el log del ayuntamiento: busca «Evaluando restricción: tipoParticipante»."
