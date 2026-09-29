# 🕸️ 01 · RDF — Resource Description Framework

> Guía práctica para entender, escribir y consultar datos en RDF, paso a paso.

![Nivel](https://img.shields.io/badge/nivel-introductorio-green?style=flat-square)
![Estándar](https://img.shields.io/badge/est%C3%A1ndar-W3C-005a9c?style=flat-square)
![Formato](https://img.shields.io/badge/formato-Turtle-orange?style=flat-square)
![Tiempo](https://img.shields.io/badge/lectura-~20%20min-lightgrey?style=flat-square)

---

## 📑 Contenido

1. [¿Qué es RDF?](#1--qué-es-rdf)
2. [La terna: la unidad básica](#2--la-terna-la-unidad-básica)
3. [Elementos clave](#3--elementos-clave)
4. [Formatos de serialización](#4--formatos-de-serialización)
5. [Ejemplo práctico en Turtle](#5--ejemplo-práctico-en-turtle)
6. [Consultas con SPARQL](#6--consultas-con-sparql)
7. [Pruébalo tú mismo](#7--pruébalo-tú-mismo)
8. [Ejercicios](#8--ejercicios)
9. [Errores frecuentes](#9--errores-frecuentes)
10. [Casos de uso](#10--casos-de-uso)
11. [Recursos y siguiente paso](#11--recursos-y-siguiente-paso)

---

## 1 · ¿Qué es RDF?

**RDF** es un estándar del **W3C** para modelar e intercambiar información en la Web.

A diferencia de las bases de datos relacionales (tablas) o de los documentos jerárquicos (JSON/XML puro), RDF modela los datos como un **grafo dirigido etiquetado**: los *nodos* son cosas y las *aristas* son las relaciones entre ellas.

| Modelo | Unidad básica | Estructura |
|:-------|:--------------|:-----------|
| Relacional | Fila | Tablas con esquema fijo |
| JSON / XML | Documento | Árbol jerárquico |
| **RDF** | **Terna** | **Grafo de afirmaciones** |

**¿Por qué importa?** Porque la información resulta **procesable por máquinas** y facilita la **interoperabilidad** entre sistemas distribuidos: dos organizaciones pueden describir sus datos con los mismos identificadores globales sin ponerse de acuerdo sobre un esquema de base de datos.

---

## 2 · La terna: la unidad básica

Toda afirmación en RDF se descompone en **tres partes** (*triple*):

```text
   Sujeto   ──── Predicado ────▶   Objeto
 (de quién)     (qué relación)     (qué valor)
```

| Parte | Qué es | Puede ser |
|:------|:-------|:----------|
| **Sujeto** *(subject)* | El recurso del que se habla | URI o nodo en blanco |
| **Predicado** *(predicate)* | La propiedad o relación | Siempre una URI |
| **Objeto** *(object)* | El valor de la propiedad | URI, nodo en blanco o literal |

Ejemplo en lenguaje natural: *"El dataset de sensores tiene como título 'Lecturas de Sensores 2026'"*.

```mermaid
graph LR
    S["ex:DatasetSensores<br/>(sujeto)"] -->|"dct:title<br/>(predicado)"| O["'Lecturas de Sensores 2026'@es<br/>(objeto)"]
```

Un conjunto de ternas forma un **grafo**. Ese es todo el modelo: no hay nada más.

---

## 3 · Elementos clave

### 🔗 URIs / IRIs
Identificadores **únicos y globales** que evitan colisiones de nombres.
Ejemplo: `http://schema.org/Person`.

### 🔤 Literales
Valores de datos primitivos. Pueden llevar **tipo de dato** o **etiqueta de idioma**:

```turtle
"42"^^xsd:integer          # número entero
"2026-09-29"^^xsd:date     # fecha
"Hola"@es                  # texto en español
```

### 👻 Nodos en blanco (*blank nodes*)
Recursos **anónimos** sin URI global. Sirven para agrupar datos locales o representar entidades que no necesitan un identificador público.

```turtle
ex:Sensor01 ex:ubicacion [
    ex:ciudad "Toledo" ;
    ex:pais   "España"
] .
```

### 📚 Vocabularios y ontologías
Conjuntos de URIs predefinidas para describir dominios concretos y **reutilizar** significado en lugar de inventarlo:

| Vocabulario | Prefijo | Sirve para |
|:------------|:-------:|:-----------|
| FOAF | `foaf:` | Personas y organizaciones |
| DCAT | `dcat:` | Catálogos y datasets |
| Dublin Core | `dct:` | Metadatos generales |

---

## 4 · Formatos de serialización

RDF es un **modelo abstracto**. Para guardarlo en ficheros o enviarlo por red se usan distintas sintaxis. Aquí, **la misma afirmación** en los cuatro formatos:

<details open>
<summary><b>Turtle</b> (<code>.ttl</code>) — compacto y legible</summary>

```turtle
@prefix ex:  <http://example.org/datos/> .
@prefix dct: <http://purl.org/dc/terms/> .

ex:DatasetSensores dct:title "Lecturas de Sensores 2026"@es .
```
</details>

<details>
<summary><b>N-Triples</b> (<code>.nt</code>) — una terna por línea</summary>

```text
<http://example.org/datos/DatasetSensores> <http://purl.org/dc/terms/title> "Lecturas de Sensores 2026"@es .
```
</details>

<details>
<summary><b>JSON-LD</b> (<code>.jsonld</code>) — RDF en sintaxis JSON</summary>

```json
{
  "@context": { "dct": "http://purl.org/dc/terms/" },
  "@id": "http://example.org/datos/DatasetSensores",
  "dct:title": { "@value": "Lecturas de Sensores 2026", "@language": "es" }
}
```
</details>

<details>
<summary><b>RDF/XML</b> (<code>.rdf</code>) — el formato original</summary>

```xml
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:dct="http://purl.org/dc/terms/">
  <rdf:Description rdf:about="http://example.org/datos/DatasetSensores">
    <dct:title xml:lang="es">Lecturas de Sensores 2026</dct:title>
  </rdf:Description>
</rdf:RDF>
```
</details>

| Formato | Legibilidad | Uso típico |
|:--------|:-----------:|:-----------|
| **Turtle** | ⭐⭐⭐ | Estándar de facto en repositorios y documentación |
| **JSON-LD** | ⭐⭐ | Desarrollo web y consumo de APIs |
| **N-Triples** | ⭐ | Procesamiento masivo y volcados de bases de datos |
| **RDF/XML** | ⭐ | Sistemas heredados; muy verboso para escribir a mano |

> 💡 **Los cuatro son equivalentes**: representan exactamente el mismo grafo.

---

## 5 · Ejemplo práctico en Turtle

Definimos un **catálogo de datos** y la **organización** que lo publica, usando DCAT, Dublin Core y FOAF.

```turtle
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct:  <http://purl.org/dc/terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix ex:   <http://example.org/datos/> .

# Sujeto: el conjunto de datos
ex:DatasetSensores a dcat:Dataset ;
    dct:title       "Lecturas de Sensores 2026"@es ;
    dct:description "Registro de temperatura y humedad."@es ;
    dct:issued      "2026-09-29"^^xsd:date ;
    dct:publisher   ex:InstitutoMeteorologico .

# Sujeto: la organización publicadora
ex:InstitutoMeteorologico a foaf:Organization ;
    foaf:name     "Instituto Meteorológico de Castilla-La Mancha" ;
    foaf:homepage <http://www.ejemplo-meteo.es> .
```

### 🧠 Cómo leerlo

- `@prefix` define **atajos** para no repetir URIs largas (`dct:title` = `http://purl.org/dc/terms/title`).
- `a` es la abreviatura de `rdf:type` ("es una instancia de").
- `;` encadena varias propiedades **sobre el mismo sujeto**.
- `,` (no usada aquí) encadena varios **objetos** para el mismo predicado.
- `dct:publisher ex:InstitutoMeteorologico` es lo que **conecta** los dos recursos: así se forma el grafo.

### 🗺️ El grafo resultante

```mermaid
graph LR
    D["ex:DatasetSensores"] -->|a| C1["dcat:Dataset"]
    D -->|dct:title| T["'Lecturas de Sensores 2026'@es"]
    D -->|dct:description| DE["'Registro de temperatura y humedad.'@es"]
    D -->|dct:issued| I["'2026-09-29'^^xsd:date"]
    D -->|dct:publisher| P["ex:InstitutoMeteorologico"]
    P -->|a| C2["foaf:Organization"]
    P -->|foaf:name| N["'Instituto Meteorológico de Castilla-La Mancha'"]
    P -->|foaf:homepage| H["http://www.ejemplo-meteo.es"]
```

---

## 6 · Consultas con SPARQL

Para interactuar con repositorios RDF (*triplestores*) se usa **SPARQL**, el lenguaje de consulta estándar del W3C. Funciona por **coincidencia de patrones de grafo**: describes la forma de lo que buscas y el motor encuentra todo lo que encaja.

**Objetivo:** obtener el título de cada dataset y el nombre de la organización que lo publica.

```sparql
PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX dct:  <http://purl.org/dc/terms/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?titulo ?nombrePublicador
WHERE {
  ?dataset a dcat:Dataset ;
           dct:title     ?titulo ;
           dct:publisher ?publicador .

  ?publicador foaf:name ?nombrePublicador .
}
```

**Resultado esperado:**

| titulo | nombrePublicador |
|:-------|:-----------------|
| "Lecturas de Sensores 2026"@es | "Instituto Meteorológico de Castilla-La Mancha" |

> 💡 Las variables empiezan por `?`. Fíjate en que `?publicador` actúa como **puente**: es el objeto de una terna y el sujeto de la siguiente.

*(SPARQL se estudia en profundidad en [`04-SPARQL`](../04-SPARQL/).)*

---

## 7 · Pruébalo tú mismo

### Opción A · Python con `rdflib`

```bash
pip install rdflib
```

Guarda el Turtle del apartado 5 como `sensores.ttl` y ejecuta:

```python
from rdflib import Graph

g = Graph()
g.parse("sensores.ttl", format="turtle")

print(f"El grafo contiene {len(g)} ternas\n")

consulta = """
PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX dct:  <http://purl.org/dc/terms/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?titulo ?nombrePublicador
WHERE {
  ?dataset a dcat:Dataset ;
           dct:title     ?titulo ;
           dct:publisher ?publicador .
  ?publicador foaf:name ?nombrePublicador .
}
"""

for fila in g.query(consulta):
    print(fila.titulo, "→", fila.nombrePublicador)

# Convertir a otro formato
print(g.serialize(format="nt"))
```

### Opción B · Sin instalar nada

- 🌐 **Apache Jena Fuseki** o cualquier *triplestore* local para cargar el fichero y lanzar consultas.
- 🌐 Endpoints públicos SPARQL como el de **Wikidata** para practicar consultas sobre datos reales.
- 🌐 Validadores online de Turtle para comprobar la sintaxis.

---

## 8 · Ejercicios

<details>
<summary><b>Ejercicio 1</b> · Añade una propiedad</summary>

Añade al dataset la propiedad `dct:license` apuntando a una URI de licencia. ¿Cambia el resultado de la consulta del apartado 6?

<sub>*Pista:* la consulta solo pide título y publicador, así que no cambia.</sub>
</details>

<details>
<summary><b>Ejercicio 2</b> · Segundo dataset</summary>

Crea `ex:DatasetPluviometros` publicado por la **misma** organización. Ejecuta de nuevo la consulta: ¿cuántas filas devuelve?

<sub>*Pista:* dos, con el mismo `nombrePublicador`.</sub>
</details>

<details>
<summary><b>Ejercicio 3</b> · Nodo en blanco</summary>

Describe la ubicación de un sensor usando un nodo en blanco con ciudad y país (ver apartado 3).
</details>

<details>
<summary><b>Ejercicio 4</b> · Cambia de formato</summary>

Convierte `sensores.ttl` a JSON-LD y a N-Triples con `rdflib`. Compara los tres ficheros: ¿qué ganas y qué pierdes en legibilidad?
</details>

<details>
<summary><b>Ejercicio 5</b> · Consulta nueva</summary>

Escribe una consulta SPARQL que devuelva la **fecha de publicación** (`dct:issued`) de cada dataset junto con la **web** (`foaf:homepage`) de su publicador.
</details>

---

## 9 · Errores frecuentes

| ❌ Error | ✅ Solución |
|:--------|:-----------|
| Olvidar el `.` al final de una terna | Cada sentencia Turtle termina en `.` |
| Usar `;` al final del último predicado | El último predicado de un sujeto cierra con `.` |
| Escribir la URI sin `<>` cuando no hay prefijo | Las URIs completas van entre `<...>` |
| Usar un literal como sujeto o predicado | Los literales solo pueden ser **objeto** |
| Olvidar declarar un `@prefix` | Toda abreviatura `xx:` necesita su prefijo |
| Confundir `"texto"` con `<uri>` | Comillas = literal · Ángulos = recurso |

---

## 10 · Casos de uso

- 🏛️ **Espacios de Datos (*Data Spaces*):** intercambio de metadatos estandarizados entre organizaciones respetando la soberanía de los datos.
- 🧠 **Grafos de conocimiento (*Knowledge Graphs*):** integración de bases de datos heterogéneas para inferir nueva información (p. ej. Wikidata).
- 🔗 **Linked Data:** enlazar conjuntos de datos abiertos a través de la web para enriquecer aplicaciones.

---

## 11 · Recursos y siguiente paso

**Referencias oficiales**

- [RDF 1.1 Primer (W3C)](https://www.w3.org/TR/rdf11-primer/)
- [RDF 1.1 Concepts (W3C)](https://www.w3.org/TR/rdf11-concepts/)
- [Turtle (W3C)](https://www.w3.org/TR/turtle/)
- [SPARQL 1.1 Query (W3C)](https://www.w3.org/TR/sparql11-query/)
- [Documentación de rdflib](https://rdflib.readthedocs.io/)

**Siguiente paso**

RDF te permite *afirmar* cosas, pero no dice qué tipos de cosas existen ni cómo se relacionan. Eso lo aporta el siguiente nivel:

➡️ [`02-RDFS` — RDF Schema](../02-RDFS/)

---

<div align="center">

[⬅️ Volver al README principal](../README.md)

</div>
