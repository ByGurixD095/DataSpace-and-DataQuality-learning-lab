# 🔎 SPARQL — Nivel Intermedio

> Pasamos de realizar consultas sencillas a combinar diferentes patrones y trabajar con resultados más complejos.

---

## 🎯 Objetivo

En el nivel básico aprendimos a consultar información mediante patrones sencillos.

Ahora aprenderemos a **combinar patrones**, trabajar con información opcional, crear alternativas y realizar operaciones sobre grupos de resultados.

Al finalizar este nivel deberías ser capaz de:

* Combinar varios patrones de triples.
* Comprender cómo se relacionan diferentes patrones.
* Trabajar con información opcional.
* Expresar alternativas.
* Proporcionar valores concretos a una consulta.
* Crear nuevos valores a partir de resultados.
* Utilizar funciones de agregación.
* Agrupar resultados.
* Filtrar grupos de resultados.

SPARQL 1.1 incorpora precisamente mecanismos como agregaciones, asignaciones y consultas más complejas para ampliar las consultas básicas.

---

# 📚 Contenidos

## 1. Múltiples patrones

Una consulta puede contener varios patrones de triples.

```sparql
SELECT ?persona ?nombre ?ciudad
WHERE {
    ?persona ex:nombre ?nombre .
    ?persona ex:viveEn ?ciudad .
}
```

Aquí ambos patrones deben poder cumplirse para obtener una solución.

### Conceptos

* Múltiples triple patterns.
* Variables compartidas.
* Relación entre patrones.
* Basic Graph Patterns.

---

## 2. `OPTIONAL` — Información opcional

No toda la información de un recurso tiene por qué existir.

`OPTIONAL` permite mantener un resultado aunque una determinada parte del patrón no encuentre información.

```sparql
SELECT ?persona ?nombre ?telefono
WHERE {
    ?persona ex:nombre ?nombre .

    OPTIONAL {
        ?persona ex:telefono ?telefono .
    }
}
```

### 🧠 Concepto clave

Sin `OPTIONAL`:

```text
Debe existir toda la información.
```

Con `OPTIONAL`:

```text
Esta información puede existir o no.
```

---

## 3. `UNION` — Alternativas

`UNION` permite combinar diferentes patrones alternativos.

```sparql
SELECT ?recurso
WHERE {
    {
        ?recurso ex:nombre ?valor .
    }
    UNION
    {
        ?recurso ex:titulo ?valor .
    }
}
```

Conceptualmente:

```text
Patrón A
   O
Patrón B
```

SPARQL define `UNION` como una forma de combinar patrones gráficos alternativos.

---

## 4. `VALUES` — Proporcionar valores

`VALUES` permite restringir una consulta proporcionando explícitamente determinados valores.

```sparql
SELECT ?persona ?nombre
WHERE {
    VALUES ?persona {
        ex:ana
        ex:luis
    }

    ?persona ex:nombre ?nombre .
}
```

Es especialmente útil cuando ya conocemos un conjunto de recursos sobre los que queremos consultar.

---

## 5. `BIND` — Crear valores

`BIND` permite asociar el resultado de una expresión a una nueva variable.

Conceptualmente:

```sparql
BIND(expresion AS ?variable)
```

Por ejemplo:

```sparql
SELECT ?nombre ?edad ?mayorDeEdad
WHERE {
    ?persona ex:nombre ?nombre .
    ?persona ex:edad ?edad .

    BIND(?edad >= 18 AS ?mayorDeEdad)
}
```

### 🧠 Concepto clave

`BIND` permite pasar de:

```text
datos existentes
      ↓
expresión
      ↓
nuevo valor calculado
```

---

## 6. Agregaciones

Las funciones de agregación permiten realizar operaciones sobre conjuntos de resultados.

Principales funciones:

* `COUNT`
* `SUM`
* `AVG`
* `MIN`
* `MAX`

Ejemplo:

```sparql
SELECT (COUNT(?persona) AS ?total)
WHERE {
    ?persona a ex:Persona .
}
```

Estas operaciones permiten responder preguntas como:

```text
¿Cuántas personas existen?

¿Cuál es la edad media?

¿Cuál es la edad máxima?

¿Cuál es la edad mínima?
```

---

## 7. `GROUP BY` — Agrupar resultados

`GROUP BY` permite dividir los resultados en grupos.

```sparql
SELECT ?ciudad (COUNT(?persona) AS ?total)
WHERE {
    ?persona ex:viveEn ?ciudad .
}
GROUP BY ?ciudad
```

Resultado conceptual:

```text
Madrid     → 25
Toledo     → 12
Ciudad Real → 8
```

---

## 8. `HAVING` — Filtrar grupos

`HAVING` permite aplicar condiciones después de realizar una agrupación.

```sparql
SELECT ?ciudad (COUNT(?persona) AS ?total)
WHERE {
    ?persona ex:viveEn ?ciudad .
}
GROUP BY ?ciudad
HAVING(COUNT(?persona) > 10)
```

### 🧠 Diferencia importante

```text
FILTER
   ↓
filtra soluciones individuales

HAVING
   ↓
filtra grupos
```

---

# 🧩 Conceptos que debes dominar

| Concepto           | Función                                 |
| ------------------ | --------------------------------------- |
| Múltiples patrones | Combinar información                    |
| `OPTIONAL`         | Buscar información que puede no existir |
| `UNION`            | Expresar alternativas                   |
| `VALUES`           | Proporcionar valores                    |
| `BIND`             | Crear nuevos valores                    |
| `COUNT`            | Contar                                  |
| `SUM`              | Sumar                                   |
| `AVG`              | Calcular medias                         |
| `MIN`              | Obtener mínimo                          |
| `MAX`              | Obtener máximo                          |
| `GROUP BY`         | Agrupar resultados                      |
| `HAVING`           | Filtrar grupos                          |

---

# 🧠 Orden recomendado

```text
Múltiples patrones
       ↓
OPTIONAL
       ↓
UNION
       ↓
VALUES
       ↓
BIND
       ↓
Agregaciones
       ↓
GROUP BY
       ↓
HAVING
```

---

# ✅ Al terminar

Deberías poder formular consultas como:

```text
"Obtén las personas y sus ciudades."

"Obtén las personas aunque algunas no tengan teléfono."

"Busca recursos que tengan nombre O título."

"Consulta únicamente estos recursos concretos."

"Calcula un valor a partir de los datos."

"Cuenta cuántos recursos existen."

"Cuenta recursos agrupándolos por ciudad."

"Devuelve únicamente las ciudades que tengan más de 10 recursos."
```

A partir de aquí ya estaremos preparados para consultas SPARQL considerablemente más complejas.
