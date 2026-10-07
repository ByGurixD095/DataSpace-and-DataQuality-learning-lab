# 🧰 comun/ — Biblioteca compartida

`dq.py` reúne lo que usan todas las carpetas, para que cada script sea corto y se centre en **un concepto**:

| Sección | Qué contiene | Se usa en |
| --- | --- | --- |
| **Modelo** | `CARACTERISTICAS`: las 15 de ISO/IEC 25012 con su perspectiva | 01, 03, 04, 06 |
| **Medidas** | Funciones `m_*` que devuelven una `Medida` (`cumplen / total`) | 02, 03, 04, 05, 06, 07 |
| **Reglas** | Evaluador de reglas en cuatro niveles (BR.DV → BR.DQM → BR.DQA → BR.DUD) | 03, 05, 07 |
| **DQV** | Construcción de mediciones RDF (solo esta parte necesita `rdflib`) | 01, 06, 07 |

> ⚠️ Material **didáctico**: ilustra los conceptos de los estándares, no los sustituye.

## ➕ Añadir tu propia medida

```python
def m_mi_medida(filas) -> Medida:
    ok = sum(1 for f in filas if ...)          # elementos que cumplen
    return Medida("mi_medida", "Nombre legible", "completeness", ok, len(filas), "Descripción")
```

Añádela a la lista de `medir_todo()` y aparecerá en todas las carpetas (y publicada en DQV).
