# 🏛️ 06 · Gobierno de espacios de datos

> **Idea:** en un espacio de datos nadie manda solo. La **autoridad de gobernanza** aprueba un **rulebook** y cada participante se **adhiere** cumpliéndolo.

## 🎯 Qué aprenderás
- Reglas **obligatorias** vs **recomendadas**, y reglas condicionales (DPD solo si se tratan datos personales).
- Reglas distintas según el **rol** (proveedor / consumidor).
- La decisión de adhesión: ❌ no admitido · ⚠️ admitido con recomendaciones · ✅ admitido.

## ▶️ Ejecutar
```bash
python espacio.py                                    # evalúa los 5 participantes
python espacio.py --participante startup-analitica
python espacio.py --rulebook
python espacio.py --alta                             # cuestionario interactivo
```
Solo usa la biblioteca estándar.

## ⚠️ Aviso
El rulebook es **inventado y didáctico**. Uno real lo define la autoridad de gobernanza del espacio (ver el DSSC Blueprint) y suele incluir aspectos jurídicos, de confianza e interoperabilidad que aquí se simplifican.

## 🧪 Prueba tú
1. Añade una regla R11 en `rulebook.json` y un campo en `participantes.csv`.
2. Haz obligatoria R07 (calidad publicada): ¿quién deja de entrar?

## ➡️ Siguiente
Vuelve al [README de 09](../README.md) y continúa con el siguiente módulo del laboratorio.
