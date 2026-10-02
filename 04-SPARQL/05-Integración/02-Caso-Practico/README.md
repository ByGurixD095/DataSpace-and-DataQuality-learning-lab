# 🧪 Caso práctico — Universidad

Un pequeño sistema de conocimiento que usa **RDF + RDFS + OWL + SPARQL**.

| Capa | Archivo | Aporta |
|------|---------|--------|
| RDF | `datos.ttl` | 4 estudiantes, 3 profesores, 5 asignaturas, 2 departamentos |
| RDFS | `ontologia.ttl` | Clases, `subClassOf`, dominios y rangos |
| OWL | `ontologia.ttl` | `SymmetricProperty`, `TransitiveProperty`, `inverseOf`, `disjointWith` |
| SPARQL | `consultas/` | 8 preguntas sobre el grafo |

## ▶️ Ejecutar (desde la carpeta `Integracion/`)

```bash
pip install rdflib owlrl
python ejecutar.py 02-Caso-Practico                    # con inferencia
python ejecutar.py 02-Caso-Practico --sin-inferencia   # sin inferencia: compara
```

## 🔑 La idea clave

`datos.ttl` **no** declara ninguna `ex:Persona` ni ningún `ex:Departamento`, y solo escribe la mitad de cada relación simétrica. SPARQL, por sí solo, no lo sabe: es el **razonador** (RDFS + OWL-RL) quien añade los triples deducidos, y SPARQL los consulta como si siempre hubieran estado.

| Consulta | Pregunta | Con inferencia | Sin inferencia |
|----------|----------|:---:|:---:|
| `01-clase` | ¿Qué recursos son `Persona`? | 7 | 0 |
| `02-propiedades` | ¿Qué propiedades tiene Ana? | 7 | 5 |
| `03-relacionados` | ¿Compañeros de Luis? | 2 | 1 |
| `04-condiciones` | ¿Requisitos (indirectos) de Calidad del Dato? | 3 | 1 |
| `05-conteo` | ¿Cuántos recursos de cada tipo? | 5 tipos | 3 tipos |
| `06-relaciones` | ¿Qué estudiantes comparten asignatura? | 3 | 3 |
| `07-construct` | Subgrafo de matriculados en Web Semántica | 4 | 4 |
| `08-ask` | ¿Alguien cursa algo impartido por Matemáticas? | true | true |

Las consultas `06`–`08` dan lo mismo en ambos modos: no dependen de conocimiento deducido.

## ⚠️ Matices

* `owl:disjointWith` está declarado, pero **OWL-RL no avisa** de inconsistencias en este montaje: es documentación del modelo. Para detectarlas hace falta un razonador completo (p. ej. HermiT desde Protégé).
* `ex:requiere+` (property path) da el mismo resultado que la transitividad **sin razonador**: dos caminos para la misma pregunta.

## 🎮 Retos

1. Declara a `ex:marta` también como `ex:Estudiante` y piensa qué debería ocurrir con `disjointWith`.
2. Añade una asignatura que requiera `ex:CAL` y comprueba la transitividad en `04`.
3. `datos.ttl` dice `ex:marta ex:tutorDe ex:ana`. Averigua con SPARQL quién es el tutor de Ana usando solo `ex:tutelado` (pista: inverso).
