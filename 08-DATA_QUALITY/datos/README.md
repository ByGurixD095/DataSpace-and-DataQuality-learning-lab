# 📊 datos/ — El dataset de práctica

Mediciones **horarias sintéticas** de calidad del aire de dos estaciones (E01 y E02) durante un día, con **defectos conocidos** puestos a propósito. Es el mismo dataset (`ex:dataset-calidad-aire`) que recorre `06-ODRL` y `07-DCAT`.

| Fichero | Qué es |
| --- | --- |
| `lecturas_calidad_aire.csv` | 50 filas: `estacion, fecha_hora, no2, pm10, pm25` |
| `generar_datos.py` | Lo regenera (reproducible) y documenta los defectos |

## 🐞 Defectos conocidos

| Defecto | Filas | Característica ISO/IEC 25012 | Medida que lo detecta |
| --- | --- | --- | --- |
| NO₂ vacío | 3 | Completitud | `completitud_no2` = 47/50 |
| NO₂ fuera de rango (-5, 5000) | 2 | Exactitud (sintáctica) | `validez_no2` = 45/50 |
| PM2,5 mayor que PM10 | 2 | Consistencia | `consistencia_pm` = 48/50 |
| Fila duplicada (misma estación y hora) | 2 | Consistencia (unicidad) | `unicidad_clave` = 48/50 |
| NO₂ sin decimales | 3 | Precisión | `precision_no2` = 44/47 |

> 🎯 Como los defectos están contados, **sabes cuál debe ser el resultado** de cada medida: es la mejor forma de comprobar que tu código mide bien.
