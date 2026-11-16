import importlib.util
import json
import subprocess
import sys
from collections import Counter

A = "attack-sim/"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.argv = ["x", "r6"]
    spec.loader.exec_module(mod)
    return mod


class FakeResp:
    status = 200
    headers = {}

    def read(self, n=-1):
        return b""


class FakeOpener:
    def __init__(self):
        self.captured = None

    def open(self, req, timeout=5):
        self.captured = (req.get_method(), req.full_url, req.data, tuple(sorted(req.header_items())))
        return FakeResp()


old = load(A + "run_large_corpus_pre_fix_20261025.py", "old_exec")
new = load(A + "run_large_corpus.py", "new_exec")
corpus = json.loads(subprocess.check_output(["git", "show", "af61eba:attack-sim/large_corpus_requests.json"]))
assert len(corpus) == 590

res = {}
detail = {}
for spec in corpus:
    o, n = FakeOpener(), FakeOpener()
    old.do_request(o, spec)
    new.do_request(n, spec)
    cat = spec["category"]
    transport = f"{spec['method']} " + ("consulta" if spec["method"] == "GET" else "formulario application/x-www-form-urlencoded")
    key = (cat, transport)
    r = res.setdefault(key, {"n": 0, "identicas": 0, "distintas": 0})
    r["n"] += 1
    if o.captured == n.captured:
        r["identicas"] += 1
    else:
        r["distintas"] += 1
        detail.setdefault(f"{cat}|{transport}", []).append(spec["id"])

out = {
    "descripcion": "Peticiones construidas por el ejecutor anterior (00ea3a3^) y por el corregido, sin red, para los 590 payloads de la Ronda 4 (corpus de af61eba); se compara metodo, URL, cuerpo y cabeceras",
    "por_categoria_y_transporte": [{"categoria": k[0], "transporte": k[1], **v} for k, v in sorted(res.items())],
    "ids_con_peticion_distinta_por_grupo_primeros_5": {k: v[:5] for k, v in detail.items()},
    "total_distintas": sum(v["distintas"] for v in res.values()),
    "tipos_de_payload_en_los_40": {},
}
M3a = {r["id"] for r in json.load(open(A + "results_config3a.json")) if not r.get("blocked")} if False else None
r3a = json.loads(subprocess.check_output(["git", "show", "af61eba:attack-sim/results_config3a.json"]))
miss = [r["id"] for r in r3a if not r.get("blocked")]
byid = {s["id"]: s for s in corpus}
fake_diff = []
for i in miss:
    o, n = FakeOpener(), FakeOpener()
    old.do_request(o, byid[i])
    new.do_request(n, byid[i])
    if o.captured != n.captured:
        fake_diff.append(i)
out["tipos_de_payload_en_los_40"] = dict(Counter((byid[i]["category"], byid[i]["method"]) .__str__() for i in miss))
out["los_40_con_peticion_distinta"] = fake_diff
json.dump(out, open("docs/evidence/r6-ejecutor-peticiones-20261025.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
