# 🌐 SPARQL Endpoint

```text
Cliente ── HTTP + consulta ──▶ Endpoint ──▶ Dataset RDF
        ◀── JSON / CSV / XML ──
```

**SPARQL como lenguaje** → lo que escribes (`SELECT …`).
**SPARQL como servicio** → un servidor HTTP que recibe esa consulta y devuelve los resultados.

| Archivo | Qué es |
|---------|--------|
| `servidor.py` | Endpoint de juguete (RDFLib + `http.server`) en `http://localhost:3030/sparql` |
| `cliente.py` | Cliente Python (solo biblioteca estándar) |
| `Cliente.java` | Cliente Java (solo JDK, `java.net.http`) |

## ▶️ Probar

```bash
# Terminal 1
pip install rdflib
python servidor.py

# Terminal 2
python cliente.py
java Cliente.java
```

También con `curl`:

```bash
curl -G http://localhost:3030/sparql \
     -H "Accept: text/csv" \
     --data-urlencode "query=SELECT ?s WHERE { ?s a <http://example.org/Ciudad> }"
```

## 📦 El protocolo en 3 ideas

1. La consulta viaja en `GET ?query=…` o en un `POST`.
2. El **formato de los resultados** lo elige la cabecera `Accept`:

   | Accept | Formato |
   |--------|---------|
   | `application/sparql-results+json` | JSON |
   | `application/sparql-results+xml` | XML |
   | `text/csv` · `text/tab-separated-values` | CSV · TSV |

3. Un `SELECT` en JSON tiene la forma `{"head": {"vars": [...]}, "results": {"bindings": [...]}}` y un `ASK`, `{"boolean": true}`.

## 🔁 Con un endpoint real

Los clientes funcionan igual contra **Apache Jena Fuseki** (u otro triplestore): crea un dataset, sube
`../datos/personas.ttl` y ejecuta `python cliente.py http://localhost:3030/NOMBRE_DATASET/sparql`.
Los endpoints reales también aceptan **SPARQL Update** (en otra URL, normalmente `/update`), que este servidor de juguete no implementa.

## 🎮 Retos

1. Pide el resultado en XML (`application/sparql-results+xml`) y léelo con `xml.etree`.
2. Lanza una consulta mal escrita y observa el código HTTP 400.
3. Haz que `cliente.py` reciba la consulta como argumento de línea de comandos.
