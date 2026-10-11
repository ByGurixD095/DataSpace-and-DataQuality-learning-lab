# 05 · Política propia

Una restricción `tipoParticipante` evaluada **por el conector**, en Java.

> ⚠️ **NO PROBADO contra un EDC real** (se escribió sin acceso a Maven Central). Basado en los *Samples* de EDC 0.18.1: si algo falla, contrasta con ellos.

```bash
./05-Politica-Propia/demostrar-denegacion.sh
```
Resultado esperado: universidad/calidad-aire ✅ · startup/calidad-aire ❌ · startup/ruido-urbano ✅.

## Código (`runtime/connector/.../policy`)
- `PolicyFunctionsExtension`: enlaza la acción `use` y el operando izquierdo (`EDC_NAMESPACE + "tipoParticipante"`) al ámbito de negociación y registra la función.
- `TipoParticipanteConstraintFunction`: compara (solo `EQ`/`NEQ`); **deniega por defecto** ante operador o valor desconocido.
- `IamClaimsExtension`: añade el claim al *iam-mock*.

> 🚨 **Con `iam-mock` cualquiera puede declarar cualquier claim: NO es seguro.** Es un andamio didáctico. La identidad real es DCP con credenciales verificables → carpeta `06`.
