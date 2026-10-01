# 🔎 SPARQL — Nivel Básico

> Primer contacto práctico con SPARQL: aprender a consultar un grafo RDF mediante patrones de triples y obtener información de forma estructurada.

---

## 🎯 Objetivo

En este nivel aprenderás a utilizar **SPARQL desde cero** para realizar consultas sencillas sobre datos RDF.

La idea no es memorizar sintaxis, sino entender cómo piensa SPARQL:

> **"Quiero encontrar recursos que cumplan estos patrones dentro del grafo RDF."**

Al finalizar este nivel deberías ser capaz de:

* Entender la estructura básica de una consulta SPARQL.
* Declarar prefijos con `PREFIX`.
* Seleccionar variables con `SELECT`.
* Buscar patrones de triples mediante `WHERE`.
* Trabajar con recursos, propiedades y literales.
* Filtrar resultados.
* Ordenar resultados.
* Limitar el número de resultados.
* Eliminar resultados duplicados.

---

# 📚 Contenidos

## 1. `SELECT` — Obtener información

La instrucción `SELECT` permite indicar qué variables queremos recuperar de una consulta.

Conceptos:

* Variables: `?persona`, `?nombre`, `?edad`
* `SELECT`
* `WHERE`
* Patrones de triples
* `PREFIX`
* IRIs
* Literales

### 🧠 Concepto clave

Una consulta SPARQL básica puede entenderse como:

```text
¿Qué variables quiero obtener?
        ↓
¿Dónde las busco?
        ↓
¿Qué patrón deben cumplir?
```

Ejemplo conceptual:

```sparql
PREFIX ex: <http://example.org/>

SELECT ?nombre
WHERE {
    ?persona ex:nombre ?nombre .
}
```

---

## 2. `FILTER` — Filtrar resultados

Una vez sabemos obtener información, podemos establecer condiciones sobre los resultados.

Conceptos:

* `FILTER`
* Comparaciones
* Operadores lógicos
* Comparaciones numéricas
* Comparaciones de texto
* Funciones básicas

Ejemplo conceptual:

```sparql
SELECT ?persona ?edad
WHERE {
    ?persona ex:edad ?edad .
    FILTER(?edad >= 18)
}
```

### 🧠 Concepto clave

`FILTER` **no busca nuevos datos**.

Primero se obtiene un conjunto de resultados y después se eliminan aquellos que no cumplen la condición.

---

## 3. `ORDER BY` y `LIMIT` — Controlar resultados

Las consultas pueden devolver muchos resultados. SPARQL permite controlar cómo se muestran.

Conceptos:

* `ORDER BY`
* `ASC`
* `DESC`
* `LIMIT`
* `OFFSET`

Ejemplo conceptual:

```sparql
SELECT ?persona ?edad
WHERE {
    ?persona ex:edad ?edad .
}
ORDER BY DESC(?edad)
LIMIT 5
```

Esto permite obtener, por ejemplo, los cinco recursos con mayor edad.

---

## 4. `DISTINCT` — Eliminar duplicados

SPARQL puede producir varias soluciones equivalentes durante una consulta.

`DISTINCT` permite obtener únicamente resultados diferentes.

```sparql
SELECT DISTINCT ?ciudad
WHERE {
    ?persona ex:viveEn ?ciudad .
}
```

### 🧠 Concepto clave

```text
SELECT
    → puede devolver duplicados

SELECT DISTINCT
    → elimina resultados repetidos
```

---

# 🧩 Conceptos que debes dominar

Al terminar este nivel deberías reconocer perfectamente:

| Concepto       | Función                            |
| -------------- | ---------------------------------- |
| `PREFIX`       | Definir prefijos                   |
| `SELECT`       | Elegir qué devolver                |
| `WHERE`        | Definir el patrón de búsqueda      |
| `?variable`    | Representar valores desconocidos   |
| Triple pattern | Patrón que deben cumplir los datos |
| `FILTER`       | Aplicar condiciones                |
| `ORDER BY`     | Ordenar resultados                 |
| `LIMIT`        | Limitar resultados                 |
| `OFFSET`       | Saltar resultados                  |
| `DISTINCT`     | Eliminar duplicados                |

---

# 🧠 Orden recomendado

```text
SELECT
  ↓
PREFIX + WHERE
  ↓
Variables
  ↓
Patrones de triples
  ↓
FILTER
  ↓
ORDER BY
  ↓
LIMIT / OFFSET
  ↓
DISTINCT
```

---

# ✅ Al terminar

Deberías ser capaz de escribir consultas como:

```text
"Obtén todas las personas."

"Obtén sus nombres."

"Obtén las personas mayores de 18 años."

"Ordénalas por edad."

"Devuelve solamente las 10 primeras."

"Devuelve las ciudades sin repetir."
```

Este nivel constituye la base necesaria para comprender las consultas más complejas de los siguientes niveles.
