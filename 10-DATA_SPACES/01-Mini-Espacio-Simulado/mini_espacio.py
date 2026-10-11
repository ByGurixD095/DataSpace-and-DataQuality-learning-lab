#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01 · Mini espacio simulado: el ciclo completo con dos «conectores» en Python (sin red).

  python mini_espacio.py                              # escenario feliz con la traza completa
  python mini_espacio.py --escenario sin-credencial   # la startup no ha sido admitida
  python mini_espacio.py --escenario denegado         # finalidad fuera de la oferta
  python mini_espacio.py --escenario revocada         # credencial revocada
  python mini_espacio.py --escenario proveedor-no-admitido
  python mini_espacio.py --escenario todos            # tabla resumen de los cinco
  python mini_espacio.py --interactivo                # tú eliges quién pide qué y para qué

Integra los otros experimentos: admisión por rulebook (05) → credencial firmada (04) → catálogo con
ofertas (02) → negociación y acuerdo (03) → transferencia.

⚠️ SIMULACIÓN DIDÁCTICA. Los nombres de mensajes y de estados se inspiran en el Dataspace Protocol,
pero esto NO es una implementación conforme: no hay red, ni JSON-LD real, ni todos los estados ni
todos los campos. Para ver una implementación real, ve a 11-Eclipse-EDC.
Requiere: rdflib, cryptography
"""
import argparse, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "comun"))
import espacio as e


# ──────────────────────────────────────────────────────────────────────────────
class Traza:
    def __init__(self, activa=True):
        self.activa, self.n = activa, 0

    def msg(self, de, a, tipo, **campos):
        self.n += 1
        if self.activa:
            detalle = "  ".join(f"{k}={v}" for k, v in campos.items())
            print(f"  {self.n:>2}. {de:>17} ─▶ {a:<17} {tipo}" + (f"\n      {'':>17}    {detalle}" if detalle else ""))

    def nota(self, texto):
        if self.activa:
            print(f"      ↳ {texto}")


class ConectorProveedor:
    """Publica un catálogo y atiende catálogo, negociación y transferencia. Solo existe si el rulebook lo admite."""

    def __init__(self, pid, traza):
        self.pid, self.traza = pid, traza
        self.catalogo = e.catalogo_rdf(e.ofertas(), pid)
        self.negociaciones, self.transferencias, self.registro = {}, {}, []

    def _autenticar(self, cred):
        ok, motivo = e.verificar_credencial(cred)
        self.traza.nota(f"{self.pid} verifica la credencial: {motivo}")
        return ok, motivo

    def catalog_request(self, cred):
        ok, motivo = self._autenticar(cred)
        if not ok:
            return None, motivo
        return [f for f in e.ofertas() if f["proveedor"] == self.pid and f["finalidades"]], "ok"

    def contract_request(self, cred, dataset, finalidad):
        ok, motivo = self._autenticar(cred)
        nid = f"neg-{len(self.negociaciones) + 1:03d}"
        if not ok:
            self.negociaciones[nid] = "TERMINATED"; return nid, "TERMINATED", motivo, []
        self.negociaciones[nid] = "REQUESTED"
        permitido, motivo, deberes = e.evaluar_peticion(self.catalogo, dataset, finalidad)
        self.traza.nota(f"{self.pid} evalúa la petición contra la oferta ODRL: {motivo}")
        self.negociaciones[nid] = "AGREED" if permitido else "TERMINATED"
        return nid, self.negociaciones[nid], motivo, deberes

    def verification(self, nid):
        if self.negociaciones.get(nid) == "AGREED":
            self.negociaciones[nid] = "VERIFIED"; self.negociaciones[nid] = "FINALIZED"
        return self.negociaciones.get(nid)

    def transfer_request(self, nid, dataset):
        if self.negociaciones.get(nid) != "FINALIZED":
            return "TERMINATED", None
        tid = f"trf-{len(self.transferencias) + 1:03d}"
        self.transferencias[tid] = "STARTED"
        datos = [{"dataset": dataset, "fila": i, "valor": round(0.5 + i * 0.07, 2)} for i in range(1, 4)]   # datos sintéticos
        self.transferencias[tid] = "COMPLETED"
        return "COMPLETED", datos

    def usage_report(self, consumidor, dataset, finalidad):
        self.registro.append(f"{consumidor} informa del uso de {dataset} (finalidad: {finalidad})")


def ejecutar(consumidor, proveedor, dataset, finalidad, cred, traza):
    """Un intercambio completo. Devuelve (resultado, motivo)."""
    directorio = {p["id"]: ConectorProveedor(p["id"], traza) for p in e.participantes()
                  if p["rol"] == "proveedor" and e.evaluar_participante(p)[0] != "no admitido"}
    if traza.activa:
        print("\n🏛️  ADMISIÓN (rulebook aplicado a cada participante)")
        for p in e.participantes():
            d, res = e.evaluar_participante(p)
            falta = [r["id"] for r, ok in res if not ok]
            print(f"   {e.ICONO_DECISION[d]} {p['id']:<19} {d}" + (f"   (incumple {', '.join(falta)})" if falta else ""))
        print(f"   Directorio del espacio: {', '.join(directorio) or '(vacío)'}\n")
        print(f"🔄 INTERCAMBIO: {consumidor} quiere «{dataset}» de {proveedor} para «{finalidad}»\n" + "─" * 86)
    if proveedor not in directorio:
        traza.msg(consumidor, "directorio", "BuscarProveedor", proveedor=proveedor)
        traza.nota(f"«{proveedor}» no está en el directorio: no fue admitido y su catálogo no se publica")
        return "❌", f"{proveedor} no está en el espacio (no admitido)"
    prov = directorio[proveedor]

    traza.msg(consumidor, proveedor, "CatalogRequestMessage")
    catalogo, motivo = prov.catalog_request(cred)
    if catalogo is None:
        traza.msg(proveedor, consumidor, "CatalogError", causa=motivo)
        return "❌", f"catálogo rechazado: {motivo}"
    traza.msg(proveedor, consumidor, "Catalog", ofertas=len(catalogo))
    if dataset not in {f["id"] for f in catalogo}:
        traza.nota(f"«{dataset}» no aparece en el catálogo de {proveedor}")
        return "❌", f"«{dataset}» no está ofertado por {proveedor}"

    traza.msg(consumidor, proveedor, "ContractRequestMessage", dataset=dataset, finalidad=finalidad)
    nid, estado, motivo, deberes = prov.contract_request(cred, dataset, finalidad)
    if estado != "AGREED":
        traza.msg(proveedor, consumidor, "ContractNegotiationTerminationMessage", estado="TERMINATED", causa=motivo)
        return "❌", f"negociación terminada: {motivo}"
    traza.msg(proveedor, consumidor, "ContractAgreementMessage", negociacion=nid, estado="AGREED", deberes=",".join(deberes) or "ninguno")
    traza.msg(consumidor, proveedor, "ContractAgreementVerificationMessage", negociacion=nid)
    traza.msg(proveedor, consumidor, "ContractNegotiationEventMessage", estado=prov.verification(nid))

    traza.msg(consumidor, proveedor, "TransferRequestMessage", negociacion=nid)
    estado_t, datos = prov.transfer_request(nid, dataset)
    traza.msg(proveedor, consumidor, "TransferStartMessage", estado="STARTED")
    traza.msg(proveedor, consumidor, "TransferCompletionMessage", estado=estado_t, filas=len(datos or []))
    if traza.activa and datos:
        for fila in datos:
            print(f"      datos: {fila}")
    if "inform" in deberes:
        traza.msg(consumidor, proveedor, "UsageReport (mensaje propio del lab)", cumple="deber inform")
        prov.usage_report(consumidor, dataset, finalidad)
        traza.nota(f"registro de usos de {proveedor}: {prov.registro[-1]}")
    return "✅", f"datos recibidos amparados por el acuerdo {nid}"


def credencial_para(consumidor, caso):
    """Qué credencial presenta el consumidor según el escenario."""
    if caso == "revocada":
        return e.emitir_credencial(consumidor, cred_id="cred-startup-analitica-antigua", forzar=True)
    try:
        return e.emitir_credencial(consumidor)
    except PermissionError:
        return None                                   # no admitido → no hay credencial que presentar


ESCENARIOS = {  # nombre: (consumidor, proveedor, dataset, finalidad)
    "feliz": ("universidad", "ayuntamiento", "calidad-aire", "investigacion"),
    "sin-credencial": ("startup-analitica", "ayuntamiento", "calidad-aire", "investigacion"),
    "denegado": ("universidad", "ayuntamiento", "calidad-aire", "comercial"),
    "revocada": ("startup-analitica", "ayuntamiento", "calidad-aire", "investigacion"),
    "proveedor-no-admitido": ("universidad", "empresa-movilidad", "flota-bus-posiciones", "investigacion"),
}

ap = argparse.ArgumentParser()
ap.add_argument("--escenario", default="feliz", choices=list(ESCENARIOS) + ["todos"])
ap.add_argument("--interactivo", action="store_true")
a = ap.parse_args()

if a.interactivo:
    def elegir(titulo, opciones, defecto=0):
        print(f"\n{titulo}")
        for i, o in enumerate(opciones, 1):
            print(f"  {i}. {o}")
        try:
            r = input(f"  elige [1-{len(opciones)}, vacío = {defecto + 1}] ").strip()
        except EOFError:
            r = ""
        return opciones[int(r) - 1] if r.isdigit() and 1 <= int(r) <= len(opciones) else opciones[defecto]
    cons = elegir("¿Quién pide los datos?", [p["id"] for p in e.participantes()], 1)
    prov = elegir("¿A qué proveedor?", [p["id"] for p in e.participantes() if p["rol"] == "proveedor"])
    ds = elegir("¿Qué dataset?", [f["id"] for f in e.ofertas() if f["proveedor"] == prov])
    try:
        fin = input("\n¿Para qué finalidad? [investigacion] ").strip() or "investigacion"
    except EOFError:
        fin = "investigacion"
    modo = elegir("¿Qué credencial presenta?", ["la que le corresponde (si la tiene)", "ninguna", "una manipulada"])
    cred = credencial_para(cons, "normal")
    if modo == "ninguna":
        cred = None
    elif modo == "una manipulada":
        cred = e.emitir_credencial("universidad"); cred["sujeto"] = cons
    print(f"\n{'=' * 86}\n🎬 {cons} → {prov}/{ds} («{fin}»)")
    res, motivo = ejecutar(cons, prov, ds, fin, cred, Traza(True))
    print(f"\n{res} {motivo}")
elif a.escenario == "todos":
    print("\n📋 RESUMEN DE ESCENARIOS\n" + "─" * 86)
    for nombre, (c, p, d, f) in ESCENARIOS.items():
        res, motivo = ejecutar(c, p, d, f, credencial_para(c, nombre), Traza(False))
        print(f"{res} {nombre:<22} {c} → {p}/{d} («{f}»)\n      {motivo}")
else:
    c, p, d, f = ESCENARIOS[a.escenario]
    print(f"\n🎬 ESCENARIO «{a.escenario}»")
    res, motivo = ejecutar(c, p, d, f, credencial_para(c, a.escenario), Traza(True))
    print(f"\n{res} {motivo}")
    print("\n💡 Fíjate en el orden: identidad (credencial) → catálogo → negociación (oferta ODRL) → acuerdo → transferencia."
          "\n   Los datos solo se mueven cuando existe un acuerdo FINALIZED; todo lo anterior es descubrimiento y confianza.")
