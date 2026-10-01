# 🔎 04 · SPARQL — Query Language for RDF

> Guía de referencia y aprendizaje progresivo para consultar, filtrar, combinar y transformar datos almacenados en grafos RDF mediante SPARQL.

![Nivel](https://img.shields.io/badge/nivel-básico%20→%20avanzado-blue?style=flat-square)
![Estándar](https://img.shields.io/badge/estándar-W3C-005a9c?style=flat-square)
![Lenguaje](https://img.shields.io/badge/lenguaje-SPARQL%201.1-orange?style=flat-square)
![Lectura](https://img.shields.io/badge/lectura-~15%20min-lightgrey?style=flat-square)

---

## 📑 Contenido

- [🔎 04 · SPARQL — Query Language for RDF](#-04--sparql--query-language-for-rdf)
  - [📑 Contenido](#-contenido)
  - [1 · ¿Qué es SPARQL?](#1--qué-es-sparql)
  - [2 · ¿Por qué necesitamos SPARQL?](#2--por-qué-necesitamos-sparql)
  - [3 · ¿Cómo funciona una consulta SPARQL?](#3--cómo-funciona-una-consulta-sparql)
  - [4 · Formas de trabajar con SPARQL](#4--formas-de-trabajar-con-sparql)
    - [4.1 · Consolas y herramientas gráficas](#41--consolas-y-herramientas-gráficas)
    - [4.2 · Python](#42--python)
    - [4.3 · Java](#43--java)
    - [4.4 · Endpoints SPARQL](#44--endpoints-sparql)
  - [5 · Anatomía de una consulta](#5--anatomía-de-una-consulta)
  - [6 · Tipos de consultas SPARQL](#6--tipos-de-consultas-sparql)
  - [7 · Ejemplo conceptual](#7--ejemplo-conceptual)
  - [8 · Ruta de aprendizaje](#8--ruta-de-aprendizaje)
    - [🟢 Nivel básico](#-nivel-básico)
    - [🟡 Nivel intermedio](#-nivel-intermedio)
    - [🔴 Nivel avanzado](#-nivel-avanzado)
  - [9 · Conceptos clave para recordar](#9--conceptos-clave-para-recordar)
  - [10 · Cheat Sheet](#10--cheat-sheet)
  - [11 · Recursos y siguiente paso](#11--recursos-y-siguiente-paso)

---

## 1 · ¿Qué es SPARQL?

**SPARQL** (*SPARQL Protocol and RDF Query Language*) es un lenguaje de consulta diseñado para trabajar con datos representados como **RDF**.

Mientras que RDF permite representar información mediante triples:

```text
Sujeto ─── Predicado ─── Objeto
```

SPARQL permite **buscar patrones dentro de esos triples**.

Por ejemplo, dado:

```turtle
ex:Ana a ex:Persona ;
       ex:nombre "Ana" ;
       ex:edad 22 .

ex:Carlos a ex:Persona ;
         ex:nombre "Carlos" ;
         ex:edad 25 .
```

Podemos preguntar:

> ¿Qué personas existen y cuál es su nombre?

Con SPARQL:

```sparql
SELECT ?persona ?nombre
WHERE {
    ?persona a ex:Persona ;
             ex:nombre ?nombre .
}
```

El resultado sería:

```text
persona       nombre
--------------------
ex:Ana        "Ana"
ex:Carlos     "Carlos"
```

> 📌 **Idea clave:** SPARQL no consulta tablas como SQL; consulta **patrones de triples dentro de un grafo RDF**.

---

## 2 · ¿Por qué necesitamos SPARQL?

En RDF y OWL hemos aprendido a **representar conocimiento**.

- RDF → representa información mediante triples.
- RDFS → añade clases, jerarquías, dominios y rangos.
- OWL → añade una semántica lógica más expresiva y permite razonamiento.
- SPARQL → permite **consultar ese conocimiento**.

Podemos verlo como una evolución:

```text
RDF
 │
 │  Representar datos
 ▼
RDFS
 │
 │  Añadir estructura y vocabulario
 ▼
OWL
 │
 │  Añadir semántica y restricciones
 ▼
SPARQL
 │
 │  Consultar y obtener información
 ▼
Resultados
```

Por ejemplo, una ontología puede definir:

```text
Persona
 ├── Profesor
 └── Estudiante
```

y SPARQL permite preguntar:

```text
¿Qué profesores existen?
¿Qué estudiantes tienen más de 20 años?
¿Qué profesores tutorizan a cada estudiante?
¿Qué personas pertenecen a una determinada clase?
```

Esto resulta especialmente útil cuando trabajamos con:

- Ontologías.
- Knowledge Graphs.
- Linked Data.
- Data Spaces.
- Catálogos RDF.
- Metadatos.
- Sistemas de integración de datos.

---

## 3 · ¿Cómo funciona una consulta SPARQL?

Una consulta SPARQL busca **patrones que coincidan con los triples existentes en el grafo**.

Supongamos:

```turtle
ex:Ana a ex:Persona ;
       ex:nombre "Ana" ;
       ex:trabajaEn ex:Universidad .

ex:Carlos a ex:Persona ;
         ex:nombre "Carlos" ;
         ex:trabajaEn ex:Empresa .
```

Podemos representar la consulta:

```sparql
SELECT ?persona
WHERE {
    ?persona a ex:Persona .
}
```

Como un patrón:

```text
?persona ─── rdf:type ─── ex:Persona
```

SPARQL intenta encontrar todos los recursos que encajen con ese patrón.

Obtendremos:

```text
?persona
---------
ex:Ana
ex:Carlos
```

### Variables

Las variables comienzan por:

```text
?
```

o:

```text
$
```

Por ejemplo:

```text
?persona
?nombre
?edad
```

Una variable representa una posición desconocida que queremos obtener o utilizar dentro de la consulta.

---

## 4 · Formas de trabajar con SPARQL

SPARQL no implica necesariamente utilizar una herramienta concreta.

Podemos trabajar con consultas de distintas formas dependiendo del objetivo.

### 4.1 · Consolas y herramientas gráficas

La forma más sencilla de empezar es utilizar una herramienta que permita escribir consultas directamente sobre un grafo RDF.

El flujo suele ser:

```text
Grafo RDF
   │
   ▼
Motor SPARQL
   │
   ▼
Consulta SPARQL
   │
   ▼
Resultados
```

Es especialmente útil para:

- Aprender SPARQL.
- Probar consultas.
- Explorar una ontología.
- Depurar patrones.
- Comprobar qué datos existen.

Algunos sistemas que pueden proporcionar esta funcionalidad son:

- Apache Jena / Fuseki.
- GraphDB.
- Virtuoso.
- Stardog.
- RDF4J.

---

### 4.2 · Python

También podemos ejecutar consultas SPARQL desde Python.

Una opción habitual es trabajar con **RDFLib**, que permite manipular grafos RDF y ejecutar consultas SPARQL.

Ejemplo conceptual:

```python
from rdflib import Graph

g = Graph()

g.parse("universidad.ttl", format="turtle")

query = """
PREFIX ex: <http://example.org/universidad#>

SELECT ?persona ?nombre
WHERE {
    ?persona a ex:Persona ;
             ex:nombre ?nombre .
}
"""

for row in g.query(query):
    print(row.persona, row.nombre)
```

El flujo sería:

```text
archivo RDF
    │
    ▼
RDFLib
    │
    ▼
Graph
    │
    ▼
SPARQL
    │
    ▼
Resultados Python
```

Esto permite integrar consultas RDF dentro de aplicaciones, scripts y procesos de análisis.

---

### 4.3 · Java

En Java existen diferentes frameworks para trabajar con RDF y SPARQL.

Uno de los más conocidos es **Apache Jena**.

El concepto es similar:

```text
Aplicación Java
      │
      ▼
   RDF Model
      │
      ▼
 SPARQL Query
      │
      ▼
 ResultSet
```

Un ejemplo simplificado:

```java
String queryString = """
    PREFIX ex: <http://example.org/universidad#>

    SELECT ?persona ?nombre
    WHERE {
        ?persona a ex:Persona ;
                 ex:nombre ?nombre .
    }
    """;
```

Posteriormente, el framework ejecuta esa consulta sobre el modelo RDF o sobre un endpoint SPARQL.

> 📌 **Idea clave:** SPARQL es el lenguaje de consulta. Python, Java, Jena, RDFLib, GraphDB, Fuseki, etc. son herramientas o entornos que permiten ejecutarlo.

---

### 4.4 · Endpoints SPARQL

Otra posibilidad es consultar un grafo que está expuesto mediante un **SPARQL Endpoint**.

En este caso, los datos no tienen por qué estar almacenados localmente.

El flujo puede ser:

```text
Aplicación
    │
    │ HTTP
    ▼
SPARQL Endpoint
    │
    ▼
Knowledge Graph
    │
    ▼
Resultados
```

Una aplicación puede enviar una consulta SPARQL a un endpoint remoto y recibir los resultados.

Esto es especialmente importante en:

- Linked Data.
- Knowledge Graphs distribuidos.
- Integración de fuentes de datos.
- Data Spaces.
- Arquitecturas basadas en servicios.

---

## 5 · Anatomía de una consulta

La forma más habitual de una consulta `SELECT` es:

```sparql
PREFIX ex: <http://example.org/>

SELECT ?variable
WHERE {
    ?sujeto ex:propiedad ?variable .
}
```

Podemos dividirla en tres partes:

### `PREFIX`

Permite definir abreviaturas para URIs.

```sparql
PREFIX ex: <http://example.org/>
```

En lugar de escribir:

```text
http://example.org/Persona
```

podemos escribir:

```text
ex:Persona
```

---

### `SELECT`

Indica qué variables queremos obtener:

```sparql
SELECT ?persona ?nombre
```

---

### `WHERE`

Contiene los patrones que deben coincidir con el grafo:

```sparql
WHERE {
    ?persona ex:nombre ?nombre .
}
```

Por tanto:

```sparql
PREFIX ex: <http://example.org/>

SELECT ?persona ?nombre
WHERE {
    ?persona ex:nombre ?nombre .
}
```

puede leerse como:

> Busca las personas y sus nombres que coincidan con este patrón en el grafo.

---

## 6 · Tipos de consultas SPARQL

SPARQL no se limita a `SELECT`.

Las principales formas de consulta y modificación son:

| Forma | Uso |
|:------|:----|
| `SELECT` | Obtener variables como resultados tabulares |
| `CONSTRUCT` | Crear un nuevo grafo RDF a partir de una consulta |
| `ASK` | Comprobar si existe una coincidencia |
| `DESCRIBE` | Obtener una descripción de un recurso |
| `INSERT` | Añadir triples |
| `DELETE` | Eliminar triples |
| `DELETE/INSERT` | Modificar triples |

### `SELECT`

Es la forma más habitual para comenzar:

```sparql
SELECT ?persona
WHERE {
    ?persona a ex:Persona .
}
```

---

### `ASK`

Devuelve una respuesta booleana:

```sparql
ASK {
    ex:Ana a ex:Persona .
}
```

Resultado:

```text
true
```

o:

```text
false
```

---

### `CONSTRUCT`

Permite construir nuevos triples:

```sparql
CONSTRUCT {
    ?persona ex:esAdulto true .
}
WHERE {
    ?persona ex:edad ?edad .
    FILTER(?edad >= 18)
}
```

El resultado vuelve a ser RDF.

---

### `DESCRIBE`

Solicita una descripción de un recurso:

```sparql
DESCRIBE ex:Ana
```

El resultado dependerá del sistema SPARQL utilizado y de cómo construya la descripción.

---

## 7 · Ejemplo conceptual

Utilizaremos una pequeña ontología universitaria:

```turtle
@prefix ex: <http://example.org/universidad#> .

ex:Ana a ex:Profesor ;
       ex:nombre "Ana" ;
       ex:edad 45 .

ex:Carlos a ex:Estudiante ;
         ex:nombre "Carlos" ;
         ex:edad 21 .

ex:Laura a ex:Estudiante ;
        ex:nombre "Laura" ;
        ex:edad 24 .
```

Podemos empezar con una pregunta muy sencilla:

> ¿Qué estudiantes existen?

```sparql
PREFIX ex: <http://example.org/universidad#>

SELECT ?estudiante
WHERE {
    ?estudiante a ex:Estudiante .
}
```

Después podemos aumentar progresivamente la complejidad:

```text
1. Buscar recursos
       │
       ▼
2. Obtener propiedades
       │
       ▼
3. Filtrar resultados
       │
       ▼
4. Combinar varios patrones
       │
       ▼
5. Agrupar y calcular
       │
       ▼
6. Consultar estructuras opcionales
       │
       ▼
7. Trabajar con grafos
       │
       ▼
8. Construir/modificar RDF
```

Esta progresión será la base de los ejemplos de este apartado.

---

# 8 · Ruta de aprendizaje

Los ejemplos de SPARQL se organizan en tres niveles.

La idea no es aprender todas las funcionalidades de golpe, sino construir las consultas progresivamente.

---

## 🟢 Nivel básico

El objetivo es aprender a **leer un grafo y encontrar información**.

### Conceptos

- `PREFIX`
- `SELECT`
- `WHERE`
- Variables
- IRIs
- Literales
- Patrones de triples
- `rdf:type`
- `a`
- `FILTER`
- `ORDER BY`
- `LIMIT`
- `DISTINCT`

### Ejemplo

```sparql
PREFIX ex: <http://example.org/universidad#>

SELECT ?nombre
WHERE {
    ?persona ex:nombre ?nombre .
}
```

Después podemos filtrar:

```sparql
SELECT ?persona ?edad
WHERE {
    ?persona ex:edad ?edad .
    FILTER(?edad >= 18)
}
```

Y ordenar:

```sparql
SELECT ?persona ?edad
WHERE {
    ?persona ex:edad ?edad .
}
ORDER BY DESC(?edad)
```

### 🎯 Objetivo del nivel

Ser capaz de responder preguntas como:

```text
¿Qué personas existen?
¿Qué nombres tienen?
¿Qué edad tiene cada persona?
¿Qué personas tienen más de 20 años?
¿Cuáles son las personas más mayores?
```

---

## 🟡 Nivel intermedio

El objetivo es aprender a **combinar información y construir consultas más expresivas**.

### Conceptos

- Múltiples patrones de triples.
- `OPTIONAL`
- `UNION`
- `FILTER`
- `BIND`
- `VALUES`
- `REGEX`
- `GROUP BY`
- `COUNT`
- `SUM`
- `AVG`
- `MIN`
- `MAX`
- `HAVING`
- `ORDER BY`
- `OFFSET`

### Combinar patrones

```sparql
SELECT ?persona ?nombre ?edad
WHERE {
    ?persona a ex:Persona .
    ?persona ex:nombre ?nombre .
    ?persona ex:edad ?edad .
}
```

### `OPTIONAL`

Permite obtener información adicional cuando exista:

```sparql
SELECT ?persona ?nombre ?email
WHERE {
    ?persona ex:nombre ?nombre .

    OPTIONAL {
        ?persona ex:email ?email .
    }
}
```

### `UNION`

Permite combinar alternativas:

```sparql
SELECT ?persona
WHERE {
    {
        ?persona a ex:Profesor .
    }
    UNION
    {
        ?persona a ex:Estudiante .
    }
}
```

### Agregaciones

```sparql
SELECT (COUNT(?persona) AS ?total)
WHERE {
    ?persona a ex:Persona .
}
```

### 🎯 Objetivo del nivel

Ser capaz de responder preguntas como:

```text
¿Cuántas personas existen?
¿Cuántos estudiantes hay?
¿Qué personas tienen email?
¿Qué profesores o estudiantes existen?
¿Cuál es la edad media?
¿Cuántas personas pertenecen a cada categoría?
```

---

## 🔴 Nivel avanzado

El objetivo es utilizar SPARQL para **trabajar con estructuras RDF complejas, grafos y transformaciones de conocimiento**.

### Conceptos

- `CONSTRUCT`
- `ASK`
- `DESCRIBE`
- `INSERT`
- `DELETE`
- `GRAPH`
- `FROM`
- `FROM NAMED`
- `SERVICE`
- Subconsultas
- Property paths
- Consultas federadas
- Consultas sobre múltiples grafos
- Transformación RDF
- Actualización de datos

### Property Paths

Permiten consultar caminos dentro del grafo.

Por ejemplo:

```sparql
SELECT ?persona ?ancestro
WHERE {
    ?persona ex:tienePadre+ ?ancestro .
}
```

El operador:

```text
+
```

permite recorrer una o más relaciones consecutivas.

También existen otros operadores de caminos:

```text
/       Secuencia
|       Alternativa
*       Cero o más pasos
+       Uno o más pasos
?       Cero o uno
^       Dirección inversa
```

---

### Consultas federadas

SPARQL puede consultar diferentes fuentes mediante `SERVICE`.

Conceptualmente:

```sparql
SELECT ?persona
WHERE {
    SERVICE <endpoint> {
        ?persona a ex:Persona .
    }
}
```

Esto permite construir consultas sobre fuentes RDF distribuidas.

---

### `CONSTRUCT`

SPARQL también puede utilizarse para transformar información RDF:

```sparql
CONSTRUCT {
    ?persona ex:esAdulto true .
}
WHERE {
    ?persona ex:edad ?edad .
    FILTER(?edad >= 18)
}
```

Aquí SPARQL deja de utilizarse únicamente para obtener resultados tabulares y pasa a utilizarse para **generar nuevo RDF**.

### 🎯 Objetivo del nivel

Ser capaz de trabajar con preguntas como:

```text
¿Cómo puedo recorrer relaciones complejas?
¿Cómo puedo consultar diferentes grafos?
¿Cómo puedo consultar otro SPARQL Endpoint?
¿Cómo puedo generar RDF a partir de otros datos?
¿Cómo puedo modificar un grafo?
¿Cómo puedo combinar conocimiento procedente de diferentes fuentes?
```

---

# 9 · Conceptos clave para recordar

### 1. SPARQL trabaja sobre RDF

No debemos pensar inicialmente en:

```text
tabla → fila → columna
```

sino en:

```text
sujeto → predicado → objeto
```

---

### 2. Una consulta busca patrones

```sparql
?sujeto ex:p ?o .
```

significa:

> Busca triples cuyo predicado sea `ex:p` y devuelve el sujeto y el objeto.

---

### 3. Las variables empiezan por `?` o `$`

```sparql
?persona
?nombre
?edad
```

---

### 4. `SELECT` no modifica el grafo

Una consulta:

```sparql
SELECT ...
```

sirve para obtener resultados.

Las operaciones de actualización pertenecen a otra categoría:

```sparql
INSERT
DELETE
```

---

### 5. SPARQL puede devolver diferentes tipos de resultados

Dependiendo de la operación:

```text
SELECT    → Resultados tabulares
ASK       → Booleano
CONSTRUCT → RDF
DESCRIBE  → RDF
```

---

### 6. SPARQL y OWL cumplen funciones diferentes

```text
OWL
 │
 ├── Define clases
 ├── Define propiedades
 ├── Define restricciones
 └── Permite razonamiento
          │
          ▼
       RDF Graph
          │
          ▼
       SPARQL
          │
          ├── Consulta
          ├── Filtra
          ├── Combina
          └── Transforma
```

> 📌 **Idea clave:** OWL permite expresar qué significa el conocimiento; SPARQL permite preguntar y trabajar con ese conocimiento.

---

# 10 · Cheat Sheet

```text
PREFIX ex: <...>       → Define un prefijo

SELECT ?x              → Devuelve variables
WHERE { ... }          → Define patrones

?s ex:p ?o .           → Patrón de triple

a                      → Abreviatura de rdf:type

FILTER(...)            → Filtra resultados
OPTIONAL { ... }       → Patrón opcional
UNION                  → Combina alternativas
VALUES                 → Proporciona valores concretos
BIND(...)              → Crea una variable

ORDER BY               → Ordena
LIMIT                  → Limita resultados
OFFSET                 → Salta resultados
DISTINCT               → Elimina duplicados

GROUP BY               → Agrupa resultados
HAVING                 → Filtra grupos

COUNT()                → Cuenta
SUM()                  → Suma
AVG()                  → Media
MIN()                  → Mínimo
MAX()                  → Máximo

ASK { ... }             → ¿Existe coincidencia?
CONSTRUCT { ... }       → Genera RDF
DESCRIBE                → Describe un recurso

INSERT DATA { ... }     → Inserta RDF
DELETE DATA { ... }     → Elimina RDF

GRAPH                   → Trabaja con un grafo concreto
SERVICE                 → Consulta un endpoint externo

/                       → Camino secuencial
|                       → Alternativa
*                       → Cero o más pasos
+                       → Uno o más pasos
?                       → Cero o uno
^                       → Dirección inversa
```

---

# 11 · Recursos y siguiente paso

### Documentación y herramientas

- **W3C SPARQL** — Especificaciones oficiales del lenguaje.
- **Apache Jena / Fuseki** — Framework Java y servidor SPARQL.
- **RDFLib** — Librería Python para trabajar con RDF.
- **GraphDB** — Plataforma para almacenar y consultar grafos RDF.
- **Protégé** — Editor de ontologías útil para crear los grafos que posteriormente podremos consultar.

### Siguiente paso

Una vez comprendidos los conceptos básicos, el aprendizaje continúa mediante ejemplos prácticos:

```text
01 · Básico
    └── SELECT, WHERE, PREFIX, variables, filtros

02 · Intermedio
    └── OPTIONAL, UNION, agregaciones, agrupaciones

03 · Avanzado
    └── Property Paths, GRAPH, SERVICE, CONSTRUCT

04 · Aplicación
    └── Python / Java / SPARQL Endpoint

05 · Integración
    └── RDF + RDFS + OWL + SPARQL
```

El objetivo final es poder pasar de:

```text
"tengo una ontología y un grafo RDF"
```

a:

```text
"puedo formular preguntas sobre ese conocimiento,
obtener resultados y utilizar esos resultados
desde una aplicación."
```

➡️ **Siguiente paso:** [Ejemplos SPARQL — Nivel básico](./01-Basico/)
