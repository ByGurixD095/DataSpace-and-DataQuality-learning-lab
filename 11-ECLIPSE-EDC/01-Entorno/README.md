# 01 · Entorno

Compila y levanta **tres conectores EDC** (`ayuntamiento` = proveedor, `universidad` y `startup` = consumidores), un **backend** (fuente de datos) y un **receptor** (destino del push).

> ⚠️ **NO PROBADO contra un EDC real** (se escribió sin acceso a Maven Central). Basado en los *Samples* de EDC 0.18.1: si algo falla, contrasta con ellos.

## Requisitos
Java 17+, `openssl`, `jq`, `curl`, Python 3. Docker es opcional.

## Pasos
```bash
./01-Entorno/generar-claves.sh   # keys/cert.pem y keys/private.pem (se cargan en el Vault en memoria; NO se versionan)
./01-Entorno/compilar.sh         # ./gradlew shadowJar → connector.jar y provider.jar
./01-Entorno/arrancar-local.sh   # procesos Java locales; logs en .logs/
./01-Entorno/estado.sh           # ¿responden los puertos?
./01-Entorno/parar-local.sh
# Alternativa con contenedores (tras generar claves y compilar):
docker compose up
```
Con Docker, exporta `EDC_LAB_DOCKER=1` antes de usar los scripts de las otras carpetas.

## Puertos
| Conector | Management | DSP (protocol) | Public (data plane) | Control | Signaling |
|---|---|---|---|---|---|
| ayuntamiento | 19193 | 19194 | 19291 | 19192 | 19195 |
| universidad | 29193 | 29194 | 29291 | 29192 | 29196 |
| startup | 39193 | 39194 | 39291 | 39192 | 39196 |
Backend: 18081 · Receptor: 14000.

## Qué hay dentro del conector
`runtime/connector`: módulos EDC (`bom-controlplane-base` + transferencia HTTP con data plane *signaling*), `SeedVaultExtension` (carga las claves), `IamClaimsExtension` (identidad **mock**) y la política propia. `runtime/provider-proxy`: el proxy del data plane (necesario para *consumer pull*), solo en el proveedor.
