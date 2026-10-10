#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
06 · Gobierno de un espacio de datos: ¿quién puede entrar y con qué reglas?

  python espacio.py                          # evalúa a todos los participantes contra el rulebook
  python espacio.py --participante startup-analitica   # detalle de uno
  python espacio.py --rulebook               # muestra las reglas
  python espacio.py --alta                   # cuestionario interactivo: ¿entrarías en el espacio?

Decisión:  alguna regla OBLIGATORIA incumplida → ❌ no admitido
           solo RECOMENDADAS incumplidas       → ⚠️  admitido con recomendaciones
           todo cumplido                        → ✅ admitido

Solo usa la biblioteca estándar. Es un juego de conceptos (autoridad de gobernanza, rulebook, adhesión),
no una implementación del DSSC Blueprint.
"""
import argparse, csv, json, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument("--participante"); ap.add_argument("--rulebook", action="store_true"); ap.add_argument("--alta", action="store_true")
a = ap.parse_args()

RB = json.loads((AQUI / "rulebook.json").read_text(encoding="utf-8"))
REGLAS = RB["reglas"]
ICONO = {"ok": "✅", "obligatoria": "❌", "recomendada": "⚠️ "}


def aplica(regla, p):
    if p["rol"] not in regla["aplica_a"]:
        return False
    cond = regla.get("condicion")
    return not cond or p.get(cond) == "si"


def evaluar(p):
    """→ (decision, [(regla, cumple)]) solo con las reglas que le aplican."""
    res = [(r, p.get(r["campo"]) == "si") for r in REGLAS if aplica(r, p)]
    if any(not ok and r["nivel"] == "obligatoria" for r, ok in res):
        return "❌ no admitido", res
    if any(not ok for _, ok in res):
        return "⚠️  admitido con recomendaciones", res
    return "✅ admitido", res


def detalle(p):
    dec, res = evaluar(p)
    print(f"\n🏛️  {p['nombre']}  ({p['rol']})  →  {dec}\n" + "─" * 64)
    for r, ok in res:
        print(f"   {ICONO['ok'] if ok else ICONO[r['nivel']]} {r['id']} {r['texto']}" + ("" if ok else f"   [{r['nivel']}]"))
    pendientes = [r for r, ok in res if not ok and r["nivel"] == "obligatoria"]
    if pendientes:
        print("   → Para entrar le falta: " + ", ".join(r["id"] for r in pendientes))


if a.rulebook:
    print(f"\n📜 {RB['nombre']}\n   ⚠️  {RB['aviso']}\n")
    for r in REGLAS:
        extra = f" (solo si {r['condicion'].replace('_', ' ')})" if r.get("condicion") else ""
        print(f"   {r['id']} [{r['nivel']:<11}] {r['texto']}{extra}  — aplica a: {', '.join(r['aplica_a'])}")
    sys.exit(0)

if a.alta:
    def pregunta(txt):
        try:
            return input(f"   {txt} [s/N] ").strip().lower() in ("s", "si", "sí", "y", "yes")
        except EOFError:
            return False
    print("\n📝 ALTA EN EL ESPACIO DE DATOS (responde s/N; vacío = no)\n")
    try:
        rol = input("   ¿Serás 'proveedor' o 'consumidor'? [consumidor] ").strip().lower()
    except EOFError:
        rol = ""
    p = {"nombre": "Tu organización", "rol": "proveedor" if rol.startswith("p") else "consumidor"}
    p["trata_datos_personales"] = "si" if pregunta("¿Tratas datos personales?") else "no"
    for r in REGLAS:
        if aplica(r, p):
            p[r["campo"]] = "si" if pregunta(f"{r['id']} {r['texto']}?") else "no"
    detalle(p)
    sys.exit(0)

with open(AQUI / "participantes.csv", newline="", encoding="utf-8") as f:
    parts = list(csv.DictReader(f))

if a.participante:
    p = next((x for x in parts if x["id"] == a.participante), None)
    if not p:
        sys.exit(f"No existe «{a.participante}». Opciones: {', '.join(x['id'] for x in parts)}")
    detalle(p)
    sys.exit(0)

print(f"\n🏛️  ADHESIÓN AL ESPACIO · {len(parts)} solicitudes\n" + "─" * 64)
for p in parts:
    dec, res = evaluar(p)
    falta = [r["id"] for r, ok in res if not ok]
    print(f"   {p['nombre']:<28} {p['rol']:<11} {dec}" + (f"   (incumple: {', '.join(falta)})" if falta else ""))
print("\nUsa --participante ID para ver el detalle, --rulebook para las reglas o --alta para probar tu caso.")
