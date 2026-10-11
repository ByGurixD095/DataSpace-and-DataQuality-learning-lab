# 🤝 03 · Oferta y acuerdo

> **Idea:** una `odrl:Offer` es una **propuesta** (sin assignee); un `odrl:Agreement` es un **contrato** con partes identificadas y la finalidad ya fijada.

## 🎯 Qué aprenderás
- Evaluar una petición contra una oferta (acción `use` + restricción `purpose isAnyOf`).
- Cómo nace un acuerdo a partir de una oferta aceptada.
- Que un **deber** (`inform`) no lo cumple ODRL: genera una obligación que debe auditar el conector y el marco de gobierno.

## ▶️ Ejecutar
```bash
python oferta_acuerdo.py
python oferta_acuerdo.py --dataset calidad-aire --finalidad comercial --consumidor universidad
```
Genera `ofertas.ttl` y `acuerdos.ttl`.

## 👀 Qué verás
2 peticiones aceptadas, 3 rechazadas: finalidad fuera de la oferta (dos veces) y dataset inexistente (el padrón no se publica).

## ⚠️ Importante
`odrl:purpose` es un operando de ODRL core, pero **cómo se comprueba una finalidad** (¿declaración? ¿auditoría?) no lo define ODRL. Aquí solo se compara texto.

## 🧪 Prueba tú
1. Añade `comercial` a las finalidades de `ruido-urbano` en `datos/ofertas.csv`.
2. Cambia `deber_informar` a `no` y comprueba que el registro de deberes cambia.

## ➡️ Siguiente
[`02-Catalogo-Federado`](../02-Catalogo-Federado/)
