# 📊 05 · Cobertura de gobierno

> **Idea:** lo que no se mide no se gobierna. Dos miradas al mismo problema: **SHACL** (¿cumple cada dataset?) y **SPARQL** (¿qué porcentaje cumple?).

## 🎯 Qué aprenderás
- Reglas de gobierno como shapes (`Violation` = bloquea, `Warning` = recomienda).
- Indicadores de cobertura con SPARQL y **verificación cruzada** SPARQL ↔ SHACL.
- Un **plan de remediación** priorizado y por qué **no se pueden inventar propietarios** para mejorar un KPI.

## ▶️ Ejecutar
```bash
python cobertura.py
python cobertura.py --asignar-por-defecto   # sube el KPI… sin gobernar nada
python cobertura.py --fecha 2027-01-01      # la revisión vigente cambia con la fecha
```

## 👀 Resultados esperados (fecha 2026-10-08)
Propietario 8/10 · steward 8/10 · custodio 9/10 · clasificados 9/10 · política 6/10 · calidad 3/10 · revisión 7/10. SHACL: 5 violaciones y 15 avisos. Sale con código 1 si hay violaciones.

## 📂 Archivos
`shapes/gobierno.shacl.ttl` (reglas) y `cobertura.py` (SHACL + SPARQL + informe).

## ➡️ Siguiente
[`06-Gobierno-de-Espacios-de-Datos`](../06-Gobierno-de-Espacios-de-Datos/)
