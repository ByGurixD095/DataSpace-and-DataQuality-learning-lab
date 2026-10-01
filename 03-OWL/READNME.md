# 🦉 03 · OWL — Web Ontology Language

> Guía de referencia rápida y repaso: lógica descriptiva, restricciones y razonamiento sobre el grafo.

![Nivel](https://img.shields.io/badge/nivel-intermedio-blue?style=flat-square)
![Estándar](https://img.shields.io/badge/est%C3%A1ndar-W3C-005a9c?style=flat-square)
![Sintaxis](https://img.shields.io/badge/sintaxis-Turtle%20%2F%20OWL%202-orange?style=flat-square)
![Lectura](https://img.shields.io/badge/lectura-~10%20min-lightgrey?style=flat-square)

---

## 📑 Contenido

- [🦉 03 · OWL — Web Ontology Language](#-03--owl--web-ontology-language)
  - [📑 Contenido](#-contenido)
  - [1 · ¿Por qué OWL si ya tenemos RDFS?](#1--por-qué-owl-si-ya-tenemos-rdfs)
  - [2 · Los 3 pilares de OWL](#2--los-3-pilares-de-owl)
  - [3 · Tipos de propiedades (Object vs Datatype)](#3--tipos-de-propiedades-object-vs-datatype)
  - [4 · Características de las propiedades](#4--características-de-las-propiedades)
  - [5 · Restricciones y constructores lógicos](#5--restricciones-y-constructores-lógicos)
    - [Restricciones de cuantificación](#restricciones-de-cuantificación)
    - [Restricciones de cardinalidad](#restricciones-de-cardinalidad)
    - [Álgebra de conjuntos](#álgebra-de-conjuntos)
  - [6 · Ejemplo práctico en Turtle](#6--ejemplo-práctico-en-turtle)
    - [🧠 ¿Qué infiere el razonador a partir del ejemplo?](#-qué-infiere-el-razonador-a-partir-del-ejemplo)
  - [7 · Inferencia y razonadores (Reasoning)](#7--inferencia-y-razonadores-reasoning)
  - [8 · Chuleta de repaso rápido (Cheat Sheet)](#8--chuleta-de-repaso-rápido-cheat-sheet)
  - [9 · Recursos y siguiente paso](#9--recursos-y-siguiente-paso)

---

## 1 · ¿Por qué OWL si ya tenemos RDFS?

**RDFS** añade jerarquías (`rdfs:subClassOf`, `rdfs:subPropertyOf`) y dominios/rangos (`rdfs:domain`, `rdfs:range`), pero su expresividad lógica es limitada.

| Necesidad | ¿Se puede en RDFS? | ¿Se puede en OWL? |
|:----------|:------------------:|:-----------------:|
| Jerarquía de clases básica |  Sí |  Sí |
| Decir que dos clases son disjuntas (no solapan) | ❌ No |  `owl:disjointWith` |
| Expresar equivalencia (`A` es lo mismo que `B`) | ❌ No |  `owl:equivalentClass` / `owl:sameAs` |
| Propiedades inversas, simétricas o transitivas | ❌ No |  `owl:inverseOf`, `owl:TransitiveProperty` |
| Restricciones de cardinalidad (mínimo, máximo, exacto) | ❌ No |  `owl:cardinality`, `owl:minCardinality` |
| Inferencia automática mediante lógica formal | ⚠️ Débil |  Lógica Descriptiva (DL) |

> 📌 **Idea clave:** En OWL, una ontología no es solo un vocabulario; es una **base de conocimiento formal** sujeta a reglas lógicas donde un razonador deduce hechos no explícitos.

---

## 2 · Los 3 pilares de OWL

1. **Clases (`owl:Class`):** Conjuntos de recursos.
2. **Propiedades:** Enlaces de datos o relaciones entre entidades.
3. **Individuos (`owl:NamedIndividual`):** Instancias concretas del mundo real.

---

## 3 · Tipos de propiedades (Object vs Datatype)

En OWL distinguimos estrictamente a dónde apunta la relación:

```text
Entidad ──── owl:ObjectProperty ────▶ Entidad
Entidad ──── owl:DatatypeProperty ──▶ Literal ("texto", 42, fecha)
```

- **`owl:ObjectProperty`**: Conecta un recurso con **otro recurso** (ej. `ex:esHijoDe`, `ex:perteneceA`).
- **`owl:DatatypeProperty`**: Conecta un recurso con un **literal tipado** (ej. `ex:tieneEdad`, `ex:codigoPostal`).

---

## 4 · Características de las propiedades

Permiten a los razonadores derivar nuevo conocimiento automáticamente:

| Característica OWL | Significado matemático | Ejemplo |
|:-------------------|:----------------------|:--------|
| `owl:TransitiveProperty` | Si $A \to B$ y $B \to C$, entonces $A \to C$ | `ex:esParteDe`, `ex:ancestroDe` |
| `owl:SymmetricProperty` | Si $A \to B$, entonces $B \to A$ | `ex:esColegaDe`, `ex:casadoCon` |
| `owl:AsymmetricProperty` | Si $A \to B$, es imposible que $B \to A$ | `ex:esPadreDe` |
| `owl:FunctionalProperty` | A cada sujeto le corresponde **a lo sumo un** objeto | `ex:tieneDNI`, `ex:madreBiologica` |
| `owl:InverseFunctionalProperty` | Dos sujetos no pueden compartir el mismo valor | `ex:tieneNumeroDePasaporte` |
| `owl:inverseOf` | Relación en sentido opuesto | `ex:esProfesorDe` $\leftrightarrow$ `ex:esAlumnoDe` |

---

## 5 · Restricciones y constructores lógicos

### Restricciones de cuantificación
- `owl:allValuesFrom` ($\forall$): Todos los valores de esta propiedad deben pertenecer a cierta clase.
- `owl:someValuesFrom` ($\exists$): Al menos un valor debe pertenecer a cierta clase.
- `owl:hasValue`: Obliga a que el valor sea un recurso o literal concreto.

### Restricciones de cardinalidad
- `owl:minCardinality`: Mínimo número de relaciones.
- `owl:maxCardinality`: Máximo número de relaciones.
- `owl:cardinality`: Número exacto.

### Álgebra de conjuntos
- `owl:unionOf` ($\cup$): Unión de clases (OR).
- `owl:intersectionOf` ($\cap$): Intersección de clases (AND).
- `owl:complementOf` ($\neg$): Negación o complemento (NOT).
- `owl:disjointWith`: Conjuntos disjuntos (un recurso no puede pertenecer a ambas clases).

---

## 6 · Ejemplo práctico en Turtle

```turtle
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix ex:   <http://example.org/universidad#> .

# 1. Definición de la ontología
<http://example.org/universidad> a owl:Ontology ;
    rdfs:label "Ontología de prueba universitaria"@es .

# 2. Clases y disyunción
ex:Persona a owl:Class .

ex:Profesor a owl:Class ;
    rdfs:subClassOf ex:Persona .

ex:Estudiante a owl:Class ;
    rdfs:subClassOf ex:Persona ;
    owl:disjointWith ex:Profesor . # No se puede ser profesor y estudiante al mismo tiempo

# 3. Propiedades con semántica rica
ex:tutorizaA a owl:ObjectProperty ;
    rdfs:domain ex:Profesor ;
    rdfs:range  ex:Estudiante ;
    owl:inverseOf ex:esTutorizadoPor .

ex:esTutorizadoPor a owl:ObjectProperty .

# 4. Asignaciones (A-Box)
ex:Ana a ex:Profesor .
ex:Carlos ex:esTutorizadoPor ex:Ana .
```

### 🧠 ¿Qué infiere el razonador a partir del ejemplo?
1. Dado que `ex:Carlos ex:esTutorizadoPor ex:Ana` y la propiedad es inversa de `tutorizaA`:  
   ➡️ **Infiere:** `ex:Ana ex:tutorizaA ex:Carlos`.
2. Dado que el rango de `tutorizaA` es `ex:Estudiante`:  
   ➡️ **Infiere:** `ex:Carlos a ex:Estudiante`.
3. Si alguien intentara declarar `ex:Carlos a ex:Profesor`:  
   ➡️ **Inconsistencia lógica (error)** detectada por `owl:disjointWith`.

---

## 7 · Inferencia y razonadores (Reasoning)

A diferencia de las bases de datos tradicionales, los sistemas basados en OWL asumen:

- **Mundo Abierto (OWA - *Open World Assumption*):** Si algo no está escrito en el grafo, **no significa que sea falso**, solo que aún no se conoce.
- **Sin Presunción de Nombres Únicos (No UNA):** Dos URIs distintas (`ex:Juan` y `ex:JuanPerez`) pueden referirse al mismo ente a menos que se indique explícitamente con `owl:differentFrom`.
- **Identidad explícita:** `owl:sameAs` unifica dos URIs en todo el grafo (clave en integración de datos y Linked Data).

---

## 8 · Chuleta de repaso rápido (Cheat Sheet)

```text
owl:Class                   -> Define una clase
owl:NamedIndividual         -> Define una instancia concreta
owl:ObjectProperty          -> Relación recurso -> recurso
owl:DatatypeProperty        -> Relación recurso -> literal
owl:subClassOf              -> Jerarquía de clases (heredado de RDFS)
owl:disjointWith            -> Exclusión mutua entre clases
owl:equivalentClass         -> Equivalencia total entre dos clases
owl:sameAs                  -> Dos URIs identifican exactamente al mismo individuo
owl:differentFrom           -> Dos URIs son expresamente individuos distintos
owl:inverseOf               -> Relación inversa bidireccional
owl:TransitiveProperty      -> Propagación en cadena (A->B->C => A->C)
owl:FunctionalProperty      -> Objeto único por sujeto
```

---

## 9 · Recursos y siguiente paso

- [W3C OWL 2 Overview (Documento oficial)](https://www.w3.org/TR/owl2-overview/)
- [Protégé (Editor gráfico de ontologías)](https://protege.stanford.edu/)
- [HermiT / Pellet (Razonadores DL)](http://www.hermit-reasoner.com/)

**Siguiente paso**

El siguiente paso natural es consultar y extraer patrones de estos grafos con ➡️ [SPARQL](../04-SPARQL/)