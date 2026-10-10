# 📇 03 · Catálogo y glosario

> **Idea:** el gobierno solo existe si **se ve**. El inventario se convierte en un catálogo DCAT donde propietario, steward, clasificación y revisión son datos consultables.

## 🎯 Qué aprenderás
- Expresar **roles** con `prov:qualifiedAttribution` + `dcat:hadRole`.
- Un **glosario SKOS** con un concepto por (término, dominio).
- Detectar **conflictos de definición** entre dominios: es un problema de gobierno, no técnico.

## ▶️ Ejecutar
```bash
python catalogo_gobernado.py                              # genera ficheros y detecta conflictos
python catalogo_gobernado.py --dataset trafico-horario    # ficha de gobierno
python catalogo_gobernado.py --termino "Estación activa"  # 2 definiciones → conflicto
```
Genera `catalogo_gobernado.ttl` y `glosario.ttl`.

## 🧪 Prueba tú
1. Edita `datos/glosario.csv` para unificar la definición de «Estación activa» y comprueba que el aviso desaparece.
2. Pide la ficha de `contratos-menores` y fíjate en todo lo que falta.

## ➡️ Siguiente
[`04-Linaje-PROV`](../04-Linaje-PROV/)
