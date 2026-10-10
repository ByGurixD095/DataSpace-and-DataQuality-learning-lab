# 🌳 04 · Linaje con PROV-O

> **Idea:** saber **de dónde viene** un dato (origen) y **a qué afecta** si cambia (impacto). El linaje también permite **propagar la clasificación**.

## 🎯 Qué aprenderás
- `prov:wasDerivedFrom`, `prov:wasGeneratedBy`, `prov:used` y actividades.
- Recorrer cadenas completas con **property paths** (`prov:wasDerivedFrom+`).
- La regla: **un derivado no puede ser menos restrictivo que su origen**, salvo que la actividad **anonimice** (`gov:anonimiza true`).

## ▶️ Ejecutar
```bash
python linaje.py                          # árbol, propagación de clasificación y cobertura (6/10)
python linaje.py --origen informe-movilidad
python linaje.py --impacto sensores-iot
```
Genera `linaje.ttl`. Sale con código 1 si hay alertas de clasificación.

## 👀 Qué verás
- 1 alerta: `informe-demografico-publico` es Público pero deriva de un dato Confidencial **sin anonimizar**.
- `tabla-demografica-anonimizada` parte del mismo origen y **no** da alerta: la actividad declara anonimización.

## ⚠️ Matiz
`gov:anonimiza` es una **declaración**. Que la anonimización sea realmente suficiente es otra cuestión (técnica y jurídica) que este script no evalúa.

## ➡️ Siguiente
[`05-Cobertura-de-Gobierno`](../05-Cobertura-de-Gobierno/)
