# 🔌 01 · Mini espacio simulado

> **Idea:** el ciclo completo de un espacio de datos, paso a paso, con dos conectores en Python y una traza que se lee de arriba abajo.

## 🎯 Qué aprenderás
- El orden real de un intercambio: **identidad → catálogo → negociación → acuerdo → transferencia**.
- Máquinas de estados explícitas de negociación y transferencia.
- Que los datos solo se mueven con un acuerdo `FINALIZED`.
- Cómo se cae un intercambio en cada punto: sin credencial, credencial revocada, finalidad fuera de la oferta, proveedor no admitido.

## ▶️ Ejecutar
```bash
python mini_espacio.py                                # escenario feliz (traza completa)
python mini_espacio.py --escenario sin-credencial
python mini_espacio.py --escenario denegado
python mini_espacio.py --escenario revocada
python mini_espacio.py --escenario proveedor-no-admitido
python mini_espacio.py --escenario todos              # tabla resumen
python mini_espacio.py --interactivo                  # eliges quién, a quién, qué y para qué
```

## 🧩 Qué integra
`05` (admisión por rulebook) → `04` (credencial Ed25519) → `02` (catálogo con ofertas) → `03` (evaluación ODRL y acuerdo) → transferencia con datos **sintéticos** + registro de usos.

## ⚠️ Importante
**Simulación didáctica.** Los nombres de mensajes y estados se inspiran en el Dataspace Protocol, pero **no es una implementación conforme**: no hay red, ni JSON-LD real, ni todos los estados y campos. `UsageReport` es un mensaje propio del laboratorio. Para ver una implementación real: [`11-Eclipse-EDC`](../../11-Eclipse-EDC/).

## 🧪 Prueba tú
1. Ejecuta `--interactivo` y pide a la universidad datos de `empresa-movilidad`: ¿por qué falla?
2. Corrige `rutas-bus` en `datos/ofertas.csv` y vuelve a ejecutar `--escenario proveedor-no-admitido`.
3. Añade un sexto escenario a `ESCENARIOS`.

## ➡️ Siguiente
[`11-Eclipse-EDC`](../../11-Eclipse-EDC/): lo mismo, con un conector real.
