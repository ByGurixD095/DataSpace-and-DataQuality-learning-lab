# 03 · Catálogo y negociación

> ⚠️ **NO PROBADO contra un EDC real** (se escribió sin acceso a Maven Central). Basado en los *Samples* de EDC 0.18.1: si algo falla, contrasta con ellos.

```bash
./03-Catalogo-y-Negociacion/catalogo.sh universidad
./03-Catalogo-y-Negociacion/negociar.sh universidad calidad-aire
```
- El catálogo se genera **por consumidor** y se guarda en `.estado/`.
- `negociar.sh` envía **la oferta exacta del catálogo** (`odrl:hasPolicy`), no «el dataset» (mismo principio que en `10`), y consulta el estado hasta `FINALIZED` o `TERMINATED` (la negociación es asíncrona).
- Si termina bien, guarda el `contractAgreementId` en `.estado/`.

La lógica `jq` de extracción de la oferta se probó con un catálogo sintético; la respuesta real de EDC puede variar de forma (JSON-LD expandido/compactado).
