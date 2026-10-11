# 🔐 04 · Confianza y credenciales

> **Idea:** en un espacio descentralizado no hay un login central. La autoridad **firma** una credencial de adhesión y cualquiera puede **comprobar** la firma con su clave pública.

## 🎯 Qué aprenderás
- Que la credencial es la versión técnica del *acuerdo de adhesión* de `09`.
- Firma **Ed25519**: la autoridad firma con su clave privada; los demás verifican con la pública.
- El orden de comprobación: presencia → emisor reconocido → firma → vigencia → revocación.
- Que la firma protege la **autenticidad**; la caducidad y la revocación se comprueban aparte.

## ▶️ Ejecutar
```bash
python credenciales.py                          # 6 casos
python credenciales.py --emitir universidad     # emite y guarda credenciales/universidad.json
python credenciales.py --verificar credenciales/universidad.json
python credenciales.py --emitir empresa-movilidad   # el rulebook no la admite → no se emite
```

## ⚠️ Importante
Es una **simulación**: no usa DID ni credenciales verificables del W3C, y la clave sale de una **semilla fija** para ser reproducible (en un sistema real, la clave privada jamás se deriva así ni se publica). La revocación es una lista en un fichero.

## 🧪 Prueba tú
1. Edita a mano `credenciales/universidad.json` (cambia el sujeto) y verifícala.
2. Añade el id de la credencial de la universidad a `datos/revocadas.json`.

## ➡️ Siguiente
[`03-Oferta-y-Acuerdo`](../03-Oferta-y-Acuerdo/)
