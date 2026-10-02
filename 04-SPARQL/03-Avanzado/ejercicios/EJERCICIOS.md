# 🏋️ Ejercicios — SPARQL Avanzado

Datos: [`../datos/red.trig`](../datos/red.trig) · Soluciones: [`soluciones/`](soluciones/)

```bash
python ejecutar.py mi_consulta.rq
```

> 💡 Grafo `ex:personas`: `ex:conoce` (con dirección), `ex:colaboraCon`, `ex:viveEn`, `ex:enPais`.
> Grafo `ex:perfiles`: `ex:email`.

| # | Enunciado | Resultado esperado |
|---|-----------|--------------------|
| 1 | ¿A quién conoce **Diego**, directa o indirectamente? (nombres) | 6 filas |
| 2 | ¿Quién conoce **directamente** a Marta? (usa `^`) | Luis, Pablo |
| 3 | Nombre, email y nombre de ciudad de quien tenga perfil en `ex:perfiles`. | 4 filas |
| 4 | ¿Conoce Inés, indirectamente, a Elena? (`ASK`) | `true` |
| 5 | `CONSTRUCT` que invierta `ex:conoce` en `ex:conocidoPor`. | 8 triples |
| 6 | Inserta a Laura Gil (vive en Madrid) y haz que Diego la conozca. | +4 triples |

## 🧠 Para pensar

1. ¿Qué diferencia hay entre `ex:conoce+` y `ex:conoce*`?
2. ¿Por qué `ASK { ex:elena ex:conoce+ ex:ana }` da `false`?
3. ¿Qué pasa con `ejecutar.py` si lanzas dos veces el ejercicio 6? ¿Y en un triplestore real?

<details>
<summary>Respuestas</summary>

1. `*` incluye además el caso de cero pasos (el recurso con él mismo).
2. Las relaciones tienen dirección y nadie lleva de Elena a Ana.
3. `ejecutar.py` parte siempre de una copia limpia, así que ve lo mismo. En un triplestore real los datos persisten (aunque insertar dos veces el mismo triple no lo duplica).

</details>
