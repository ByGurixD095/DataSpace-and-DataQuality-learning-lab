# 🧰 comun/

`gov.py` es la biblioteca compartida por los experimentos 02–05.

| Función | Qué hace |
| --- | --- |
| `cargar_inventario`, `cargar_csv` | Lee los CSV de `datos/` |
| `vocabulario_rdf` | Roles y clasificación como SKOS |
| `catalogo_rdf` | Inventario → catálogo DCAT con roles, clasificación, política y calidad |
| `indicadores`, `cobertura` | Indicadores de cobertura con SPARQL |
| `politicas_rdf`, `evaluar` | Políticas ODRL por nivel y evaluador mínimo |

Fecha de referencia fija: `2026-10-08` (reproducibilidad). Requiere `rdflib`.
