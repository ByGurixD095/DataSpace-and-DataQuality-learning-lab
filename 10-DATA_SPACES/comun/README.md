# 🧰 comun/

`espacio.py` es la biblioteca compartida por los cinco experimentos.

| Función | Qué hace |
| --- | --- |
| `participantes`, `ofertas`, `rulebook`, `revocadas` | Leen `datos/` |
| `catalogo_rdf`, `catalogos_federados` | Catálogo DCAT de un proveedor (con oferta ODRL y calidad DQV) y conjunto de grafos con nombre |
| `evaluar_participante`, `derivados_proveedor` | Rulebook aplicado; R05–R07 derivadas de los metadatos |
| `emitir_credencial`, `verificar_credencial` | Credencial de adhesión firmada con Ed25519 |
| `evaluar_peticion`, `acuerdo_rdf` | Petición contra una `odrl:Offer`; creación del `odrl:Agreement` |

Fecha de referencia fija: `2026-10-08`. Requiere `rdflib` y `cryptography`.
La clave de la autoridad sale de una **semilla fija** solo para ser reproducible: no es un patrón para sistemas reales.
