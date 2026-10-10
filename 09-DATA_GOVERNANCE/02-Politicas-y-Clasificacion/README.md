# 🔐 02 · Políticas y clasificación

> **Idea:** clasifica una vez, aplica una política **por nivel** y deja que el nivel decida qué se puede hacer con el dato.

## 🎯 Qué aprenderás
- Un esquema de clasificación (**Público / Interno / Confidencial**) como **SKOS**.
- Una política **ODRL** por nivel, con prohibiciones, permisos y deberes.
- Una evaluación mínima: **prohibición ⇒ deniega**; **sin clasificar ⇒ denegado por defecto**.

## ▶️ Ejecutar
```bash
python politicas.py                                                    # matriz nivel × acción × solicitante
python politicas.py --dataset trafico-horario --accion distribute --solicitante externo
python politicas.py --dataset contratos-menores --accion use --solicitante interno   # sin clasificar
```
Genera `esquema_clasificacion.ttl` y `politicas_por_clasificacion.ttl`.

## ⚠️ Importante
`gov:tipoSolicitante` es un **leftOperand propio**, no existe en ODRL core. Un conector real necesitaría un **perfil** que lo defina y una función que sepa evaluarlo. ODRL **describe**; el evaluador de aquí es solo una demostración.

## 🧪 Prueba tú
1. Cambia la política «Interno» para que permita `distribute` y vuelve a ejecutar.
2. Añade un cuarto nivel («Restringido») en `comun/gov.py`.

## ➡️ Siguiente
[`03-Catalogo-y-Glosario`](../03-Catalogo-y-Glosario/)
