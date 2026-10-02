# SHACL --- Shapes Constraint Language

> Guía práctica para aprender, consultar y repasar **SHACL** dentro de
> un entorno RDF.

------------------------------------------------------------------------

## 📚 ¿Qué es SHACL?

**SHACL (Shapes Constraint Language)** es un lenguaje del W3C utilizado
para **describir y validar la estructura de grafos RDF**.

Mientras que RDF nos permite representar información como triples:

``` text
sujeto → predicado → objeto
```

SHACL nos permite expresar reglas sobre cómo debería ser esa
información.

Por ejemplo, podemos decir:

-   una persona debe tener un nombre;
-   el nombre debe ser un literal de tipo `xsd:string`;
-   una persona puede tener entre 0 y 3 teléfonos;
-   un identificador debe ser único o seguir determinado patrón;
-   una propiedad debe apuntar a recursos de una determinada clase;
-   un nodo debe cumplir simultáneamente varias condiciones.

La idea fundamental puede resumirse así:

``` text
RDF → representa los datos
SHACL → describe las condiciones que deben cumplir esos datos
```

SHACL está especialmente relacionado con **calidad del dato**, ya que
permite comprobar automáticamente si un grafo RDF cumple unas
condiciones previamente definidas.

> **Idea clave:** SHACL no sustituye a RDF ni a OWL. Añade una capa de
> **restricciones y validación** sobre los datos RDF.

------------------------------------------------------------------------

## 🧠 ¿Por qué necesitamos SHACL?

RDF es muy flexible. Esa flexibilidad es una de sus grandes ventajas,
pero también puede convertirse en un problema cuando necesitamos que los
datos tengan una estructura determinada.

Imaginemos estos datos:

``` turtle
ex:Alice a ex:Person ;
    ex:name "Alice" ;
    ex:age 23 .

ex:Bob a ex:Person ;
    ex:age "twenty" .
```

Desde el punto de vista de RDF, ambos grafos pueden ser sintácticamente
válidos.

Pero quizá nuestro sistema necesite que:

1.  toda `ex:Person` tenga `ex:name`;
2.  `ex:name` sea un `xsd:string`;
3.  `ex:age` sea un entero;
4.  la edad sea opcional.

RDF por sí solo no está pensado como un sistema general de validación de
este tipo.

Aquí entra SHACL.

------------------------------------------------------------------------

# 1. 🧩 Conceptos fundamentales

Antes de escribir SHACL conviene entender cuatro conceptos:

  Concepto                Significado
  ----------------------- ----------------------------------------------------------
  **Data Graph**          Grafo RDF que queremos validar
  **Shapes Graph**        Grafo RDF que contiene las reglas SHACL
  **Shape**               Conjunto de restricciones aplicadas a determinados nodos
  **Validation Report**   Resultado de ejecutar la validación

La relación es:

``` text
                 ┌─────────────────────┐
                 │    Shapes Graph     │
                 │                     │
                 │   ex:PersonShape    │
                 │   restricciones     │
                 └──────────┬──────────┘
                            │
                         valida
                            │
                            ▼
                 ┌─────────────────────┐
                 │      Data Graph     │
                 │                     │
                 │ ex:Alice a Person    │
                 │ ex:Bob   a Person    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Validation Report   │
                 │                     │
                 │ conform / violations│
                 └─────────────────────┘
```

------------------------------------------------------------------------

## 1.1 Data Graph

Es el grafo RDF que contiene los **datos reales que queremos
comprobar**.

Ejemplo:

``` turtle
@prefix ex: <http://example.com/> .

ex:Alice
    a ex:Person ;
    ex:name "Alice" ;
    ex:age 23 .

ex:Bob
    a ex:Person ;
    ex:age "twenty" .
```

Este sería nuestro **Data Graph**.

------------------------------------------------------------------------

## 1.2 Shapes Graph

Es el grafo que contiene las **shapes y restricciones** que utilizaremos
para validar el Data Graph.

Ejemplo:

``` turtle
@prefix ex: <http://example.com/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:PersonShape
    a sh:NodeShape ;
    sh:targetClass ex:Person ;

    sh:property [
        sh:path ex:name ;
        sh:minCount 1 ;
        sh:datatype xsd:string ;
    ] .
```

La shape dice, de forma simplificada:

> "Los recursos que sean `ex:Person` deben tener al menos un `ex:name` y
> ese valor debe ser un `xsd:string`."

------------------------------------------------------------------------

## 1.3 Shape

Una **shape** es una definición de las condiciones que deben cumplir
determinados nodos.

Hay dos grandes tipos que conviene conocer inicialmente:

-   **Node Shapes**
-   **Property Shapes**

### Node Shape

Una `NodeShape` aplica restricciones al nodo como conjunto.

``` turtle
ex:PersonShape
    a sh:NodeShape ;
    sh:targetClass ex:Person .
```

### Property Shape

Una `PropertyShape` aplica restricciones a los valores asociados a una
determinada propiedad.

Por ejemplo:

``` turtle
sh:path ex:name ;
sh:datatype xsd:string ;
sh:minCount 1 ;
```

Normalmente veremos Property Shapes dentro de una Node Shape.

------------------------------------------------------------------------

# 2. 🎯 Targets: ¿a qué nodos se aplica una Shape?

Una restricción no tiene utilidad si no sabemos **sobre qué nodos debe
ejecutarse**.

SHACL proporciona diferentes mecanismos para seleccionar los **focus
nodes**.

Los más habituales son:

-   `sh:targetClass`
-   `sh:targetNode`
-   `sh:targetSubjectsOf`
-   `sh:targetObjectsOf`

------------------------------------------------------------------------

## 2.1 `sh:targetClass`

Selecciona como focus nodes los recursos que pertenecen a una clase.

``` turtle
ex:PersonShape
    a sh:NodeShape ;
    sh:targetClass ex:Person .
```

Si tenemos:

``` turtle
ex:Alice a ex:Person .
ex:Bob a ex:Person .
ex:Car a ex:Vehicle .
```

La shape se aplicará a:

``` text
ex:Alice
ex:Bob
```

pero no a:

``` text
ex:Car
```

------------------------------------------------------------------------

## 2.2 `sh:targetNode`

Permite indicar directamente un nodo concreto.

``` turtle
ex:AliceShape
    a sh:NodeShape ;
    sh:targetNode ex:Alice .
```

Esta técnica resulta útil cuando queremos validar recursos concretos.

------------------------------------------------------------------------

## 2.3 `sh:targetSubjectsOf`

Selecciona los sujetos que tienen determinada propiedad.

``` turtle
ex:NameShape
    a sh:NodeShape ;
    sh:targetSubjectsOf ex:name .
```

Si tenemos:

``` turtle
ex:Alice ex:name "Alice" .
ex:Bob ex:name "Bob" .
```

los focus nodes serán:

``` text
ex:Alice
ex:Bob
```

------------------------------------------------------------------------

## 2.4 `sh:targetObjectsOf`

Selecciona los objetos de una propiedad.

``` turtle
ex:PersonReferenceShape
    a sh:NodeShape ;
    sh:targetObjectsOf ex:knows .
```

Con:

``` turtle
ex:Alice ex:knows ex:Bob .
```

`ex:Bob` puede convertirse en focus node de la shape.

------------------------------------------------------------------------

# 3. 🏗️ Nuestra primera Shape

Vamos a construir una shape paso a paso.

Supongamos que queremos validar personas.

### Datos

``` turtle
@prefix ex: <http://example.com/> .

ex:Alice
    a ex:Person ;
    ex:name "Alice" ;
    ex:age 23 .
```

### Shape

``` turtle
@prefix ex: <http://example.com/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:PersonShape
    a sh:NodeShape ;
    sh:targetClass ex:Person ;

    sh:property [
        sh:path ex:name ;
        sh:minCount 1 ;
        sh:datatype xsd:string ;
    ] .
```

Podemos leerla casi como una frase:

``` text
PersonShape
    ↓
es una Node Shape
    ↓
se aplica a ex:Person
    ↓
debe existir ex:name
    ↓
ex:name debe ser xsd:string
```

------------------------------------------------------------------------

# 4. 🔢 Cardinalidad

La cardinalidad indica **cuántos valores puede o debe tener una
propiedad**.

Las restricciones más importantes son:

-   `sh:minCount`
-   `sh:maxCount`

------------------------------------------------------------------------

## 4.1 `sh:minCount`

Indica el número mínimo de valores.

``` turtle
sh:minCount 1 ;
```

Significa:

> Debe existir al menos un valor.

Ejemplo:

``` turtle
sh:property [
    sh:path ex:name ;
    sh:minCount 1 ;
] .
```

Sin `ex:name`:

``` turtle
ex:Bob a ex:Person .
```

la validación fallaría.

------------------------------------------------------------------------

## 4.2 `sh:maxCount`

Indica el número máximo de valores.

``` turtle
sh:maxCount 1 ;
```

Significa:

> No puede haber más de un valor.

Ejemplo:

``` turtle
sh:property [
    sh:path ex:birthDate ;
    sh:maxCount 1 ;
] .
```

------------------------------------------------------------------------

## 4.3 Combinando ambas

Podemos expresar una cardinalidad exacta:

``` turtle
sh:minCount 1 ;
sh:maxCount 1 ;
```

Esto significa:

``` text
exactamente 1 valor
```

También podemos expresar:

  Restricción                   Significado
  ----------------------------- -----------------
  `minCount 0`                  opcional
  `minCount 1`                  obligatorio
  `maxCount 1`                  como máximo uno
  `minCount 1` + `maxCount 1`   exactamente uno

------------------------------------------------------------------------

# 5. 🔤 Tipos de datos

Podemos restringir el tipo RDF de los valores mediante `sh:datatype`.

Ejemplo:

``` turtle
sh:property [
    sh:path ex:age ;
    sh:datatype xsd:integer ;
] .
```

Entonces:

``` turtle
ex:Alice ex:age 23 .
```

puede cumplir la restricción.

Mientras que:

``` turtle
ex:Alice ex:age "twenty" .
```

no cumple la restricción de `xsd:integer`.

------------------------------------------------------------------------

## 5.1 Tipos habituales

``` turtle
xsd:string
xsd:integer
xsd:decimal
xsd:double
xsd:boolean
xsd:date
xsd:dateTime
```

Ejemplo:

``` turtle
sh:property [
    sh:path ex:birthDate ;
    sh:datatype xsd:date ;
] .
```

------------------------------------------------------------------------

# 6. 🧱 Restricción por clase

`sh:class` permite exigir que los valores sean instancias de una
determinada clase.

Ejemplo:

``` turtle
sh:property [
    sh:path ex:worksFor ;
    sh:class ex:Company ;
] .
```

Esto expresa:

> El valor de `ex:worksFor` debe ser un recurso perteneciente a
> `ex:Company`.

Por ejemplo:

``` turtle
ex:Alice ex:worksFor ex:Acme .
ex:Acme a ex:Company .
```

------------------------------------------------------------------------

# 7. 🔗 Restricción por tipo de nodo

`sh:nodeKind` permite restringir qué clase de término RDF puede
utilizarse.

Algunos valores habituales son:

``` turtle
sh:IRI
sh:BlankNode
sh:Literal
sh:BlankNodeOrIRI
sh:IRIOrLiteral
sh:BlankNodeOrLiteral
```

Ejemplo:

``` turtle
sh:property [
    sh:path ex:homepage ;
    sh:nodeKind sh:IRI ;
] .
```

Esto indica que `ex:homepage` debe contener una IRI.

------------------------------------------------------------------------

# 8. 📏 Restricciones de longitud y valor

SHACL también permite establecer restricciones sobre valores literales.

Algunas especialmente útiles:

``` turtle
sh:minLength
sh:maxLength
sh:pattern
sh:minInclusive
sh:maxInclusive
sh:minExclusive
sh:maxExclusive
```

------------------------------------------------------------------------

## 8.1 Longitud

``` turtle
sh:property [
    sh:path ex:name ;
    sh:minLength 2 ;
    sh:maxLength 100 ;
] .
```

------------------------------------------------------------------------

## 8.2 Expresiones regulares

``` turtle
sh:property [
    sh:path ex:email ;
    sh:pattern "^[^@]+@[^@]+\\.[^@]+$" ;
] .
```

Esto permite validar un formato mediante una expresión regular.

> Las expresiones regulares pueden ser útiles, pero conviene no
> utilizarlas para reglas excesivamente complejas si una restricción
> SHACL más específica puede expresar la intención de forma más clara.

------------------------------------------------------------------------

## 8.3 Rangos numéricos

``` turtle
sh:property [
    sh:path ex:age ;
    sh:minInclusive 0 ;
    sh:maxInclusive 120 ;
] .
```

Esto permite expresar:

``` text
0 ≤ age ≤ 120
```

------------------------------------------------------------------------

# 9. 🧾 Enumeraciones con `sh:in`

Podemos restringir un valor a una lista concreta.

``` turtle
sh:property [
    sh:path ex:status ;
    sh:in (
        "active"
        "inactive"
        "pending"
    ) ;
] .
```

Los valores permitidos son únicamente:

``` text
active
inactive
pending
```

Esto resulta útil para campos categóricos.

------------------------------------------------------------------------

# 10. 🚫 `sh:hasValue`

`sh:hasValue` exige que aparezca un valor concreto.

``` turtle
sh:property [
    sh:path ex:country ;
    sh:hasValue "Spain" ;
] .
```

La propiedad `ex:country` debe contener el valor indicado.

------------------------------------------------------------------------

# 11. 🔀 Restricciones lógicas

SHACL permite combinar condiciones.

Las principales son:

-   `sh:and`
-   `sh:or`
-   `sh:xone`
-   `sh:not`

------------------------------------------------------------------------

## 11.1 `sh:and`

Todas las condiciones deben cumplirse.

Conceptualmente:

``` text
A AND B
```

------------------------------------------------------------------------

## 11.2 `sh:or`

Debe cumplirse al menos una condición.

``` text
A OR B
```

------------------------------------------------------------------------

## 11.3 `sh:xone`

Debe cumplirse exactamente una de las condiciones.

``` text
A XOR B
```

------------------------------------------------------------------------

## 11.4 `sh:not`

La condición indicada no debe cumplirse.

``` text
NOT A
```

Estas restricciones son especialmente útiles cuando el modelo de datos
tiene reglas alternativas.

------------------------------------------------------------------------

# 12. 🧩 Reutilizar Shapes con `sh:node`

Una shape puede exigir que un nodo cumpla otra shape.

Ejemplo:

``` turtle
ex:AddressShape
    a sh:NodeShape ;

    sh:property [
        sh:path ex:street ;
        sh:minCount 1 ;
    ] ;

    sh:property [
        sh:path ex:postalCode ;
        sh:minCount 1 ;
    ] .
```

Podemos utilizarla desde otra shape:

``` turtle
ex:PersonShape
    a sh:NodeShape ;
    sh:targetClass ex:Person ;

    sh:property [
        sh:path ex:address ;
        sh:node ex:AddressShape ;
    ] .
```

Esto permite construir validaciones modulares.

Podemos imaginarlo como:

``` text
PersonShape
    │
    └── address
          │
          └── AddressShape
                 ├── street
                 └── postalCode
```

------------------------------------------------------------------------

# 13. 🔄 `sh:property` frente a `sh:node`

Esta diferencia es muy importante.

### `sh:property`

Define restricciones sobre **una propiedad y sus valores**.

``` turtle
sh:property [
    sh:path ex:name ;
    sh:datatype xsd:string ;
] .
```

### `sh:node`

Indica que el valor debe cumplir **otra Node Shape**.

``` turtle
sh:property [
    sh:path ex:address ;
    sh:node ex:AddressShape ;
] .
```

Una forma sencilla de recordarlo:

``` text
sh:property → "¿Cómo debe ser esta propiedad?"

sh:node     → "¿Qué Shape debe cumplir este nodo?"
```

------------------------------------------------------------------------

# 14. 📊 `sh:nodeShape` y `sh:propertyShape`

En el modelo de SHACL existen dos conceptos que suelen aparecer juntos:

``` text
Node Shape
    ↓
Property Shape
```

Ejemplo:

``` turtle
ex:PersonShape
    a sh:NodeShape ;
    sh:targetClass ex:Person ;

    sh:property [
        sh:path ex:name ;
        sh:minCount 1 ;
        sh:datatype xsd:string ;
    ] .
```

Aquí:

``` text
ex:PersonShape
```

es la Node Shape.

Mientras que el nodo anónimo:

``` turtle
[
    sh:path ex:name ;
    sh:minCount 1 ;
    sh:datatype xsd:string ;
]
```

representa una Property Shape.

------------------------------------------------------------------------

# 15. 🧪 Validation Report

Cuando ejecutamos una validación SHACL obtenemos un **Validation
Report**.

El resultado permite saber si el Data Graph cumple las restricciones.

Conceptualmente:

``` text
Data Graph
     +
Shapes Graph
     ↓
Validación SHACL
     ↓
Validation Report
```

El informe contiene información sobre las infracciones encontradas.

Una respuesta típica puede indicar:

``` text
Conforms: false
```

junto con detalles sobre:

-   el nodo que incumple;
-   la propiedad afectada;
-   la constraint que falló;
-   el valor problemático;
-   el mensaje asociado.

------------------------------------------------------------------------

## 15.1 `sh:ValidationReport`

El resultado se representa también como RDF.

Ejemplo simplificado:

``` turtle
[
    a sh:ValidationReport ;
    sh:conforms false ;
    sh:result [
        sh:focusNode ex:Bob ;
        sh:resultPath ex:name ;
        sh:resultSeverity sh:Violation ;
    ]
] .
```

------------------------------------------------------------------------

# 16. ⚠️ Severidades

SHACL permite clasificar los resultados mediante severidades.

Las principales son:

``` turtle
sh:Violation
sh:Warning
sh:Info
```

Ejemplo:

``` turtle
sh:property [
    sh:path ex:email ;
    sh:minCount 1 ;
    sh:severity sh:Warning ;
] .
```

Esto permite distinguir entre problemas críticos y problemas que
simplemente queremos señalar.

------------------------------------------------------------------------

# 17. 💬 Mensajes personalizados

Podemos proporcionar mensajes que hagan los resultados más
comprensibles.

``` turtle
sh:property [
    sh:path ex:name ;
    sh:minCount 1 ;
    sh:message "La persona debe tener un nombre." ;
] .
```

Así, un sistema que muestre los resultados puede proporcionar
información más útil que un mensaje técnico genérico.

------------------------------------------------------------------------

# 18. 🧭 Paths

`sh:path` indica **qué camino o propiedad se está validando**.

El caso más sencillo es una propiedad:

``` turtle
sh:path ex:name ;
```

Pero SHACL permite expresar paths más complejos.

Algunos conceptos que aparecen en paths son:

``` text
secuencia
alternativa
inversa
cero o más
una o más
cero o una
```

Por ejemplo, una secuencia conceptual:

``` text
ex:address / ex:postalCode
```

permite expresar una navegación desde una persona hasta su código postal
pasando por su dirección.

Los paths son una de las partes más potentes de SHACL, pero también una
de las que conviene estudiar después de dominar las Property Shapes
básicas.

------------------------------------------------------------------------

# 19. 🧱 Ejemplo completo

Vamos a combinar varios conceptos.

## Data Graph

``` turtle
@prefix ex: <http://example.com/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:Alice
    a ex:Person ;
    ex:name "Alice" ;
    ex:age 23 ;
    ex:email "alice@example.com" .

ex:Bob
    a ex:Person ;
    ex:age "twenty" ;
    ex:email "not-an-email" .
```

## Shapes Graph

``` turtle
@prefix ex: <http://example.com/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:PersonShape
    a sh:NodeShape ;

    sh:targetClass ex:Person ;

    sh:property [
        sh:path ex:name ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:datatype xsd:string ;
        sh:message "Toda persona debe tener exactamente un nombre." ;
    ] ;

    sh:property [
        sh:path ex:age ;
        sh:datatype xsd:integer ;
        sh:minInclusive 0 ;
        sh:maxInclusive 120 ;
        sh:message "La edad debe ser un entero entre 0 y 120." ;
    ] ;

    sh:property [
        sh:path ex:email ;
        sh:datatype xsd:string ;
        sh:pattern "^[^@]+@[^@]+\\.[^@]+$" ;
        sh:message "El email debe tener un formato válido." ;
    ] .
```

### ¿Qué ocurrirá?

`ex:Alice` puede cumplir las restricciones.

`ex:Bob` presenta varios problemas:

``` text
❌ falta ex:name
❌ ex:age no tiene el datatype esperado
❌ ex:email no cumple el patrón
```

Este es precisamente uno de los usos más interesantes de SHACL para
**calidad del dato**.

------------------------------------------------------------------------

# 20. 🆚 SHACL frente a RDF, RDFS y OWL

Es importante no confundir estas tecnologías.

  Tecnología   Pregunta principal
  ------------ ------------------------------------------------------
  RDF          ¿Cómo representamos información?
  RDFS         ¿Cómo describimos clases y relaciones básicas?
  OWL          ¿Cómo expresamos conocimiento y axiomas ontológicos?
  SHACL        ¿Cumplen los datos unas condiciones determinadas?
  SPARQL       ¿Cómo consultamos o manipulamos datos RDF?

Una forma sencilla de visualizarlo:

``` text
                RDF
                 │
        representación de datos
                 │
       ┌─────────┴─────────┐
       │                   │
      RDFS                OWL
       │                   │
 vocabulario y          conocimiento
 jerarquías             y axiomas
       │                   │
       └─────────┬─────────┘
                 │
               SHACL
                 │
            restricciones
             y validación
                 │
              SPARQL
                 │
        consulta / manipulación
```

> **Importante:** SHACL y OWL pueden utilizarse conjuntamente, pero
> cumplen funciones diferentes. Una ontología OWL no debe entenderse
> simplemente como un sustituto de un conjunto de reglas de validación
> SHACL.

------------------------------------------------------------------------

# 21. 🔍 SHACL y razonamiento: una diferencia importante

Una confusión habitual es pensar:

> "Si OWL dice que algo debería cumplirse, SHACL comprobará
> automáticamente que los datos lo cumplen."

No necesariamente.

SHACL está orientado a **validar grafos contra condiciones definidas en
shapes**.

Por otro lado, OWL se utiliza para representar conocimiento ontológico y
permitir determinadas inferencias.

Por eso:

``` text
OWL → semántica y razonamiento ontológico
SHACL → restricciones y validación
```

Pueden complementarse, pero no tienen exactamente el mismo propósito.

------------------------------------------------------------------------

# 22. 🧠 SHACL y calidad del dato

SHACL tiene una relación especialmente interesante con la **Data
Quality**.

Una organización puede definir reglas como:

``` text
Cada dataset debe tener un título.
Cada recurso debe tener un identificador.
Cada fecha debe utilizar el datatype correcto.
Cada persona debe tener un email.
Cada catálogo debe contener información mínima.
```

Estas reglas pueden convertirse en shapes.

Por ejemplo:

``` text
Regla de calidad
      ↓
SHACL Shape
      ↓
Validación automática
      ↓
Validation Report
      ↓
Indicadores / incidencias
```

Esto permite pasar de una definición abstracta de calidad a
**comprobaciones ejecutables sobre los datos**.

------------------------------------------------------------------------

# 23. 🌐 SHACL en Data Spaces

SHACL puede ser especialmente útil en escenarios de **Data Spaces**.

En un Data Space diferentes participantes pueden intercambiar datasets
que deben cumplir determinados requisitos.

Por ejemplo:

``` text
Proveedor
    │
    │ dataset RDF
    ▼
Validación SHACL
    │
    ├── ✅ cumple
    │
    └── ❌ no cumple
             │
             ▼
      Validation Report
```

Una organización podría definir un perfil de datos mediante SHACL y
utilizarlo como condición de calidad antes de aceptar determinados
datos.

Ejemplo conceptual:

``` text
Dataset de movilidad
        │
        ├── identificador obligatorio
        ├── fecha obligatoria
        ├── coordenadas válidas
        ├── tipo de vehículo permitido
        └── valores dentro de rangos
                  │
                  ▼
              SHACL
                  │
          ┌───────┴───────┐
          ▼               ▼
        válido          inválido
```

Esto no significa que SHACL resuelva por sí solo toda la **calidad del
dato**. Puede cubrir determinadas dimensiones y reglas estructurales,
pero la calidad de datos puede incluir muchas otras dimensiones y
procesos.

------------------------------------------------------------------------

# 24. 🧰 SHACL Core y SHACL-SPARQL

La especificación clásica de SHACL distingue entre:

### SHACL Core

Incluye las restricciones estándar del lenguaje.

Ejemplos:

``` text
sh:minCount
sh:maxCount
sh:datatype
sh:class
sh:nodeKind
sh:pattern
sh:minInclusive
sh:maxInclusive
sh:in
sh:hasValue
```

### SHACL-SPARQL

Permite utilizar SPARQL para expresar restricciones más avanzadas.

Conceptualmente:

``` text
SHACL Core
    ↓
restricciones estándar

SHACL-SPARQL
    ↓
restricciones expresadas mediante SPARQL
```

Para empezar a aprender SHACL conviene dominar **Core antes de entrar en
SHACL-SPARQL**.

------------------------------------------------------------------------

# 25. 🧪 Una estrategia práctica para crear Shapes

Cuando tengas que construir una shape desde cero, puedes seguir este
proceso.

### Paso 1 --- Identifica el recurso

Pregunta:

> ¿Qué tipo de recurso quiero validar?

Ejemplo:

``` text
ex:Person
```

------------------------------------------------------------------------

### Paso 2 --- Define el target

Por ejemplo:

``` turtle
sh:targetClass ex:Person ;
```

------------------------------------------------------------------------

### Paso 3 --- Lista las propiedades importantes

Por ejemplo:

``` text
name
email
age
address
```

------------------------------------------------------------------------

### Paso 4 --- Decide la cardinalidad

Para cada propiedad:

``` text
¿Es obligatoria?
¿Puede repetirse?
¿Puede aparecer una sola vez?
```

------------------------------------------------------------------------

### Paso 5 --- Define el tipo

Pregunta:

``` text
¿Es un literal?
¿Una IRI?
¿Un recurso de una clase concreta?
¿Qué datatype debe tener?
```

------------------------------------------------------------------------

### Paso 6 --- Añade restricciones de valor

Por ejemplo:

``` text
rango
longitud
patrón
valores permitidos
```

------------------------------------------------------------------------

### Paso 7 --- Añade mensajes

Los mensajes ayudan a convertir un resultado técnico en una incidencia
comprensible.

------------------------------------------------------------------------

### Paso 8 --- Valida con datos reales

No basta con escribir una shape.

Hay que probarla con:

``` text
datos válidos
datos inválidos
casos límite
datos incompletos
```

------------------------------------------------------------------------

# 26. 🧪 Casos que deberías probar

Para cada shape es recomendable crear al menos:

### Caso válido

``` text
Todos los requisitos se cumplen.
```

### Caso inválido por ausencia

``` text
Falta una propiedad obligatoria.
```

### Caso inválido por datatype

``` text
Se utiliza un tipo incorrecto.
```

### Caso inválido por cardinalidad

``` text
Hay demasiados o demasiado pocos valores.
```

### Caso inválido por valor

``` text
El valor existe, pero está fuera del rango permitido.
```

### Caso límite

``` text
El valor está exactamente en el límite permitido.
```

Esto es especialmente importante cuando SHACL forma parte de una
herramienta de **evaluación de calidad del dato**.

------------------------------------------------------------------------

# 27. 🧹 Buenas prácticas

## 27.1 Mantén las shapes legibles

Evita crear una única shape gigantesca si puedes dividirla de forma
lógica.

------------------------------------------------------------------------

## 27.2 Utiliza nombres claros

Mejor:

``` turtle
ex:PersonShape
ex:AddressShape
ex:DatasetShape
```

que:

``` turtle
ex:S1
ex:S2
ex:S3
```

------------------------------------------------------------------------

## 27.3 Utiliza mensajes útiles

Mejor:

``` text
"La persona debe tener exactamente un nombre."
```

que:

``` text
Constraint violation.
```

------------------------------------------------------------------------

## 27.4 Separa datos y shapes

Una estructura de repositorio puede ser:

``` text
SHACL/
├── README.md
├── data/
│   ├── valid.ttl
│   └── invalid.ttl
├── shapes/
│   └── person-shapes.ttl
└── reports/
    └── validation-report.ttl
```

Esto facilita entender qué se está validando y con qué reglas.

------------------------------------------------------------------------

## 27.5 Empieza por SHACL Core

No empieces directamente con SPARQL.

Primero domina:

``` text
targets
properties
cardinalidades
datatypes
node kinds
classes
valores
patrones
logical constraints
node shapes
validation reports
```

Después puedes avanzar hacia restricciones SPARQL.

------------------------------------------------------------------------

# 28. ⚠️ Errores frecuentes

### Confundir Data Graph y Shapes Graph

``` text
Data Graph   → datos que queremos validar
Shapes Graph → reglas utilizadas para validar
```

------------------------------------------------------------------------

### Olvidar el target

Una shape puede estar correctamente escrita y, aun así, no aplicarse a
los nodos que esperábamos si no hemos definido correctamente cómo se
seleccionan los focus nodes.

------------------------------------------------------------------------

### Confundir `sh:datatype` y `sh:class`

``` text
sh:datatype → tipo de literal RDF
sh:class    → clase RDF que debe cumplir un recurso
```

------------------------------------------------------------------------

### Utilizar SHACL como si fuera OWL

SHACL está orientado a validación mediante restricciones.

OWL está orientado a representación ontológica y razonamiento.

------------------------------------------------------------------------

### Crear restricciones demasiado complejas demasiado pronto

Antes de recurrir a mecanismos avanzados, comprueba si la regla puede
expresarse con SHACL Core de forma clara.

------------------------------------------------------------------------

# 29. 🗂️ Chuleta rápida

## Estructura básica

``` turtle
ex:PersonShape
    a sh:NodeShape ;
    sh:targetClass ex:Person ;

    sh:property [
        sh:path ex:name ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:datatype xsd:string ;
    ] .
```

------------------------------------------------------------------------

## Targets

``` turtle
sh:targetClass
sh:targetNode
sh:targetSubjectsOf
sh:targetObjectsOf
```

------------------------------------------------------------------------

## Cardinalidad

``` turtle
sh:minCount
sh:maxCount
```

------------------------------------------------------------------------

## Tipos

``` turtle
sh:datatype
sh:class
sh:nodeKind
```

------------------------------------------------------------------------

## Valores

``` turtle
sh:in
sh:hasValue
sh:pattern
```

------------------------------------------------------------------------

## Rangos

``` turtle
sh:minInclusive
sh:maxInclusive
sh:minExclusive
sh:maxExclusive
```

------------------------------------------------------------------------

## Longitud

``` turtle
sh:minLength
sh:maxLength
```

------------------------------------------------------------------------

## Composición

``` turtle
sh:and
sh:or
sh:xone
sh:not
```

------------------------------------------------------------------------

## Reutilización

``` turtle
sh:node
```

------------------------------------------------------------------------

## Resultados

``` turtle
sh:ValidationReport
sh:conforms
sh:result
sh:focusNode
sh:resultPath
sh:resultSeverity
sh:resultMessage
```

------------------------------------------------------------------------

# 30. 🧭 Ruta de aprendizaje recomendada

Si estás empezando desde cero:

``` text
01. RDF
    ↓
02. RDFS
    ↓
03. SPARQL
    ↓
04. SHACL
    ↓
05. SHACL Core
    ↓
06. Validation Reports
    ↓
07. SHACL-SPARQL
    ↓
08. Aplicaciones en Data Quality
    ↓
09. Aplicaciones en Data Spaces
```

### Nivel 1 --- Fundamentos

Aprende:

-   qué es SHACL;
-   Data Graph;
-   Shapes Graph;
-   Node Shape;
-   Property Shape;
-   targets.

### Nivel 2 --- Restricciones

Aprende:

-   cardinalidades;
-   datatypes;
-   clases;
-   node kinds;
-   rangos;
-   patrones;
-   enumeraciones.

### Nivel 3 --- Composición

Aprende:

-   `sh:node`;
-   `sh:and`;
-   `sh:or`;
-   `sh:xone`;
-   `sh:not`;
-   paths.

### Nivel 4 --- Validación

Aprende:

-   Validation Reports;
-   severidades;
-   mensajes;
-   interpretación de resultados.

### Nivel 5 --- Avanzado

Aprende:

-   SHACL-SPARQL;
-   custom constraint components;
-   casos de validación complejos;
-   integración con herramientas;
-   automatización.

### Nivel 6 --- Aplicación

Lleva SHACL a:

-   Data Quality;
-   Data Governance;
-   Data Spaces;
-   catálogos de datos;
-   interoperabilidad;
-   pipelines de validación.

------------------------------------------------------------------------

# 31. 🔬 Ejercicio recomendado

Crea una shape para `ex:Dataset`.

Los requisitos son:

``` text
Un dataset debe:

✓ tener un título
✓ tener exactamente un identificador
✓ tener una descripción opcional
✓ tener una fecha de creación
✓ tener un formato
✓ utilizar un formato permitido
```

Puedes comenzar con:

``` turtle
ex:DatasetShape
    a sh:NodeShape ;
    sh:targetClass ex:Dataset .
```

Y construir progresivamente las Property Shapes.

### Objetivo

No intentes escribir toda la shape de una vez.

Construye:

``` text
1. target
2. title
3. identifier
4. description
5. creation date
6. format
7. valores permitidos
```

Después crea:

``` text
valid-dataset.ttl
invalid-dataset.ttl
```

y compara los resultados.

------------------------------------------------------------------------

# 32. 🔗 Relación con el resto del Learning Lab

SHACL tiene sentido especialmente cuando se estudia junto al resto del
ecosistema RDF.

``` text
RDF
 │
 ├── Representación de datos
 │
 ├── RDFS
 │      └── vocabularios y jerarquías
 │
 ├── OWL
 │      └── ontologías y razonamiento
 │
 ├── SPARQL
 │      └── consulta y manipulación
 │
 └── SHACL
        └── restricciones y validación
```

Una posible progresión dentro de un Learning Lab sería:

``` text
RDF
 ↓
RDFS
 ↓
SPARQL
 ↓
SHACL
 ↓
Data Quality
 ↓
Data Spaces
```

------------------------------------------------------------------------

# 33. 📌 Conceptos que deberías ser capaz de explicar

Antes de considerar que dominas los fundamentos de SHACL, deberías poder
responder sin consultar documentación:

-   ¿Qué es SHACL?
-   ¿Qué diferencia hay entre Data Graph y Shapes Graph?
-   ¿Qué es una Node Shape?
-   ¿Qué es una Property Shape?
-   ¿Qué es un focus node?
-   ¿Para qué sirve `sh:targetClass`?
-   ¿Qué diferencia hay entre `sh:minCount` y `sh:maxCount`?
-   ¿Qué diferencia hay entre `sh:datatype` y `sh:class`?
-   ¿Para qué sirve `sh:nodeKind`?
-   ¿Qué hace `sh:pattern`?
-   ¿Qué hace `sh:in`?
-   ¿Qué diferencia hay entre `sh:property` y `sh:node`?
-   ¿Qué es un Validation Report?
-   ¿Qué significa `sh:conforms`?
-   ¿Qué severidades proporciona SHACL?
-   ¿Qué diferencia hay entre SHACL y OWL?
-   ¿Qué diferencia hay entre SHACL Core y SHACL-SPARQL?
-   ¿Cómo puede utilizarse SHACL para comprobar reglas de calidad del
    dato?

Si puedes responderlas y construir una shape sencilla desde cero, ya
tienes una base sólida para continuar con ejemplos más avanzados.

------------------------------------------------------------------------

# 34. 📚 Referencias oficiales

-   **W3C --- Shapes Constraint Language (SHACL), Recommendation de
    2017**\
    https://www.w3.org/TR/shacl/

-   **W3C --- SHACL 1.2 Core**\
    https://www.w3.org/TR/shacl12-core/

-   **W3C --- SHACL 1.2 SPARQL-Related Features**\
    https://www.w3.org/TR/shacl12-sparql/

-   **W3C --- SHACL 1.2 Rules**\
    https://www.w3.org/TR/shacl12-rules/

-   **W3C --- SHACL 1.2 User Interfaces**\
    https://www.w3.org/TR/shacl12-ui/

> **Nota sobre versiones:** la especificación SHACL original fue
> publicada como Recommendation por el W3C el 20 de julio de 2017. En
> 2026 existe además una familia de especificaciones **SHACL 1.2** en
> desarrollo, incluyendo SHACL 1.2 Core y extensiones relacionadas. Para
> aprender los fundamentos, esta guía se centra principalmente en
> conceptos estables de SHACL Core y señala las funcionalidades
> avanzadas como una segunda etapa de aprendizaje.

------------------------------------------------------------------------

# 🧠 Resumen final

Si tuvieras que quedarte con una sola idea:

> **SHACL permite definir cómo deberían ser los datos RDF y comprobar
> automáticamente si realmente cumplen esas condiciones.**

El modelo mental básico es:

``` text
              SHAPES GRAPH
                   │
                   │
              "debería ser"
                   │
                   ▼
                SHACL
                   │
                   │ valida
                   ▼
               DATA GRAPH
                   │
                   │
              "es realmente"
                   │
                   ▼
           VALIDATION REPORT
                   │
             ┌─────┴─────┐
             ▼           ▼
           válido      errores
```

Y la relación con un contexto de calidad del dato puede resumirse como:

``` text
Requisito de calidad
        ↓
Restricción SHACL
        ↓
Validación automática
        ↓
Resultado
        ↓
Identificación de incumplimientos
```

SHACL convierte, por tanto, muchas reglas que normalmente quedarían
escritas como documentación o requisitos en **restricciones formalizadas
que pueden ejecutarse sobre grafos RDF**.
