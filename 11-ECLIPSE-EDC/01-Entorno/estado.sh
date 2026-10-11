#!/usr/bin/env bash
# ¿Están escuchando los puertos de cada pieza? (comprobación TCP: no depende de ningún endpoint de EDC)
comprobar() {   # comprobar <nombre> <puerto>
  if (exec 3<>"/dev/tcp/localhost/$2") 2>/dev/null; then echo "✅ $1 (puerto $2)"; else echo "❌ $1 (puerto $2)"; fi
}
comprobar "backend (fuente de datos)"   8081
comprobar "receptor (push)"             4000
comprobar "ayuntamiento · Management"   19193
comprobar "ayuntamiento · DSP"          19194
comprobar "ayuntamiento · data plane"   19291
comprobar "universidad  · Management"   29193
comprobar "universidad  · DSP"          29194
comprobar "startup      · Management"   39193
comprobar "startup      · DSP"          39194
