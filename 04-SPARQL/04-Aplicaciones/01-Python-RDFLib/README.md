# 🐍 Python + RDFLib

```text
Python → RDFLib → Graph → SPARQL → Resultados
```

| Archivo | Muestra |
|---------|---------|
| `01_consulta.py` | Cargar un grafo, `SELECT`, recorrer filas, consultas parametrizadas (`initBindings`), resultados → JSON |
| `02_modificar.py` | `g.add`, SPARQL Update, `ASK`, `CONSTRUCT` |

```bash
pip install rdflib
python 01_consulta.py
python 02_modificar.py
```

## Ideas clave

* `Graph.parse()` carga; `Graph.query()` consulta; `Graph.update()` modifica.
* Cada fila es accesible por el nombre de la variable (`fila.nombre`); un literal se convierte con `.toPython()`.
* Si una variable no tiene valor (`OPTIONAL`), su valor es `None`.

## 🎮 Retos

1. Añade a `01_consulta.py` una consulta que devuelva la edad media por ciudad.
2. Haz que `ciudad` se pida por `input()`.
3. Guarda el resultado de una consulta en un CSV con el módulo `csv`.
