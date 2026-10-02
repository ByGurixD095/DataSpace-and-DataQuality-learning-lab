# ☕ Java + Apache Jena

```text
Java → Apache Jena → Dataset/Model → SPARQL → Resultados
```

| Archivo | Muestra |
|---------|---------|
| `src/ConsultaSelect.java` | Cargar un `Model`, `SELECT`, recorrer `ResultSet`, `ASK` |
| `src/ActualizarDataset.java` | `Dataset`, `UpdateAction` (SPARQL Update), `CONSTRUCT` |

Requisitos: **Java 17+** y **Maven**.

```bash
cd 02-Java-Jena
mvn -q compile
mvn -q exec:java -Dexec.mainClass=ConsultaSelect
mvn -q exec:java -Dexec.mainClass=ActualizarDataset
```

> Ejecuta los comandos desde esta carpeta: las rutas (`../datos/personas.ttl`) son relativas.
> Maven descargará Jena la primera vez.
>
> 💡 El `pom.xml` ya indica `src/` como carpeta de código fuente.

## Ideas clave

| Jena | Equivale en RDFLib |
|------|--------------------|
| `Model` | `Graph` |
| `RDFDataMgr.loadModel()` | `Graph.parse()` |
| `QueryExecutionFactory.create()` + `execSelect()` | `Graph.query()` |
| `UpdateAction.parseExecute()` | `Graph.update()` |

* Un `QueryExecution` debe cerrarse: usa `try-with-resources`.
* `getLiteral("x")` falla con `null` si la variable no tiene valor (`OPTIONAL`): compruébalo con `fila.contains("x")`.

## 🎮 Retos

1. Imprime el resultado con `ResultSetFormatter.out(System.out, resultados)` en lugar de recorrerlo a mano.
2. Añade una consulta con `GROUP BY` (edad media por ciudad).
3. Guarda el modelo modificado con `RDFDataMgr.write(salida, modelo, Lang.TURTLE)`.
