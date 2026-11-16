import importlib.util
import json
import sqlite3
import subprocess
import sys
import time
import urllib.request
import urllib.error
import http.cookiejar
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AS = ROOT / "attack-sim"
OUT = ROOT / "docs" / "evidence"
BASE = "http://localhost:3000"
UA = "logsguardian-corpus-runner/1.0"
IDS = ["cmdi_112", "cmdi_134", "cmdi_31", "cmdi_38", "cmdi_6", "cmdi_184", "cmdi_185"]
REPS = 3
PROXY_HEADERS = {
    "X-Real-IP": "192.168.65.1",
    "X-Forwarded-For": "192.168.65.1",
    "X-Forwarded-Port": "8080",
    "X-Forwarded-Proto": "http",
}
VARIANTS = [
    ("v0_sin_cabeceras", {}),
    ("v1_cabeceras_xff", dict(PROXY_HEADERS)),
    ("v2_cabeceras_xff_host_sin_puerto", {**PROXY_HEADERS, "Host": "localhost"}),
]

spec = importlib.util.spec_from_file_location("h", AS / "run_large_corpus.py")
h = importlib.util.module_from_spec(spec)
sys.argv = ["x", "e1"]
spec.loader.exec_module(h)
h.BASE_URL = BASE

orig_request = urllib.request.Request
EXTRA = {}


class Req(orig_request):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        for name, value in EXTRA.items():
            self.add_header(name, value)


urllib.request.Request = Req

corpus = {}
for line in open(AS / "combined_corpus_round5_20261025.jsonl"):
    r = json.loads(line)
    if r["id"] in IDS:
        corpus[r["id"]] = r

opener = h.make_opener()
h.login(opener, "admin", "admin123")

sends = []
for vname, extra in VARIANTS:
    EXTRA.clear()
    EXTRA.update(extra)
    for rep in range(1, REPS + 1):
        for pid in IDS:
            t0 = time.time() * 1000
            out = h.do_request(opener, corpus[pid])
            t1 = time.time() * 1000
            sends.append({"variante": vname, "rep": rep, "id": pid, "status": out.get("status"),
                          "blocked": out.get("blocked"), "t0": t0, "t1": t1})
EXTRA.clear()
time.sleep(2)

cid = subprocess.check_output(
    "COMPOSE_PROJECT_NAME=lsgt6final20261025 docker compose -f docker-compose.yml -f docker-compose.direct.yml ps -q app",
    shell=True, cwd=ROOT, stderr=subprocess.DEVNULL).decode().strip()
tmp = OUT / "e1-events-snapshot-20261025"
tmp.mkdir(exist_ok=True)
for suf in ["", "-wal", "-shm"]:
    subprocess.run(["docker", "cp", f"{cid}:/app/logsguardian-events.db{suf}", str(tmp / f"logsguardian-events.db{suf}")],
                   stderr=subprocess.DEVNULL)
con = sqlite3.connect(str(tmp / "logsguardian-events.db"))
cols = [r[1] for r in con.execute("PRAGMA table_info(detection_events)")]
rows = [dict(zip(cols, r)) for r in con.execute("SELECT * FROM detection_events ORDER BY timestamp")]
ping = [r for r in rows if r["path"] == "/admin/ping"]

matched = 0
for s in sends:
    cands = [r for r in ping if s["t0"] - 5 <= r["timestamp"] <= s["t1"] + 5]
    if len(cands) == 1:
        e = cands[0]
        s["evento"] = {k: e.get(k) for k in ["verdict", "predicted_class", "confidence", "if_score", "user_agent", "client_ip"] if k in e}
        matched += 1
    else:
        s["evento"] = None
        s["eventos_candidatos"] = len(cands)

res = {"columnas_detection_events": cols, "n_envios": len(sends), "n_eventos_ping": len(ping), "n_emparejados": matched,
       "cabeceras_proxy": PROXY_HEADERS, "variantes": [v[0] for v in VARIANTS], "envios": sends}
json.dump(res, open(OUT / "e1-proxy-headers-20261025.json", "w"), indent=1)

summary = {}
for s in sends:
    summary.setdefault(s["id"], {}).setdefault(s["variante"], []).append(s["blocked"])
for pid, d in summary.items():
    print(pid, {v: f"{sum(1 for x in l if x)}/{len(l)}" for v, l in d.items()})
print("columnas:", cols)
print("envios", len(sends), "eventos ping", len(ping), "emparejados", matched)
