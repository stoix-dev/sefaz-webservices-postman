# -*- coding: utf-8 -*-
"""Monta a coleção Postman completa dos webservices da SEFAZ (NF-e, NFC-e, CT-e,
MDF-e) a partir do inventário coletado. Uma pasta por modelo; cada request com
envelope SOAP 1.2, Content-Type com action, variáveis {{}} e descrição."""
import json
from urllib.parse import urlparse

CT = 'application/soap+xml; charset=utf-8; action="{action}"'


def url_obj(u):
    """Destrincha a URL em protocol/host/path para o Postman renderizar."""
    p = urlparse(u)
    return {
        "raw": u,
        "protocol": p.scheme,
        "host": p.hostname.split(".") if p.hostname else [],
        "path": [seg for seg in p.path.split("/") if seg],
    }


def req(nome, url_h, url_p, action, envelope, obs, assina):
    tag = "🔏 assina XML" if assina else "aberto"
    # usa homologacao como URL default (mais seguro p/ teste); prod na descricao.
    padrao = url_h if url_h and url_h.startswith("http") else url_p
    desc = f"[{tag}]\n\n{obs}\n\nHomolog: {url_h}\nProd: {url_p}"
    return {
        "name": nome,
        "request": {
            "method": "POST",
            "header": [{"key": "Content-Type", "value": CT.format(action=action)}],
            "url": url_obj(padrao),
            "body": {"mode": "raw", "raw": envelope},
            "description": desc,
        },
        "response": [],
    }


def folder(nome, desc, items):
    return {"name": nome, "description": desc, "item": items}


data = json.load(open("inventario.json", encoding="utf-8"))

itens = []
for bloco in data["modelos"]:
    reqs = []
    for s in bloco["servicos"]:
        if s.get("metodo") in (None, "n/a"):
            # serviço registrado como inexistente/descontinuado: vira nota
            reqs.append({
                "name": f"(nota) {s['nome']}",
                "request": {"method": "GET", "url": {"raw": ""},
                            "description": s.get("obs", "")},
                "response": [],
            })
            continue
        env = s["envelope"]
        reqs.append(req(s["nome"], s.get("url_homolog", ""), s.get("url_prod", ""),
                        s["soapAction"], env, s.get("obs", ""), s.get("assinaXml", False)))
    itens.append(folder(bloco["modelo"], bloco.get("desc", ""), reqs))

# pasta de eventos (referência, sem request)
if "eventos" in data:
    ev_desc = "Eventos enviados via RecepcaoEvento do respectivo modelo (com tpEvento). Referência de códigos:\n\n"
    for e in data["eventos"]:
        ev_desc += f"- {e['tpEvento']} · {e['nome']} ({e['modelo']}): {e['obs']}\n"
    itens.append(folder("Eventos (referência de tpEvento)", ev_desc, []))

col = {
    "info": {
        "name": "SEFAZ · Catálogo de Webservices (NF-e · NFC-e · CT-e · MDF-e)",
        "description": data["descricao"],
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
    },
    "variable": data["variaveis"],
    "item": itens,
}

json.dump(col, open("postman/SEFAZ-Webservices-Catalogo.postman_collection.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
n = sum(len(f["item"]) for f in itens)
print(f"OK: {len(itens)} pastas, {n} requests/notas")
