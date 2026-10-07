# 📐 01 · Modelo ISO/IEC 25012

**Las 15 características de calidad del dato, convertidas en un grafo RDF que se puede consultar.**

## 🎯 Qué aprendes
- Cómo se reparten las 15 características: **5 inherentes, 7 mixtas y 3 del sistema**.
- Que el modelo cabe en **DQV**: una dimensión puede pertenecer a **más de una categoría** (así se representan las mixtas).
- Qué características **no** se pueden medir mirando solo los valores.

## ▶️ Ejecutar

```bash
python explorar_modelo.py      # requiere rdflib
```

## 📦 Qué hay
| Fichero | Contenido |
| --- | --- |
| `explorar_modelo.py` | Construye el modelo, lo guarda y lo interroga con SPARQL |
| `caracteristicas_25012.ttl` | El modelo generado: 2 categorías + 15 dimensiones, con etiquetas ES/EN y definiciones |

## 🔍 Qué observar

```
🧬🖥️ mixtas          7   Accesibilidad, Conformidad, Confidencialidad, …
🧬 inherentes        5   Exactitud, Completitud, Consistencia, Credibilidad, Actualidad
🖥️ del sistema      3   Disponibilidad, Portabilidad, Recuperabilidad

📏 Cobertura de este laboratorio: 5 de 15 características tienen alguna medida automática.
```

- La consulta SPARQL **deduce** si una característica es mixta contando en cuántas categorías está: la estructura del grafo *es* el conocimiento.
- Solo **5 de 15** quedan cubiertas por medidas automáticas. El resto (credibilidad, trazabilidad, disponibilidad…) exige inspección, metadatos o monitorización. Reconocerlo forma parte de una evaluación honesta.

## 🏋️ Ejercicios
1. 🟢 Abre `caracteristicas_25012.ttl` y localiza a qué categorías pertenece *Precisión*.
2. 🟡 Escribe una consulta SPARQL que liste las características **solo del sistema** con su definición.
3. 🔴 Añade una característica ficticia al modelo (por ejemplo, «Sostenibilidad») y comprueba cómo la clasifica la consulta.

➡️ Siguiente: [`02-Medidas-ISO-25024`](../02-Medidas-ISO-25024/) — cómo se mide cada característica.
