# 🔎 SPARQL — Nivel Avanzado

> En este nivel dejamos de trabajar únicamente con consultas y empezamos a utilizar SPARQL para navegar, transformar y modificar grafos RDF.

---

## 🎯 Objetivo

El nivel avanzado introduce las características que permiten utilizar SPARQL sobre escenarios más complejos.

Aquí aprenderás a:

* Navegar por grafos mediante caminos de propiedades.
* Utilizar subconsultas.
* Trabajar con grafos nombrados.
* Construir nuevos grafos RDF.
* Comprobar condiciones.
* Consultar diferentes fuentes.
* Modificar datos RDF.
* Entender consultas federadas.

SPARQL 1.1 incorpora capacidades como **property paths, subqueries, agregaciones, consultas `ASK`, `CONSTRUCT` y operaciones de actualización**.

---

# 📚 Contenidos

## 1. Property Paths

Los **property paths** permiten recorrer relaciones del grafo siguiendo determinados caminos.

Por ejemplo:

```text
Persona
   ↓ conoce
Persona
   ↓ conoce
Persona
```

En lugar de escribir manualmente cada relación, podemos expresar un camino.

Conceptos:

* Caminos simples.
* Caminos alternativos.
* Repetición.
* Secuencias.
* Navegación por relaciones.

Son especialmente útiles cuando no conocemos de antemano cuántos pasos existen entre dos recursos.

---

## 2. Subconsultas

Una consulta SPARQL puede contener otra consulta dentro de ella.

Conceptualmente:

```text
Consulta exterior
      ↓
   Subconsulta
      ↓
Resultados
```

Esto permite construir consultas complejas por etapas.

Ejemplo conceptual:

```sparql
SELECT ?persona ?total
WHERE {
    {
        SELECT ?persona (COUNT(?amigo) AS ?total)
        WHERE {
            ?persona ex:conoce ?amigo .
        }
        GROUP BY ?persona
    }
}
```

---

## 3. `GRAPH` — Trabajar con grafos nombrados

Un RDF dataset puede contener diferentes grafos.

`GRAPH` permite indicar sobre qué grafo queremos trabajar.

Conceptualmente:

```text
Dataset
├── Grafo A
├── Grafo B
└── Grafo C
```

Podemos consultar un grafo concreto mediante:

```sparql
GRAPH ex:grafoA {
    ...
}
```

Esto resulta especialmente importante cuando trabajamos con datasets RDF formados por múltiples grafos.

---

## 4. `CONSTRUCT` — Construir RDF

Mientras `SELECT` devuelve resultados, `CONSTRUCT` permite generar un **nuevo grafo RDF** a partir de una consulta.

Conceptualmente:

```text
Grafo original
      ↓
   Consulta
      ↓
Nuevo grafo RDF
```

Ejemplo:

```sparql
CONSTRUCT {
    ?persona ex:nombre ?nombre .
}
WHERE {
    ?persona ex:name ?nombre .
}
```

Esta característica convierte SPARQL en una herramienta útil no solo para consultar RDF, sino también para transformar datos RDF.

---

## 5. `DESCRIBE`

`DESCRIBE` permite solicitar una descripción de uno o varios recursos.

```sparql
DESCRIBE ex:persona1
```

El contenido exacto de la descripción depende del servicio SPARQL que procese la consulta.

### 🧠 Concepto clave

```text
SELECT
→ tú defines exactamente qué variables quieres.

DESCRIBE
→ solicitas información descriptiva sobre un recurso.
```

---

## 6. `ASK`

`ASK` permite comprobar si existe al menos una solución para un patrón.

Devuelve:

```text
true
```

o

```text
false
```

Ejemplo:

```sparql
ASK {
    ex:persona1 ex:nombre ?nombre .
}
```

Es útil para preguntas del tipo:

```text
¿Existe este recurso?

¿Existe esta relación?

¿Existe algún recurso que cumpla esta condición?
```

---

## 7. `INSERT` y `DELETE`

SPARQL 1.1 también permite modificar grafos RDF.

Entre las operaciones disponibles se encuentran:

* `INSERT`
* `DELETE`
* `INSERT DATA`
* `DELETE DATA`
* `DELETE/INSERT`

Estas operaciones forman parte de **SPARQL 1.1 Update**.

Ejemplo conceptual:

```sparql
INSERT DATA {
    ex:persona1 ex:nombre "Ana" .
}
```

Y para eliminar:

```sparql
DELETE DATA {
    ex:persona1 ex:nombre "Ana" .
}
```

### ⚠️ Importante

Hasta ahora estábamos principalmente **consultando** datos.

Con SPARQL Update comenzamos a **modificar el Graph Store**.

---

## 8. `SERVICE` — Consultas remotas

`SERVICE` permite indicar un endpoint SPARQL remoto sobre el que ejecutar una parte de una consulta.

Conceptualmente:

```text
Consulta local
     +
Consulta remota
     ↓
Resultados
```

Esto introduce el concepto de **federación de consultas**.

---

# 🧩 Conceptos que debes dominar

| Concepto       | Función                       |
| -------------- | ----------------------------- |
| Property Paths | Navegar por relaciones        |
| Subqueries     | Consultas dentro de consultas |
| `GRAPH`        | Trabajar con grafos nombrados |
| `CONSTRUCT`    | Crear grafos RDF              |
| `DESCRIBE`     | Describir recursos            |
| `ASK`          | Comprobar existencia          |
| `INSERT`       | Insertar datos                |
| `DELETE`       | Eliminar datos                |
| `SERVICE`      | Consultar servicios remotos   |

---

# 🧠 Orden recomendado

```text
Property Paths
      ↓
Subqueries
      ↓
GRAPH
      ↓
CONSTRUCT
      ↓
DESCRIBE
      ↓
ASK
      ↓
INSERT / DELETE
      ↓
SERVICE
```

---

# ✅ Al terminar

Deberías poder enfrentarte a preguntas como:

```text
"¿Cómo puedo recorrer varias relaciones?"

"¿Cómo puedo consultar el resultado de otra consulta?"

"¿Cómo consulto un grafo concreto?"

"¿Cómo genero un nuevo grafo RDF?"

"¿Existe algún recurso que cumpla esta condición?"

"¿Cómo modifico un grafo RDF?"

"¿Cómo puedo consultar otro endpoint SPARQL?"
```

Con este nivel ya tendrás una visión bastante completa de las capacidades principales de SPARQL 1.1.
