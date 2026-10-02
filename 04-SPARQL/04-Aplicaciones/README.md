# 🔎 SPARQL — Aplicaciones

> SPARQL no tiene por qué utilizarse únicamente escribiendo consultas manualmente: puede integrarse dentro de aplicaciones y servicios.

---

## 🎯 Objetivo

Hasta ahora hemos aprendido la sintaxis de SPARQL de forma independiente.

En esta sección veremos cómo llevar ese conocimiento a aplicaciones reales.

El objetivo es comprender la relación entre:

```text
Aplicación
    ↓
Librería / cliente RDF
    ↓
SPARQL
    ↓
Dataset / Graph Store
```

Al finalizar deberías entender cómo una aplicación puede:

* Cargar datos RDF.
* Crear o acceder a un grafo.
* Ejecutar consultas SPARQL.
* Procesar los resultados.
* Modificar datos RDF.
* Comunicarse con un endpoint SPARQL.

---

# 📚 Contenidos

## 1. Python + RDFLib

### 📁 `01-Python-RDFLib/`

Python permite trabajar con RDF mediante librerías especializadas.

En este apartado se utilizará **RDFLib** para comprender cómo integrar consultas SPARQL dentro de un programa.

Conceptos:

* Crear/cargar un grafo RDF.
* Leer datos RDF.
* Ejecutar una consulta SPARQL.
* Recorrer resultados.
* Trabajar con RDF desde Python.

Arquitectura conceptual:

```text
Python
  ↓
RDFLib
  ↓
RDF Graph
  ↓
SPARQL Query
  ↓
Resultados
```

---

## 2. Java + Apache Jena

### 📁 `02-Java-Jena/`

Java dispone de herramientas para trabajar con RDF y SPARQL.

En este apartado se utilizará **Apache Jena** para comprender cómo integrar SPARQL dentro de una aplicación Java.

Conceptos:

* Crear/cargar datasets RDF.
* Ejecutar consultas SPARQL.
* Procesar resultados.
* Trabajar con modelos RDF.
* Ejecutar operaciones de actualización.

Arquitectura conceptual:

```text
Java
  ↓
Apache Jena
  ↓
Dataset RDF
  ↓
SPARQL
  ↓
Resultados
```

---

## 3. SPARQL Endpoint

### 📁 `03-SPARQL-Endpoint/`

Un **SPARQL endpoint** permite que una aplicación se comunique con un servicio capaz de procesar consultas SPARQL.

Conceptualmente:

```text
Cliente
   │
   │ SPARQL Query
   ▼
Endpoint SPARQL
   │
   ▼
RDF Dataset
   │
   │ Resultados
   ▼
Cliente
```

Aquí aprenderemos a distinguir entre:

```text
SPARQL como lenguaje
        vs
SPARQL como servicio
```

---

# 🔌 Consulta desde una aplicación

Una aplicación puede construir o almacenar una consulta:

```sparql
SELECT ?persona ?nombre
WHERE {
    ?persona ex:nombre ?nombre .
}
```

Y enviarla al sistema RDF correspondiente.

El resultado puede ser procesado posteriormente por la aplicación.

---

# 📦 Resultados SPARQL

Las consultas `SELECT` producen resultados que pueden representarse mediante diferentes formatos de intercambio.

Entre ellos se encuentran:

* JSON
* XML
* CSV
* TSV

Estos formatos permiten que una aplicación pueda consumir los resultados de una consulta de forma estructurada.

---

# 🧠 Conceptos importantes

| Concepto      | Qué representa                  |
| ------------- | ------------------------------- |
| RDFLib        | Trabajo con RDF desde Python    |
| Apache Jena   | Framework RDF para Java         |
| Dataset       | Conjunto de grafos RDF          |
| Endpoint      | Servicio que procesa consultas  |
| Query         | Consulta SPARQL                 |
| Resultados    | Datos devueltos por la consulta |
| SPARQL Update | Modificación de datos           |

---

# 🧠 Orden recomendado

```text
RDF local
   ↓
Python + RDFLib
   ↓
Java + Jena
   ↓
SPARQL Endpoint
   ↓
Aplicación cliente
```

---

# ✅ Al terminar

Deberías poder responder:

```text
¿Cómo ejecuto SPARQL desde Python?

¿Cómo ejecuto SPARQL desde Java?

¿Qué diferencia existe entre una consulta local y un endpoint?

¿Cómo recibe una aplicación los resultados?

¿Cómo puedo integrar SPARQL dentro de una aplicación?
```

Esta sección sirve como puente entre el aprendizaje de SPARQL como lenguaje y su utilización dentro de proyectos reales.
