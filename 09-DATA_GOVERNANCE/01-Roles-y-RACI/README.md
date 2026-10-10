# 👥 01 · Roles y RACI

> **Idea:** una matriz RACI no es un dibujo para un documento: son **reglas que se pueden comprobar**.

## 🎯 Qué aprenderás
- Qué significan **R**esponsable, **A**ccountable, **C**onsultado e **I**nformado.
- Por qué cada actividad necesita **una sola «A»** y **al menos una «R»**.
- Por qué los roles se asignan a **unidades o cargos, no a personas**.

## ▶️ Ejecutar
```bash
python raci.py                              # matriz válida → código de salida 0
python raci.py matriz_raci_con_errores.csv  # detecta 4 problemas → código de salida 1
```

## 📂 Archivos
| Archivo | Para qué |
| --- | --- |
| `matriz_raci.csv` | Matriz correcta de ejemplo |
| `matriz_raci_con_errores.csv` | La misma idea con errores (dos «A», ninguna «A», sin «R»…) |
| `raci.py` | Validador (solo biblioteca estándar) |

## 🧪 Prueba tú
1. Añade una actividad nueva al CSV y rompe una regla a propósito.
2. En una celda pon `A/R` (quien decide también ejecuta): ¿lo acepta el validador?
3. Usa el código de salida en un pipeline: ¿qué pasaría en CI si la matriz está mal?

## ➡️ Siguiente
[`02-Politicas-y-Clasificacion`](../02-Politicas-y-Clasificacion/): ¿qué puede hacerse con cada dato?
