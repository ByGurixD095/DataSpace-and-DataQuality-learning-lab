# 01 · RDF (Resource Description Framework)

Tres grafos en **Turtle (`.ttl`)** que recorren RDF de menos a más, usando **solo RDF puro**: no hay RDFS ni OWL. Esos dos tienen su propio espacio en el repositorio (`02-RDFS`, `03-OWL`).

Los tres grafos comparten el mismo mini-dominio (personas, datasets y mediciones de calidad de un pequeño espacio de datos) para que se vea cómo **el mismo contenido se puede expresar con más potencia** a medida que subes de nivel.

## Contenido

| Fichero | Nivel | Triples | Idea central |
|---|---|---|---|
| [`01-basico.ttl`](01-basico.ttl) | Básico | 14 | La triple: sujeto, predicado, objeto |
| [`02-intermedio.ttl`](02-intermedio.ttl) | Intermedio | 43 | Sintaxis expresiva y tipos de nodos y valores |
| [`03-avanzado.ttl`](03-avanzado.ttl) | Avanzado | 76 | El vocabulario propio de RDF (`rdf:`) |

## Qué significa «solo RDF»

- Se usa el namespace `rdf:` (`rdf:type`, `rdf:Statement`, `rdf:Bag`, `rdf:first`...) y los tipos de dato `xsd:`.
- **No** se usa `rdfs:` (`rdfs:Class`, `rdfs:label`, `rdfs:domain`...) ni `owl:`.
- Por eso las clases y propiedades del dominio (`ex:Persona`, `ex:Dataset`, `ex:trabajaCon`...) **no se declaran**: son simplemente IRIs que se usan. Declararlas formalmente es trabajo de RDFS/OWL.
- En Turtle, los comentarios (`# ...`) sustituyen a `rdfs:comment` para explicar el contenido.

---

## Nivel 1 · Básico

**Objetivo:** entender la unidad mínima de RDF, la triple `sujeto → predicado → objeto`.

**Qué contiene**
- Recursos identificados por IRI (`ex:Gonzalo`, `ex:DatasetClientes`).
- Tipos con `rdf:type`.
- Relaciones entre recursos (`ex:trabajaCon`, `ex:derivadoDe`).
- Propiedades con literales simples (`"CSV"`, `"Clientes"`).

**Cómo está escrito:** una triple por línea, sin abreviaturas. Así cada línea es literalmente una arista del grafo.

```
Gonzalo ──trabajaCon──▶ Lucia ──esResponsableDe──▶ DatasetVentas
   │                                                    │
   └──haCreado──▶ DatasetClientes ◀──derivadoDe─────────┘
```

**Conceptos que debes llevarte**
- Un grafo RDF es un conjunto de triples; el orden no importa.
- El objeto puede ser un recurso (IRI) o un literal.

---

## Nivel 2 · Intermedio

**Objetivo:** escribir RDF de forma compacta y usar los distintos tipos de nodos y valores.

**Qué contiene**

| Sección | Concepto |
|---|---|
| 1 | Abreviaturas de Turtle: `a` (= `rdf:type`), `;` (mismo sujeto), `,` (mismo sujeto y predicado) |
| 2 | Literales con tipo: `xsd:integer`, `xsd:decimal`, `xsd:double`, `xsd:boolean`, `xsd:date`, `xsd:dateTime` |
| 3 | Literales con idioma: `"Clientes"@es`, `"Customers"@en` |
| 4 | Nodos anónimos (*blank nodes*): sintaxis `[ ... ]` y etiquetas `_:auditoria1` |
| 5 | Colecciones ordenadas `( ... )` y la colección vacía `()` |
| 6 | Literales multilínea (`"""..."""`) y caracteres escapados |
| 7 | `@base` e IRIs relativas (`<Lucia>`) |

**Conceptos que debes llevarte**
- Los literales numéricos sin comillas (`12500`, `0.97`, `false`) son atajos de tipos `xsd`.
- Un nodo anónimo es un recurso sin IRI, útil para agrupar datos que no necesitan identidad propia.
- `( a b c )` es azúcar sintáctico de una estructura interna que se ve en el nivel avanzado.

---

## Nivel 3 · Avanzado

**Objetivo:** usar el vocabulario propio de RDF para modelar lo que las triples simples no permiten.

**Qué contiene**

| Sección | Concepto | Para qué sirve |
|---|---|---|
| 1 | `rdf:Property` | Declarar propiedades sin recurrir a RDFS |
| 2 | Reificación (`rdf:Statement`, `rdf:subject`, `rdf:predicate`, `rdf:object`) | Hablar **sobre** una triple: quién la midió, cuándo, con qué confianza |
| 3 | Contenedores `rdf:Bag`, `rdf:Seq`, `rdf:Alt` (`rdf:_1`, `rdf:_2`...) | Grupos sin orden, con orden y alternativas |
| 4 | Listas explícitas (`rdf:first`, `rdf:rest`, `rdf:nil`) | Ver por dentro lo que genera `( ... )`, y listas anidadas |
| 5 | `rdf:value` | Valores estructurados: cantidad + unidad + precisión |
| 6 | Literales especiales: `rdf:JSON`, `rdf:HTML`, `rdf:XMLLiteral`, `rdf:langString` | Incrustar JSON, HTML o XML como valor |

**Conceptos que debes llevarte**
- **La reificación no afirma la triple original.** En el fichero, `ex:medicion1` describe una triple que además está escrita aparte; `ex:medicion2` describe una que *no* está en el grafo.
- Los contenedores son una convención abierta (se pueden ampliar desde otro documento); las listas `rdf:first/rest/nil` son cerradas.
- `rdf:langString` es el tipo implícito de todo literal con idioma; en Turtle no se escribe explícitamente.

**Enlace con calidad del dato:** la reificación de este nivel es la base de anotar mediciones de calidad (valor medido, herramienta, fecha, confianza), algo que se retoma en `08-Data-Quality`.


## Ejercicios propuestos

1. En el nivel básico, añade una persona y un dataset nuevos y conéctalos con al menos tres triples.
2. Reescribe el nivel básico usando `a`, `;` y `,` y comprueba con rdflib que el número de triples no cambia.
3. En el intermedio, añade un título en un cuarto idioma y comprueba con rdflib cuántas triples nuevas aparecen.
4. En el avanzado, reifica otra medición (por ejemplo, exactitud) y decide si además debes escribir la triple original.
5. Convierte la lista de `ex:columnas` del avanzado (sección 4.a) a la sintaxis `( ... )` y comprueba que el grafo resultante es equivalente.

## Siguiente paso

Cuando estos grafos te resulten cómodos, pasa a `02-RDFS`: allí se declaran formalmente clases y propiedades (`rdfs:Class`, `rdfs:domain`, `rdfs:range`) sobre este mismo tipo de datos.
