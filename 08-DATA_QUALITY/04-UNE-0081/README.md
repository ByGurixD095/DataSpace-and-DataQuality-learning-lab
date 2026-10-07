# 🇪🇸 04 · UNE 0081 — Evaluación de la calidad del dato

**Una matriz de trabajo que conecta características, métricas y umbrales, y te dice qué parte de la evaluación has podido automatizar.**

## 🎯 Qué aprendes
- Cómo se organiza una evaluación al estilo de la **UNE 0081:2023**: modelo (ISO/IEC 25012) → métricas (ISO/IEC 25024) → proceso (ISO/IEC 25040).
- Que una evaluación seria informa de su **cobertura**: qué se ha medido y qué queda pendiente.

> ⚠️ **Esto NO es la especificación.** `matriz_evaluacion.csv` es una **plantilla de trabajo** inspirada en el proceso; no reproduce el contenido de la UNE 0081. Para el modelo y las métricas oficiales, consulta la norma (se puede adquirir en AENOR) y la explicación de datos.gob.es enlazada en el README principal.

## ▶️ Ejecutar (solo biblioteca estándar)

```bash
python matriz.py
```

## 📦 Qué hay
| Fichero | Contenido |
| --- | --- |
| `matriz_evaluacion.csv` | Una fila por métrica: característica, prioridad, métrica, medida automática (si existe), umbral y cómo se obtiene |
| `matriz.py` | Ejecuta las medidas automatizables y marca el resto como pendiente |

## 🔍 Qué observar

```
  📊 Métricas evaluadas automáticamente: 6/11  ·  cumplen: 2/6
  🎯 Características priorizadas con al menos una medida: 5/10
```

- Las filas **sin `medida_id`** (credibilidad, trazabilidad, comprensibilidad, accesibilidad, disponibilidad) quedan como **«pendiente»**, con la forma de obtenerlas: inspección documental, revisión de metadatos, prueba de acceso, monitorización…
- Un informe que dijera «todo OK» con la mitad de las características sin medir **engañaría**. La cobertura lo hace visible.

## 🔗 Conexión con `07-DCAT`
La **accesibilidad** (¿responde la URL de descarga?) y la **trazabilidad** (¿hay publicador y contacto?) se evalúan sobre los **metadatos del catálogo**. Es exactamente lo que comprueba el laboratorio de `07-DCAT`.

## 🏋️ Ejercicios
1. 🟢 Cambia un umbral en el CSV y comprueba cómo cambia el resultado.
2. 🟡 Añade una fila de **precisión** para PM10 (necesitarás la medida; ver `comun/README.md`).
3. 🔴 Automatiza la medida de **accesibilidad**: comprueba con `urllib` que la URL de descarga del catálogo responde.

➡️ Siguiente: [`05-Reglas-DMN4DQ`](../05-Reglas-DMN4DQ/) — cómo expresar las reglas y decidir.
