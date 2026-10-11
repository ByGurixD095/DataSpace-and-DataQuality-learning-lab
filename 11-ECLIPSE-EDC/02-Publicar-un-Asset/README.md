# 02 · Publicar un asset

Publica en el ayuntamiento dos datasets con los **tres objetos** de EDC: asset, policy definition y contract definition.

> ⚠️ **NO PROBADO contra un EDC real** (se escribió sin acceso a Maven Central). Basado en los *Samples* de EDC 0.18.1: si algo falla, contrasta con ellos.

```bash
./02-Publicar-un-Asset/publicar.sh
```

| Dataset | Política de acceso | Política de contrato |
|---|---|---|
| `calidad-aire` | abierta | **solo universidades** (`tipoParticipante eq universidad`) |
| `ruido-urbano` | abierta | abierta |

El asset apunta (`dataAddress` HttpData) al backend: `/calidad-aire/`, `/ruido-urbano/`. Los JSON están en `recursos/`. Ejercicio: cambia la política de acceso para que la startup **ni vea** el asset en su catálogo.
