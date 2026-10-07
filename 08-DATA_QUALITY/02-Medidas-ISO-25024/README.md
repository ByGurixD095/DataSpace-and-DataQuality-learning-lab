# 📏 02 · Medidas ISO/IEC 25024

**Cada medida es un ratio `cumplen / total`. Aquí las calculas sobre un dataset con defectos conocidos.**

## 🎯 Qué aprendes
- A expresar una medida como **ratio** y a asociarla a una **característica** del modelo.
- Que una misma característica admite **varias medidas** (consistencia: coherencia entre atributos *y* unicidad).
- Que **medir no es decidir**: la norma no fija umbrales.

## ▶️ Ejecutar (solo biblioteca estándar)

```bash
python medir.py
python medir.py --ahora 2026-10-06T10:00     # la actualidad cambia con la fecha de referencia
python medir.py --json                        # salida legible por máquinas
```

## 🔍 Salida esperada

```
  medida             característica 25012 cumplen/total    valor  gráfico
  completitud_no2    Completitud         47/50       94.0%  ███████████████████░
  validez_no2        Exactitud           45/50       90.0%  ██████████████████░░
  consistencia_pm    Consistencia        48/50       96.0%  ███████████████████░
  unicidad_clave     Consistencia        48/50       96.0%  ███████████████████░
  precision_no2      Precisión           44/47       93.6%  ███████████████████░
  actualidad_24h     Actualidad           1/1       100.0%  ████████████████████
  actualidad_3h      Actualidad           1/1       100.0%  ████████████████████
```

Cada cifra coincide con los defectos documentados en [`datos/`](../datos/): 3 vacíos → 47/50; 3 vacíos + 2 fuera de rango → 45/50; 2 duplicados → 48/50…

## 💡 Cosas que conviene notar
- **El denominador importa.** La precisión se calcula sobre los 47 valores *presentes* (no sobre 50): si dividieras entre 50 penalizarías dos veces el mismo defecto.
- **La actualidad es un caso aparte:** con `--ahora 2026-10-06T10:00`, `actualidad_3h` pasa a 0 mientras `actualidad_24h` sigue en 1. El dato es el mismo; lo que cambia es el **momento**.
- `unicidad_clave` no es una característica de ISO/IEC 25012: se mapea a **consistencia** (mapeo habitual, no literal).

## 🏋️ Ejercicios
1. 🟢 Ejecuta con `--ahora` dos días después y explica qué medidas cambian.
2. 🟡 Añade una medida de **precisión** para PM10 (ver `comun/README.md`).
3. 🟡 Calcula a mano la validez si el rango válido del NO₂ fuera [0, 200]. Comprueba con el script.
4. 🔴 Implementa una medida de **conformidad**: porcentaje de `fecha_hora` que cumple el formato ISO 8601.

➡️ Siguiente: [`03-Proceso-ISO-25040`](../03-Proceso-ISO-25040/) — cómo se organiza una evaluación completa.
