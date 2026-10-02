# 🏋️ Ejercicios — SPARQL Intermedio

Todos los ejercicios se resuelven sobre [`../datos/personas-libros.ttl`](../datos/personas-libros.ttl).

Intenta resolverlos **antes** de mirar [`soluciones/`](soluciones/). Ejecuta tu consulta con:

```bash
python ejecutar.py mi_consulta.rq
```

> 💡 Esquema del grafo
> * `ex:Persona` → `ex:nombre`, `ex:edad`, `ex:viveEn`, y opcionalmente `ex:telefono`, `ex:email`
> * `ex:Ciudad` → `ex:nombre`
> * `ex:Libro` → `ex:titulo`, `ex:paginas`, `ex:genero`
>
> ⚠️ Las ciudades también tienen `ex:nombre`: si buscas personas, añade `a ex:Persona`.

---

## 🟢 Calentamiento

| # | Enunciado | Resultado esperado |
|---|-----------|--------------------|
| 1 | Nombre de cada persona junto al **nombre** de su ciudad. | 16 filas |
| 2 | Todas las personas con su email, **aunque no lo tengan**. | 16 filas (6 con email) |
| 3 | Nombres de las personas que **no** tienen email. | 10 filas |
| 4 | Una sola columna `?valor` con los nombres de las personas **y** los títulos de los libros (sin ciudades). | 22 filas |

## 🟡 Intermedio-bajo

| # | Enunciado | Resultado esperado |
|---|-----------|--------------------|
| 5 | Con `VALUES`: nombre y edad de Carlos, Sofía y Diego. | 45, 61, 23 |
| 6 | Nombre, edad y **año de nacimiento aproximado** (2026 − edad), ordenado por año. | 16 filas |
| 7 | ¿Cuántos libros son de género `"Novela"`? | 4 |
| 8 | **Edad máxima** por ciudad (mostrando el nombre de la ciudad). | Madrid 34 · Sevilla 52 · Valencia 61 · Barcelona 35 · Ciudad Real 45 |

## 🔴 Retos

| # | Enunciado | Resultado esperado |
|---|-----------|--------------------|
| 9 | Ciudades con **más de 3** personas. | Madrid (5) |
| 10 | Por género: nº de libros, total de páginas y media, **solo** géneros con más de un libro. | Novela · 4 · 2747 · 686.75 |
| 11 | Personas que no tienen **ni teléfono ni email**. | Álvaro, Carmen, Elena, Javier, Lucía |
| 12 | La ciudad con **más** personas (una sola fila). | Madrid · 5 |

---

## 🧠 Preguntas para pensar

1. En el ejercicio 2, ¿qué pasa si quitas el `OPTIONAL` y dejas el patrón del email suelto?
2. ¿Por qué no puedes escribir `FILTER(COUNT(?persona) > 3)` en el ejercicio 9?
3. ¿Qué error da `SELECT ?ciudad (COUNT(?persona) AS ?total)` si olvidas el `GROUP BY`?
4. ¿Se puede resolver el ejercicio 5 sin `VALUES`? ¿Qué ventaja tiene `VALUES`?
5. En el ejercicio 11, ¿por qué hace falta `!BOUND` y no basta con `FILTER(?telefono = "")`?

<details>
<summary>Respuestas</summary>

1. Solo quedan las 6 personas con email: sin `OPTIONAL`, la información pasa a ser obligatoria.
2. `FILTER` actúa sobre soluciones individuales, **antes** de agrupar, y el recuento aún no existe. Para filtrar grupos se usa `HAVING`.
3. Un error: las variables no agregadas del `SELECT` deben aparecer en `GROUP BY`.
4. Sí, con `UNION` de tres patrones o con `FILTER(?persona IN (...))`. `VALUES` es más corto y expresa mejor la intención ("estos recursos concretos").
5. Porque la variable **no tiene valor** (no es una cadena vacía): hay que preguntar si está enlazada con `BOUND`.

</details>
