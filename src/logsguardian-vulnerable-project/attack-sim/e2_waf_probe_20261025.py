import importlib.util
import http.cookiejar
import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AS = ROOT / "attack-sim"
IDS = ["cmdi_6", "cmdi_184", "cmdi_185", "cmdi_112", "cmdi_134", "cmdi_31", "cmdi_38", "cmdi_0"]

spec = importlib.util.spec_from_file_location("h", AS / "run_large_corpus.py")
h = importlib.util.module_from_spec(spec)
sys.argv = ["x", "e2"]
spec.loader.exec_module(h)
h.BASE_URL = "http://127.0.0.1:9312"

orig_request = urllib.request.Request


class Req(orig_request):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.add_header("Host", "localhost:3000")


urllib.request.Request = Req

corpus = {}
for line in open(AS / "combined_corpus_round5_20261025.jsonl"):
    r = json.loads(line)
    if r["id"] in IDS:
        corpus[r["id"]] = r

jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
opener.addheaders = [("Cookie", "connect.sid=s%3Afixedcookie20261025")]

audit = ROOT / "docs" / "evidence" / "e2-waf-audit-20261025" / "audit.log"
out = []
for pid in IDS:
    before = sum(1 for _ in open(audit))
    r = h.do_request(opener, corpus[pid])
    time.sleep(0.4)
    lines = open(audit).read().splitlines()
    new = [json.loads(l)["transaction"] for l in lines[before:]]
    rec = new[-1] if new else None
    msgs = []
    if rec:
        for m in rec.get("messages", []):
            d = m["details"]
            msgs.append({"ruleId": d.get("ruleId"), "message": m["message"], "severity": d.get("severity"), "data": d.get("data")})
    out.append({"id": pid, "status_cliente": r.get("status"), "http_code_registro": rec["response"]["http_code"] if rec else None,
                "interrumpida": rec.get("is_interrupted") if rec else None, "uri": rec["request"]["uri"] if rec else None, "reglas": msgs})
json.dump(out, open(ROOT / "docs" / "evidence" / "e2-waf-probe-20261025.json", "w"), ensure_ascii=False, indent=1)
for o in out:
    print(o["id"], o["status_cliente"], o["http_code_registro"], o["interrumpida"], [(m["ruleId"], m["severity"]) for m in o["reglas"]])
