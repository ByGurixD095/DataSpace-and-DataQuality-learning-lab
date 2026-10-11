# 06 · Identidad real con el MVD

Aquí no hay código propio: el **Minimum Viable Dataspace (MVD)** de Eclipse es un entorno de demostración que despliega conectores con **Identity Hub**, **Issuer Service** y credenciales verificables (**DCP**), sobre Kubernetes (KinD).

> ⚠️ No probado desde aquí. Sigue el README del repositorio **en una etiqueta concreta** (no `main`) y respeta sus requisitos (Docker, KinD, Helm, JDK 17+, Git). Es una demo, no un despliegue de producción.

## Guía
1. `git clone https://github.com/eclipse-edc/MinimumViableDataspace.git` y `git checkout <etiqueta>`.
2. Levántalo según su README y recorre su flujo (catálogo → negociación → transferencia).
3. Observa cómo la identidad deja de ser un *claim* declarado: el conector exige **credenciales emitidas por un emisor de confianza**.

## Mapa con `10-Data-Spaces`
| En el mini-espacio (10) | En EDC con DCP |
|---|---|
| `04-Confianza-y-Credenciales` (Ed25519) | Credenciales verificables firmadas, verificadas por Identity Hub |
| Rulebook | Políticas + tipos de credencial exigidos |
| `tipoParticipante` (claim mock, carpeta 05) | Credencial de pertenencia / tipo de participante |

**Ejercicio:** reescribe la restricción de `05` para que exija una credencial en vez de un claim declarado.
