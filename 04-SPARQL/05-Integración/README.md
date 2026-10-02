# 🔗 Integración — RDF + RDFS + OWL + SPARQL

> El objetivo final del aprendizaje no es utilizar RDF, RDFS, OWL y SPARQL de forma aislada, sino comprender cómo se complementan.

---

## 🎯 Objetivo

En los bloques anteriores cada tecnología se ha estudiado de forma independiente.

Ahora vamos a unirlas:

```text
RDF
 ↓
RDFS
 ↓
OWL
 ↓
SPARQL
```

Cada tecnología cumple una función diferente.

---

# 🧩 1. RDF — Representar datos

RDF proporciona la estructura básica para representar información mediante triples:

```text
Sujeto → Predicado → Objeto
```

Por ejemplo:

```text
persona1 → nombre → "Ana"
persona1 → trabajaEn → empresa1
```

RDF responde principalmente a:

> **¿Cómo representamos los datos?**

---

# 🧩 2. RDFS — Definir vocabulario

RDFS permite describir recursos, clases y propiedades.

Por ejemplo:

```text
Persona
Empresa
trabajaEn
```

Podemos establecer relaciones como:

```text
Persona → es una clase

trabajaEn → es una propiedad

trabajaEn → relaciona Persona con Empresa
```

RDFS responde principalmente a:

> **¿Cómo describimos la estructura básica de nuestros datos?**

---

# 🧩 3. OWL — Definir conocimiento y restricciones

OWL permite expresar relaciones y restricciones más complejas.

Por ejemplo:

```text
Persona
   ↓
tiene como padre
   ↓
Persona
```

También permite expresar características de propiedades, restricciones y relaciones lógicas.

OWL responde principalmente a:

> **¿Qué conocimiento y restricciones podemos expresar sobre nuestros datos?**

---

# 🧩 4. SPARQL — Consultar los datos

Una vez tenemos nuestros datos y su modelo, SPARQL permite consultarlos.

Por ejemplo:

```text
RDF
 ↓
RDFS / OWL
 ↓
SPARQL
 ↓
Resultados
```

SPARQL responde principalmente a:

> **¿Cómo obtenemos información del grafo?**

---

# 🔄 Cómo trabajan conjuntamente

Podemos visualizar todo el sistema como:

```text
                  ┌──────────────┐
                  │     OWL      │
                  │ Conocimiento │
                  │ restricciones│
                  └──────┬───────┘
                         │
                  ┌──────▼───────┐
                  │     RDFS     │
                  │  Vocabulario │
                  │   y clases   │
                  └──────┬───────┘
                         │
                  ┌──────▼───────┐
                  │     RDF      │
                  │    Datos     │
                  └──────┬───────┘
                         │
                  ┌──────▼───────┐
                  │   SPARQL     │
                  │   Consultas  │
                  └──────────────┘
```

La idea importante es que **no son tecnologías que compitan entre sí**.

Cada una trabaja en una capa diferente del problema.

---

# 📁 1. RDF + RDFS + OWL + SPARQL

### `01-RDF-RDFS-OWL-SPARQL/`

En este ejercicio se combinarán las cuatro tecnologías.

La carpeta contendrá:

```text
01-RDF-RDFS-OWL-SPARQL/
├── ontologia.ttl
├── datos.ttl
└── consultas.rq
```

### `ontologia.ttl`

Contendrá las definiciones realizadas mediante:

* RDFS
* OWL

### `datos.ttl`

Contendrá las instancias y datos RDF.

### `consultas.rq`

Contendrá las consultas SPARQL utilizadas para recuperar información.

---

# 🧪 2. Caso práctico

### `02-Caso-Practico/`

Este será el ejercicio final del aprendizaje.

La intención es construir un pequeño escenario completo donde sea necesario utilizar todo lo aprendido.

Estructura:

```text
02-Caso-Practico/
├── README.md
├── datos.ttl
├── ontologia.ttl
└── consultas/
```

---

## 🏗️ Flujo del caso práctico

El desarrollo seguirá este orden:

### Paso 1 — Modelar

Definir qué información queremos representar.

```text
¿Qué entidades existen?
¿Qué propiedades tienen?
¿Qué relaciones existen?
```

↓

### Paso 2 — RDF

Representar los datos mediante triples.

↓

### Paso 3 — RDFS

Definir:

* Clases.
* Propiedades.
* Jerarquías.
* Relaciones básicas.

↓

### Paso 4 — OWL

Añadir:

* Restricciones.
* Características de propiedades.
* Relaciones más complejas.
* Conocimiento adicional.

↓

### Paso 5 — SPARQL

Crear consultas para obtener información del sistema.

↓

### Paso 6 — Integración

Utilizar todo el modelo como un pequeño sistema de conocimiento.

---

# 🔎 Ejemplos de preguntas

El caso práctico debería permitir responder preguntas como:

```text
¿Qué recursos pertenecen a una determinada clase?

¿Qué propiedades tiene un recurso?

¿Qué recursos están relacionados con otro recurso?

¿Qué recursos cumplen determinadas condiciones?

¿Cuántos recursos existen de cada tipo?

¿Qué relaciones existen entre determinadas entidades?

¿Podemos construir un subconjunto del grafo?

¿Podemos comprobar si existe determinada información?
```

---

# 🧠 Qué debes aprender realmente

El objetivo de esta sección no es aprender nuevas palabras clave.

El objetivo es comprender **cómo encajan las piezas**:

```text
RDF
↓
Representa información

RDFS
↓
Define vocabulario y estructura

OWL
↓
Expresa conocimiento y restricciones

SPARQL
↓
Consulta y transforma los datos
```

---

# 🗺️ Recorrido completo

El aprendizaje completo del repositorio queda:

```text
01 · RDF
     ↓
02 · RDFS
     ↓
03 · OWL
     ↓
04 · SPARQL
     ↓
05 · Integración
```

Y dentro de SPARQL:

```text
Básico
   ↓
Intermedio
   ↓
Avanzado
   ↓
Aplicaciones
   ↓
Integración
```

---

# ✅ Resultado final

Al terminar esta sección deberías poder enfrentarte a un pequeño proyecto basado en tecnologías semánticas donde seas capaz de:

* Modelar información con RDF.
* Definir vocabularios con RDFS.
* Expresar conocimiento mediante OWL.
* Consultar los datos con SPARQL.
* Integrar estas tecnologías dentro de una aplicación.
* Entender cómo se relacionan entre sí.

> **La meta no es saber utilizar cuatro tecnologías por separado, sino entender el ecosistema completo.**
