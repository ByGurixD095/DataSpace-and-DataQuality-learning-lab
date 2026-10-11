# 04 · Transferencia

> ⚠️ **NO PROBADO contra un EDC real** (se escribió sin acceso a Maven Central). Basado en los *Samples* de EDC 0.18.1: si algo falla, contrasta con ellos.

```bash
./04-Transferencia/pull.sh universidad calidad-aire   # consumer pull con EDR
./04-Transferencia/push.sh universidad ruido-urbano   # provider push al receptor
```
- **Pull:** el consumidor obtiene una **EDR** (`/edrs/{id}/dataaddress`: `endpoint` + token `authorization`) y llama él mismo al proxy público del proveedor.
- **Push:** el proveedor envía los datos al receptor (`receptor/recibido/`; consulta `GET /ultimo`).
- El proxy de ejemplo solo admite **GET** y no es para producción.
