import http.cookiejar
import importlib.util
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

AS = Path(__file__).resolve().parent
MODO = sys.argv[1]
assert MODO in ("con", "sin")
BASE = "http://localhost:3000"
UA = "logsguardian-corpus-runner/1.0"
PROXY_HEADERS = {
    "X-REAL-IP": "192.168.65.1",
    "X-Forwarded-For": "192.168.65.1",
    "X-Forwarded-Port": "8080",
    "X-Forwarded-Proto": "http",
}

orig_request = urllib.request.Request


class Req(orig_request):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        if MODO == "con":
            for name, value in PROXY_HEADERS.items():
                self.add_header(name, value)


urllib.request.Request = Req


def load_module(filename, modname):
    spec = importlib.util.spec_from_file_location(modname, AS / filename)
    mod = importlib.util.module_from_spec(spec)
    sys.argv = ["x", "s1"]
    spec.loader.exec_module(mod)
    return mod


legacy = load_module("run_large_corpus.py", "run_large_corpus_s1")
legacy.BASE_URL = BASE
xss = load_module("send_xss_corpus.py", "send_xss_corpus_s1")
xss.BASE_URL = BASE
sys.argv = ["s1", MODO]


def make_opener():
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))


def login(opener, username, password):
    data = urllib.parse.urlencode({"username": username, "password": password}).encode()
    req = urllib.request.Request(f"{BASE}/login", data=data, method="POST")
    req.add_header("User-Agent", UA)
    try:
        resp = opener.open(req, timeout=5)
        return resp.status
    except urllib.error.HTTPError as e:
        return e.code


corpus = [json.loads(l) for l in open(AS / "combined_corpus_round5_20261025.jsonl") if l.strip()]
alice, admin = make_opener(), make_opener()
login_status = {"alice": login(alice, "alice", "alice123"), "admin": login(admin, "admin", "admin123")}

results = []
t0 = time.time()
for spec in corpus:
    opener = admin if spec.get("auth") == "admin" else alice
    if spec["schema"] == "legacy":
        out = legacy.do_request(opener, spec)
    else:
        out = xss.do_request_xss(alice, spec)
    results.append({"id": spec["id"], "category": spec["category"], "status": out.get("status"),
                    "blocked": out.get("blocked"), "error": out.get("error")})
elapsed = time.time() - t0
dest = AS / f"results_s1_config2_{MODO}_cabeceras_run1_20261025.json"
json.dump({"modo": MODO, "cabeceras": PROXY_HEADERS if MODO == "con" else {}, "login_status": login_status,
           "elapsed_s": elapsed, "results": results}, open(dest, "w"), indent=1)
by = {}
for r in results:
    c = by.setdefault(r["category"], [0, 0])
    c[1] += 1
    c[0] += 1 if r["blocked"] else 0
print(MODO, login_status, {k: f"{v[0]}/{v[1]}" for k, v in by.items()}, f"{elapsed:.1f}s")
