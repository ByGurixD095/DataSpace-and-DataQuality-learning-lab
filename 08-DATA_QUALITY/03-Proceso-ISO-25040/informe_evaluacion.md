# Informe de evaluación de calidad del dato

*Generado el 2026-10-07 · referencia temporal de los datos: 2026-10-06 00:30*

## 1. Requisitos de la evaluación
- **Propósito:** Decidir si el dataset de calidad del aire sirve para un informe oficial de cumplimiento normativo
- **Interesados:** Responsable de medio ambiente (adquirente), Equipo de datos (proveedor), Evaluador independiente
- **Contexto de uso:** `informe_oficial` · **Rigor:** alto
- **Características priorizadas:** Completitud, Exactitud, Consistencia, Actualidad, Precisión

## 2. Especificación: medidas y criterios
| Medida | Característica | Criterio |
|---|---|---|
| `completitud_no2` | Completitud | ≥ 95% |
| `validez_no2` | Exactitud | ≥ 98% |
| `consistencia_pm` | Consistencia | ≥ 99% |
| `unicidad_clave` | Consistencia | ≥ 100% |
| `precision_no2` | Precisión | ≥ 90% |
| `actualidad_24h` | Actualidad | ≥ 100% |

## 3. Diseño
- **Datos evaluados:** datos/lecturas_calidad_aire.csv (50 filas)
- **Herramienta:** comun/dq.py (medidas ISO/IEC 25024 como ratios)
- **Reproducibilidad:** fecha de referencia fija + datos y código versionados

## 4. Ejecución
| Medida | Valor | Exigido | Resultado |
|---|---|---|---|
| `completitud_no2` | 94.0% (47/50) | ≥ 95% | ❌ no cumple |
| `validez_no2` | 90.0% (45/50) | ≥ 98% | ❌ no cumple |
| `consistencia_pm` | 96.0% (48/50) | ≥ 99% | ❌ no cumple |
| `unicidad_clave` | 96.0% (48/50) | ≥ 100% | ❌ no cumple |
| `precision_no2` | 93.6% (44/47) | ≥ 90% | ✅ cumple |
| `actualidad_24h` | 100.0% (1/1) | ≥ 100% | ✅ cumple |

## 5. Conclusiones
- **Medidas que no cumplen:** `completitud_no2`, `validez_no2`, `consistencia_pm`, `unicidad_clave`
- **Nivel de calidad** (contexto `informe_oficial`): **Medio**
- **Decisión de uso:** ⚠️ Utilizable solo con aviso y revisión manual

> Los umbrales son ilustrativos. Una evaluación formal debe documentar por qué se eligieron.
