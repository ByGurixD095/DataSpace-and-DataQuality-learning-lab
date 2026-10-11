# ✅ 05 · Rulebook y conformidad

> **Idea:** un rulebook que solo se rellena de buena fe no protege a nadie. Con SHACL, **se comprueba**: lo que un proveedor publica de verdad decide si cumple.

## 🎯 Qué aprenderás
- El rulebook de `09` convertido en **shapes SHACL** (Violation = bloquea, Warning = recomienda).
- Reglas **derivadas**: R05–R07 salen de validar las ofertas, no de lo que el participante declara.
- Regla condicional (R03: DPD solo si trata datos personales) con `sh:or`.
- **Verificación cruzada**: la decisión de SHACL debe coincidir con la del rulebook en Python.

## ▶️ Ejecutar
```bash
python conformidad.py
python conformidad.py --participante empresa-movilidad
```
Sale con código 1 si hay violaciones.

## 👀 Qué verás
- `rutas-bus` no es publicable (sin clasificación ni oferta) → `empresa-movilidad` incumple R05 y R06.
- `startup-analitica` incumple R03 (trata datos personales sin DPD).
- Ayuntamiento y universidad entran sin problema.

## 📂 Archivos
`shapes/ofertas.shacl.ttl` (qué se puede publicar), `shapes/participantes.shacl.ttl` (rulebook) y `conformidad.py`.

## 🧪 Prueba tú
1. Completa `rutas-bus` en `datos/ofertas.csv` y comprueba que `empresa-movilidad` entra.
2. Convierte R10 en obligatoria en `rulebook.json` y en la shape: ¿quién deja de entrar?

## ➡️ Siguiente
[`04-Confianza-y-Credenciales`](../04-Confianza-y-Credenciales/): ¿cómo demuestra un participante que fue admitido?
