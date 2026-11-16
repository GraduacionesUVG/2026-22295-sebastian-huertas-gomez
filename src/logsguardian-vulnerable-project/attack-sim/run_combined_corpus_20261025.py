"""Combined runner for the four-configuration comparison (2026-10-25).

Reuses, unmodified:
  - attack-sim/run_large_corpus_fixed.py's do_request() for "legacy" schema
    entries (sqli, path_traversal, cmdi) - same pre-encoding handling
    already verified in T4/T2b of the XSS task.
  - attack-sim/send_xss_corpus.py's do_request_xss() for "xss_v2" schema
    entries - same multi-transport handling already verified there.

Does not reimplement either; both are imported by file path and called
directly, so a fix to either upstream file is picked up automatically
without touching this file.

Usage: python3 run_combined_corpus_20261025.py <config_name> <corpus_path> <run_label>
Writes attack-sim/results_combined_<config_name>_<run_label>_20261025.json
"""
from __future__ import annotations

import importlib.util
import json
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


def load_module(filename: str, modname: str):
    spec = importlib.util.spec_from_file_location(modname, ATTACK_SIM_DIR / filename)
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


def estrato_for(spec: dict) -> dict:
    if spec["schema"] == "legacy":
        return {"method": spec["method"], "path": spec["path"], "param": spec["param"]}
    return {
        "contexto": spec["contexto"], "vector": spec["vector"], "funcion": spec["funcion"],
        "codificacion": spec["codificacion"], "transporte": spec["transporte"], "campo": spec["campo"],
    }


def main() -> int:
    config_name = sys.argv[1]
    corpus_path = sys.argv[2]
    run_label = sys.argv[3]

    legacy_harness = load_module("run_large_corpus_fixed.py", "run_large_corpus_fixed")
    legacy_harness.BASE_URL = BASE_URL
    xss_harness = load_module("send_xss_corpus.py", "send_xss_corpus")
    xss_harness.BASE_URL = BASE_URL

    with open(corpus_path) as f:
        corpus = [json.loads(l) for l in f if l.strip()]

    alice_opener = make_opener()
    admin_opener = make_opener()
    login(alice_opener, "alice", "alice123")
    login(admin_opener, "admin", "admin123")

    results = []
    t0 = time.time()
    for i, spec in enumerate(corpus, 1):
        opener = admin_opener if spec.get("auth") == "admin" else alice_opener
        req_t0 = time.time()
        if spec["schema"] == "legacy":
            outcome = legacy_harness.do_request(opener, spec)
            outcome["latency_ms"] = (time.time() - req_t0) * 1000
        else:
            outcome = xss_harness.do_request_xss(alice_opener, spec)

        results.append({
            "id": spec["id"],
            "category": spec["category"],
            "estrato": estrato_for(spec),
            "status": outcome.get("status"),
            "blocked": outcome.get("blocked"),
            "layer_guess": outcome.get("layer_guess"),
            "reason": outcome.get("reason"),
            "error": outcome.get("error"),
            "latency_ms": outcome.get("latency_ms"),
        })
        if i % 100 == 0 or i == len(corpus):
            print(f"  {i}/{len(corpus)} done...")

    elapsed = time.time() - t0
    out_path = ATTACK_SIM_DIR / f"results_combined_{config_name}_{run_label}_20261025.json"
    with open(out_path, "w") as f:
        json.dump({"config": config_name, "run": run_label, "elapsed_s": elapsed, "results": results}, f, indent=2)

    from collections import defaultdict
    by_cat = defaultdict(lambda: {"total": 0, "blocked": 0})
    for r in results:
        by_cat[r["category"]]["total"] += 1
        if r["blocked"]:
            by_cat[r["category"]]["blocked"] += 1

    print(f"\n=== {config_name} {run_label} ({elapsed:.1f}s, {len(results)} requests) ===")
    for cat, c in sorted(by_cat.items()):
        rate = c["blocked"] / c["total"] * 100 if c["total"] else 0
        print(f"  {cat}: {c['blocked']}/{c['total']} ({rate:.1f}%)")
    print(f"Escrito: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
