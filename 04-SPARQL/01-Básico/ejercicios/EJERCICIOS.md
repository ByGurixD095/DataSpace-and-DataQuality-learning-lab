# 🏋️ Ejercicios — SPARQL Básico

Todos los ejercicios se resuelven sobre [`../datos/personas.ttl`](../datos/personas.ttl).

Intenta resolverlos **antes** de mirar la carpeta [`soluciones/`](soluciones/). Cuando tengas una consulta, ejecútala con:

```bash
python ejecutar.py mi_consulta.rq
```

> 💡 Recuerda el esquema del grafo:
> `ex:Persona` → `ex:nombre`, `ex:edad`, `ex:profesion`, `ex:viveEn`
> `ex:Ciudad` → `ex:nombre`

---

## 🟢 Calentamiento

| # | Enunciado | Resultado esperado |
|---|-----------|--------------------|
| 1 | Obtén todas las ciudades con su nombre. | 5 filas |
| 2 | Obtén el nombre y la profesión de cada persona. | 10 filas |
| 3 | Obtén las personas **menores de edad** (nombre y edad). | Luis (17), Lucía (16) |
| 4 | Obtén los nombres de las personas que viven en **Madrid** (usa el recurso `ex:Madrid` directamente en el patrón). | Ana, Marta, Javier |

## 🟡 Intermedio-bajo

| # | Enunciado | Resultado esperado |
|---|-----------|--------------------|
| 5 | Obtén las personas cuya profesión sea `"Estudiante"`. | Luis, Lucía, Elena |
| 6 | Obtén las **3 personas más jóvenes**. | Lucía (16), Luis (17), Javier (18) |
| 7 | Obtén los nombres de las ciudades donde vive alguien, **sin repetir** y ordenados alfabéticamente. | Barcelona, Ciudad Real, Madrid, Sevilla, Valencia |

## 🔴 Retos

| # | Enunciado | Resultado esperado |
|---|-----------|--------------------|
| 8 | Personas de entre **20 y 50 años** (ambos incluidos), con el nombre de su ciudad, ordenadas por nombre. | Ana, Carlos, Diego, Marta |
| 9 | **Paginación:** si mostramos las personas por edad descendente de 3 en 3, ¿cuál es la página 2? | Ana (34), Marta (28), Diego (23) |

---

## 🧠 Preguntas para pensar

1. ¿Qué pasa en el ejercicio 6 si quitas el `ORDER BY`?
2. ¿Qué diferencia hay entre `FILTER(?edad > 18)` y `FILTER(?edad >= 18)` con estos datos?
3. En el ejercicio 7, ¿es necesario `DISTINCT` si ordenas? ¿Por qué?
4. ¿Qué ocurriría si una persona no tuviera `ex:profesion`? ¿Aparecería en el ejercicio 2?

<details>
<summary>Respuestas</summary>

1. Obtendrías 3 personas **cualesquiera**: sin `ORDER BY`, el orden no está garantizado.
2. Con `>` se pierde Javier (18). Es un error de límite muy habitual.
3. Sí. `ORDER BY` solo ordena, no elimina filas repetidas.
4. **No aparecería**: un patrón de triple obligatorio descarta las soluciones que no lo cumplen. (`OPTIONAL` se ve en el nivel intermedio.)

</details>
