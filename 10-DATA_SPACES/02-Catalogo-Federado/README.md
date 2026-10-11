# 📚 02 · Catálogo federado

> **Idea:** cada proveedor publica **su** catálogo; el consumidor los consulta como uno solo sin perder de quién viene cada oferta.

## 🎯 Qué aprenderás
- Un **grafo con nombre** por participante (`urn:espacio:catalogo:<id>`) en un `Dataset` de rdflib.
- Una única consulta SPARQL con `GRAPH ?g` que devuelve el origen de cada resultado.
- Filtrar por **finalidad permitida** (ODRL), **calidad** (DQV) y **clasificación**.
- Que un dataset sin metadatos completos es, en la práctica, **invisible**.

## ▶️ Ejecutar
```bash
python catalogo_federado.py
python catalogo_federado.py --finalidad docencia --min-calidad 0.9
python catalogo_federado.py --proveedor empresa-movilidad --clasificacion Interno
```
Genera `federado.trig`.

## ⚠️ Matiz
Esto es una consulta sobre grafos **locales**. Un espacio real federa catálogos de participantes **distintos** a través del protocolo de catálogo; aquí solo se ilustra la parte semántica.

## 🧪 Prueba tú
1. Quita la calidad de un dataset de `datos/ofertas.csv` y observa que desaparece del resultado.
2. Escribe una consulta que devuelva el nº de ofertas por proveedor (`GROUP BY ?g`).

## ➡️ Siguiente
[`01-Mini-Espacio-Simulado`](../01-Mini-Espacio-Simulado/): todo junto.
