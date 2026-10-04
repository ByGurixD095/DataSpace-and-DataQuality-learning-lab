# 🧪 Ejemplos jugables de SHACL

Tres niveles para **ejecutar** lo que explica el [README de SHACL](../README.md).
Cada carpeta tiene lo mismo:

| Archivo       | Qué es                                          |
|---------------|-------------------------------------------------|
| `shapes.ttl`  | Shapes Graph (las reglas)                       |
| `valid.ttl`   | Data Graph que **debe** cumplirlas              |
| `invalid.ttl` | Data Graph que **debe** romperlas (cada caso comentado) |

## ▶️ Cómo ejecutarlos

```bash
pip install pyshacl rdflib
python validate.py        # los tres niveles
python validate.py 02     # solo el intermedio
```

## 🗺️ Qué contiene cada nivel

| Nivel | Ejemplo | Conceptos del README que se ven en acción |
|-------|---------|-------------------------------------------|
| `01-Basico` | Personas | `targetClass`, `minCount`/`maxCount`, `datatype`, rangos, `pattern`, caso límite |
| `02-Intermedio` | Datasets (solución del ejercicio 31) | `sh:in`, `xsd:date`, `sh:or`, `sh:node` (shape reutilizada), propiedades opcionales |
| `03-Calidad-y-Data-Spaces` | Registros de movilidad | `sh:severity` (Violation / Warning / Info), `sh:message` por dimensión de calidad, `sh:sparql` |

## 🔗 SHACL dentro del resto del laboratorio

SHACL no vive aislado; estos ejemplos enlazan con otras carpetas del repo:

- **Data Quality** → en el nivel 3 cada mensaje lleva la dimensión ISO/IEC 25012 que comprueba
  (`[Completitud]`, `[Precisión sintáctica]`, `[Consistencia]`…) y `validate.py` agrupa los resultados por dimensión.
- **SPARQL (`04-SPARQL`)** → la regla "el fin no puede ser anterior al inicio" no se puede expresar en SHACL Core;
  se resuelve con una consulta SPARQL dentro de la shape (`sh:sparql`).
- **Data Spaces** → el perfil de movilidad es el tipo de requisito que un proveedor tendría que cumplir antes
  de publicar un dataset: Violation = se rechaza, Warning/Info = se acepta con aviso.

## 📝 Qué deberías ver

- `valid.ttl` → `conforms = True` en los tres niveles.
- `01-Basico/invalid.ttl` → 8 resultados. **Bob** aparece 3 veces en `age`: `"twenty"` incumple a la vez
  el datatype y los dos rangos (una misma propiedad puede romper varias restricciones).
- `02-Intermedio/invalid.ttl` → 9 resultados, incluido uno de `SinNombre`, que se valida **a través** de `sh:node`.
- `03-.../invalid.ttl` → 4 Violation, 1 Warning y 1 Info. Ojo: con `allow_warnings=False` `conforms` sale `False`
  igualmente; si quieres que solo bloqueen las Violation, pon `allow_warnings=True` en `validate.py`.

## 🚀 Para ampliar

1. Añade un caso límite en el nivel 3 (`speedKmh 120`, `lat 90`) y comprueba que **no** salta nada.
2. Pasa un `invalid.ttl` por `pyshacl` desde la CLI: `pyshacl -s shapes.ttl -f human invalid.ttl`.
3. Intenta modelar en SHACL una regla de tu TFG y mira si necesita Core o SPARQL.
