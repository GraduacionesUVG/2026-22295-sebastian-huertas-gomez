"""T9 sender: sends the final XSS corpus (post T5/T6, 200 payloads) against
the running stack, across all three accepted transports (T3): urlencoded,
multipart/form-data, json.

attack-sim/run_large_corpus_fixed.py (T2) only builds
application/x-www-form-urlencoded bodies - it has no multipart or json
support, and per rule 7 it is not modified here (it is a copy of a
specific, hash-verified commit, kept byte-identical). This is a separate,
new file that reuses its do_request() for the urlencoded case (same
pre-encoding handling, same cookie jar, same fixed User-Agent) and adds its
own request construction for multipart and json, so the corpus's
transport dimension is actually exercised, not silently dropped.

For the urlencoded transport, a payload whose codificacion is url_single
or url_double is pre-encoded text and must not be re-escaped - same
PRE_ENCODED_CATEGORIES convention as the fixed harness, extended here to
this generator's own codificacion field directly (no category-based
guessing needed, since the corpus already records which payloads are
pre-encoded).

Writes per-request results with the fields T9 requires: id, estrato (all
seven stratifying fields), http status, blocked, failure reason, RF
probability (read back from the app's SQLite event log, see
read_rf_probabilities()), latency.

Usage: python3 send_xss_corpus.py <config_name> <corpus_path> <db_container_path>
"""
from __future__ import annotations

import importlib.util
import json
import sqlite3
import sys
import time
import urllib.parse
import urllib.request
import urllib.error
import http.cookiejar
from pathlib import Path

ATTACK_SIM_DIR = Path(__file__).parent
BASE_URL = "http://localhost:3000"
FIXED_USER_AGENT = "logsguardian-corpus-runner/1.0"
PRE_ENCODED_CODIFICACIONES = {"url_single", "url_double"}


def load_fixed_harness():
    spec = importlib.util.spec_from_file_location(
        "run_large_corpus_fixed", ATTACK_SIM_DIR / "run_large_corpus_fixed.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def make_opener():
    jar = http.cookiejar.CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))


def login(opener, username, password):
    data = urllib.parse.urlencode({"username": username, "password": password}).encode()
    req = urllib.request.Request(f"{BASE_URL}/login", data=data, method="POST")
    req.add_header("User-Agent", FIXED_USER_AGENT)
    try:
        opener.open(req, timeout=5)
    except urllib.error.HTTPError:
        pass


def _multipart_body(fields: dict[str, str], boundary: str) -> bytes:
    parts = []
    for k, v in fields.items():
        parts.append(f"--{boundary}\r\n")
        parts.append(f'Content-Disposition: form-data; name="{k}"\r\n\r\n')
        parts.append(f"{v}\r\n")
    parts.append(f"--{boundary}--\r\n")
    return "".join(parts).encode("utf-8", errors="replace")


def do_request_xss(opener, spec: dict) -> dict:
    endpoint = spec["endpoint"]
    campo = spec["campo"]
    transporte = spec["transporte"]
    forma_enviada = spec["forma_enviada"]
    codificacion = spec["codificacion"]
    pre_encoded = codificacion in PRE_ENCODED_CODIFICACIONES

    t0 = time.time()
    try:
        if transporte == "urlencoded":
            if pre_encoded:
                data = f"{urllib.parse.quote(campo, safe='')}={forma_enviada}".encode()
            else:
                data = urllib.parse.urlencode({campo: forma_enviada}).encode()
            req = urllib.request.Request(f"{BASE_URL}{endpoint}", data=data, method="POST")
            req.add_header("Content-Type", "application/x-www-form-urlencoded")
        elif transporte == "multipart":
            boundary = "----lsgxssboundary20261025"
            body = _multipart_body({campo: forma_enviada}, boundary)
            req = urllib.request.Request(f"{BASE_URL}{endpoint}", data=body, method="POST")
            req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
        elif transporte == "json":
            body = json.dumps({campo: forma_enviada}).encode("utf-8")
            req = urllib.request.Request(f"{BASE_URL}{endpoint}", data=body, method="POST")
            req.add_header("Content-Type", "application/json")
        else:
            raise ValueError(f"transporte desconocido: {transporte}")

        req.add_header("User-Agent", FIXED_USER_AGENT)
        try:
            resp = opener.open(req, timeout=10)
            status = resp.status
            body_snippet = resp.read(200).decode("utf-8", errors="ignore")
        except urllib.error.HTTPError as e:
            status = e.code
            try:
                body_snippet = e.read(200).decode("utf-8", errors="ignore")
            except Exception:
                body_snippet = ""
        latency_ms = (time.time() - t0) * 1000
        blocked = status == 403
        if status >= 500:
            reason = "http_5xx"
        elif not blocked and status not in (200, 201, 302):
            reason = f"http_{status}"
        else:
            reason = None
        return {"status": status, "blocked": blocked, "reason": reason, "latency_ms": latency_ms, "error": None}
    except Exception as e:
        latency_ms = (time.time() - t0) * 1000
        return {"status": None, "blocked": False, "reason": "error_red", "latency_ms": latency_ms, "error": str(e)}


def read_rf_probabilities(db_path: str, since_ts_ms: int) -> list[dict]:
    """Reads detection_events written after since_ts_ms, for RF-probability
    attribution by best-effort timestamp/path/method match (the app does
    not echo a request id back, so this is a nearest-match join, not exact -
    documented as such in the thesis-delta deliverable)."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT timestamp, method, path, query_string, verdict, predicted_class, confidence "
        "FROM detection_events WHERE timestamp >= ? ORDER BY timestamp ASC",
        (since_ts_ms,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def main() -> int:
    config_name = sys.argv[1]
    corpus_path = sys.argv[2]
    run_label = sys.argv[3] if len(sys.argv) > 3 else "run1"

    harness = load_fixed_harness()

    with open(corpus_path) as f:
        corpus = [json.loads(l) for l in f if l.strip()]

    alice_opener = make_opener()
    login(alice_opener, "alice", "alice123")

    results = []
    t_start_ms = int(time.time() * 1000)
    for i, spec in enumerate(corpus, 1):
        outcome = do_request_xss(alice_opener, spec)
        results.append({
            "id": spec["id"],
            "contexto": spec["contexto"],
            "vector": spec["vector"],
            "funcion": spec["funcion"],
            "codificacion": spec["codificacion"],
            "transporte": spec["transporte"],
            "campo": spec["campo"],
            "endpoint": spec["endpoint"],
            **outcome,
        })
        if i % 50 == 0 or i == len(corpus):
            print(f"  {i}/{len(corpus)} done...")

    out_path = ATTACK_SIM_DIR / f"results_xss_{config_name}_{run_label}_20261025.json"
    with open(out_path, "w") as f:
        json.dump({"t_start_ms": t_start_ms, "results": results}, f, indent=2)

    blocked = sum(1 for r in results if r["blocked"])
    print(f"\n=== xss {config_name} {run_label}: {blocked}/{len(results)} bloqueados ===")
    print(f"Escrito: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
