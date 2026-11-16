#!/usr/bin/env python3
"""Run the large attack corpus against the currently-running stack.

Usage: python3 run_large_corpus.py <config_name> [--limit N]

config_name is a free-form label (e.g. "config1", "config2", "config3a",
"config3b") used only to tag the output file - it does not select or start
anything, the stack must already be up on http://localhost:3000.
"""
import json
import sys
import time
import http.cookiejar
import urllib.request
import urllib.parse
import urllib.error
from collections import defaultdict

BASE_URL = "http://localhost:3000"
CORPUS_PATH = "attack-sim/large_corpus_requests.json"
# Fixed across every request: User-Agent is part of logsguardian's feature
# vector, and confidence for short/low-signal payloads sits close enough to
# the 0.35 block threshold that switching HTTP clients (curl vs urllib's
# default UA) was observed to flip individual verdicts. Pinning this keeps
# results comparable across configs and reproducible independent of which
# client runs the script.
FIXED_USER_AGENT = "logsguardian-corpus-runner/1.0"

CONFIG_NAME = sys.argv[1] if len(sys.argv) > 1 else "unknown"
LIMIT = None
if "--limit" in sys.argv:
    LIMIT = int(sys.argv[sys.argv.index("--limit") + 1])


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


def do_request(opener, req_spec):
    method = req_spec["method"]
    path = req_spec["path"]
    param = req_spec["param"]
    payload = req_spec["payload"]
    extra = req_spec.get("extra", {})

    if method == "GET":
        qs = urllib.parse.urlencode({param: payload})
        url = f"{BASE_URL}{path}?{qs}"
        req = urllib.request.Request(url, method="GET")
    else:
        body = {param: payload, **extra}
        data = urllib.parse.urlencode(body).encode()
        req = urllib.request.Request(f"{BASE_URL}{path}", data=data, method="POST")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("User-Agent", FIXED_USER_AGENT)

    try:
        resp = opener.open(req, timeout=5)
        status = resp.status
        headers = dict(resp.headers)
        body_snippet = resp.read(200).decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as e:
        status = e.code
        headers = dict(e.headers) if e.headers else {}
        try:
            body_snippet = e.read(200).decode("utf-8", errors="ignore")
        except Exception:
            body_snippet = ""
    except Exception as e:
        return {"status": "error", "error": str(e), "blocked": None, "layer_guess": None}

    blocked = status == 403
    # Best-effort layer attribution, informational only - not the primary
    # metric. App responses carry X-Powered-By: Express; a bare WAF block
    # (nginx default error page, no app headers) doesn't.
    if not blocked:
        layer_guess = "n/a"
    elif "X-Powered-By" in headers or '"error":"Forbidden"' in body_snippet:
        layer_guess = "app"
    else:
        layer_guess = "waf-or-unknown"

    return {"status": status, "blocked": blocked, "layer_guess": layer_guess}


def main():
    with open(CORPUS_PATH) as f:
        corpus = json.load(f)
    if LIMIT:
        # Take a spread across categories, not just the first N of one category.
        by_cat = defaultdict(list)
        for r in corpus:
            by_cat[r["category"]].append(r)
        corpus = []
        per_cat = max(1, LIMIT // len(by_cat))
        for cat, items in by_cat.items():
            corpus.extend(items[:per_cat])
        corpus = corpus[:LIMIT]

    alice_opener = make_opener()
    admin_opener = make_opener()
    login(alice_opener, "alice", "alice123")
    login(admin_opener, "admin", "admin123")

    results = []
    t0 = time.time()
    for i, req_spec in enumerate(corpus, 1):
        opener = admin_opener if req_spec.get("auth") == "admin" else alice_opener
        outcome = do_request(opener, req_spec)
        results.append({
            "id": req_spec["id"],
            "category": req_spec["category"],
            **outcome,
        })
        if i % 100 == 0 or i == len(corpus):
            print(f"  {i}/{len(corpus)} done...")

    elapsed = time.time() - t0
    out_path = f"attack-sim/results_{CONFIG_NAME}.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    by_category = defaultdict(lambda: {"total": 0, "blocked": 0})
    for r in results:
        by_category[r["category"]]["total"] += 1
        if r["blocked"]:
            by_category[r["category"]]["blocked"] += 1

    print(f"\n=== {CONFIG_NAME} Summary ({elapsed:.1f}s, {len(results)} requests) ===")
    for cat, counts in sorted(by_category.items()):
        rate = counts["blocked"] / counts["total"] * 100 if counts["total"] else 0
        print(f"  {cat}: {counts['blocked']}/{counts['total']} ({rate:.1f}%)")
    print(f"\nResults written to {out_path}")


if __name__ == "__main__":
    main()
