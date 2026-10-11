# 📦 datos/

Datos de ejemplo **inventados** del espacio ambiental municipal. Tienen **huecos a propósito** para que el rulebook tenga algo que detectar. Derivan del escenario de [`09-Data-Governance`](../../09-Data-Governance/).

| Archivo | Contenido | Huecos deliberados |
| --- | --- | --- |
| `participantes.csv` | 4 participantes con las respuestas organizativas del rulebook | `startup-analitica` trata datos personales sin DPD (R03) y no lleva registro de usos (R10) |
| `ofertas.csv` | 5 datasets publicados: nivel, finalidades permitidas, deber de informar, calidad | `empresa-movilidad/rutas-bus` sin clasificación, sin oferta y sin calidad |
| `rulebook.json` | 10 reglas (obligatorias y recomendadas); R05–R07 son **derivadas** | — |
| `revocadas.json` | Credenciales revocadas por la autoridad | — |

Notas:
- El **padrón** de `09` (Confidencial) **no** está en `ofertas.csv`: no publicar lo que no debe compartirse también es gobierno.
- R05, R06 y R07 no se declaran: se **calculan** de lo que cada proveedor publica.
