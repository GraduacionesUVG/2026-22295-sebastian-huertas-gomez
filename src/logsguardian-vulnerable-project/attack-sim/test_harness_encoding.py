"""T2b: verifies that attack-sim/run_large_corpus_fixed.py puts the exact
same bytes on the wire that the corpus records as the payload - for both
transports (GET query string, POST urlencoded body) and both payload
classes (pre-encoded categories that must not be re-escaped, and
non-pre-encoded categories that go through normal urlencode()).

Does not touch the real app. Points the harness at a local capture server
(capture_server.py) that records the raw request target / raw body bytes
exactly as received, with no parsing. The expected wire form is computed
independently in this file, not by calling into the code under test.

Exits 0 and prints PASS per case on success. On the first mismatch, prints
the case, the expected and the captured bytes, and exits 1 - per the task
rules, a failure here must stop and be reported, not be worked around.

Usage: python3 test_harness_encoding.py
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import http.cookiejar
from pathlib import Path

ATTACK_SIM_DIR = Path(__file__).parent
CAPTURE_PORT = 8899
CAPTURE_LOG = ATTACK_SIM_DIR / "capture_server_output.jsonl"

CASES = [
    {
        "label": "path_traversal (GET, doble-codificado, pre_encoded=True)",
        "req_spec": {
            "id": "path_traversal_17", "category": "path_traversal", "method": "GET",
            "path": "/posts/1/attachment", "param": "file",
            "payload": "%252e%252e%252f%252e%252e%252fboot.ini", "extra": {}, "auth": "alice",
        },
        "expect_raw_target": "/posts/1/attachment?file=%252e%252e%252f%252e%252e%252fboot.ini",
    },
    {
        "label": "cmdi (POST, con espacio y %-codificado, pre_encoded=True)",
        "req_spec": {
            "id": "cmdi_0", "category": "cmdi", "method": "POST",
            "path": "/admin/ping", "param": "host",
            "payload": "127.0.0.1%26%26echo LSG_CMDI_MARKER %23", "extra": {}, "auth": "admin",
        },
        "expect_raw_body": "host=127.0.0.1%26%26echo LSG_CMDI_MARKER %23",
    },
    {
        "label": "sqli (GET, no pre-codificado, debe pasar por urlencode normal)",
        "req_spec": {
            "id": "sqli_0", "category": "sqli", "method": "GET",
            "path": "/posts/search", "param": "q",
            "payload": 'test") AND 8198=2485#', "extra": {}, "auth": "alice",
        },
        "expect_raw_target": "/posts/search?" + urllib.parse.urlencode({"q": 'test") AND 8198=2485#'}),
    },
    {
        "label": "xss (POST, no pre-codificado, un solo payload real confirmado por ZAP)",
        "req_spec": {
            "id": "xss_0", "category": "xss", "method": "POST",
            "path": "/profile", "param": "bio",
            "payload": "</div><scrIpt>alert(1);</scRipt><div>", "extra": {}, "auth": "alice",
        },
        "expect_raw_body": urllib.parse.urlencode({"bio": "</div><scrIpt>alert(1);</scRipt><div>"}),
    },
]


def load_harness():
    spec = importlib.util.spec_from_file_location(
        "run_large_corpus_fixed", ATTACK_SIM_DIR / "run_large_corpus_fixed.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    if CAPTURE_LOG.exists():
        CAPTURE_LOG.unlink()

    server_proc = subprocess.Popen(
        [sys.executable, str(ATTACK_SIM_DIR / "capture_server.py"), str(CAPTURE_PORT), str(CAPTURE_LOG)]
    )
    time.sleep(0.5)

    try:
        harness = load_harness()
        harness.BASE_URL = f"http://127.0.0.1:{CAPTURE_PORT}"

        jar = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

        for case in CASES:
            harness.do_request(opener, case["req_spec"])

        time.sleep(0.2)
        lines = [json.loads(l) for l in CAPTURE_LOG.read_text().splitlines() if l.strip()]

        if len(lines) != len(CASES):
            print(f"FALLO: se esperaban {len(CASES)} peticiones capturadas, llegaron {len(lines)}")
            return 1

        all_pass = True
        for case, captured in zip(CASES, lines):
            if "expect_raw_target" in case:
                expected = case["expect_raw_target"]
                actual = captured["raw_target"]
                field = "raw_target"
            else:
                expected = case["expect_raw_body"]
                actual = captured["raw_body"]
                field = "raw_body"

            if actual == expected:
                print(f"PASS  {case['label']}")
            else:
                all_pass = False
                print(f"FALLO {case['label']}")
                print(f"  campo esperado ({field}): {expected!r}")
                print(f"  campo capturado ({field}): {actual!r}")

        return 0 if all_pass else 1
    finally:
        server_proc.terminate()
        server_proc.wait(timeout=5)


if __name__ == "__main__":
    sys.exit(main())
