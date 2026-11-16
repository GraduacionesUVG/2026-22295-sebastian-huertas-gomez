import json
import re
import subprocess
from collections import Counter
from math import sqrt

Z = 1.959963984540054
A = "attack-sim/"
CATS = ["sqli", "xss", "path_traversal", "cmdi"]


def wilson(k, n):
    p = k / n
    d = 1 + Z * Z / n
    c = (p + Z * Z / (2 * n)) / d
    m = Z * sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / d
    return [round(max(0.0, c - m) * 100, 1), round(min(1.0, c + m) * 100, 1)]


def sha(blob):
    import hashlib
    return hashlib.sha256(blob).hexdigest()


def git_show(rev_path):
    return subprocess.check_output(["git", "show", rev_path])


R4 = "af61eba"
res = {}
for name, path in (("config1", "results_config1.json"), ("config2", "results_config2.json"), ("config3a", "results_config3a.json"), ("config3b", "results_config3b.json")):
    blob = git_show(f"{R4}:{A}{path}")
    res[name] = {r["id"]: r for r in json.loads(blob)}
    res[name]["_sha256"] = sha(blob)
    res[name]["_n"] = len(res[name]) - 1
corpus_blob = git_show(f"{R4}:{A}large_corpus_requests.json")
corpus = {r["id"]: r for r in json.loads(corpus_blob)}
ids = [i for i in res["config3a"] if not i.startswith("_")]
assert len(ids) == 590 and [i for i in res["config3b"] if not i.startswith("_")] == ids
cat = {i: res["config3a"][i]["category"] for i in ids}
leak = json.load(open(A + "leakage_report_round4_20261025.json"))["por_payload"]
blk = lambda c: {i for i in ids if res[c][i].get("blocked")}
B1, B2, B3a, B3b = blk("config1"), blk("config2"), blk("config3a"), blk("config3b")
M3a = set(ids) - B3a
app_layer = {i for i in B3b if res["config3b"][i].get("layer_guess") == "app"}
out = {
    "A1": {
        "commit_ronda4": R4,
        "archivos": {c: {"sha256": res[c]["_sha256"], "n": res[c]["_n"]} for c in res},
        "campos_del_resultado": sorted(next(iter(r for k, r in res["config3b"].items() if not k.startswith("_"))).keys()),
        "totales": {"config1": len(B1), "config2": len(B2), "config3a": len(B3a), "config3b": len(B3b)},
        "ejecutor_en_af61eba_sha256": sha(git_show(f"{R4}:{A}run_large_corpus.py")),
        "ejecutor_anterior_extraido_sha256": sha(open(A + "run_large_corpus_pre_fix_20261025.py", "rb").read()),
        "corpus_ronda4_sha256": sha(corpus_blob),
    },
    "A2": {
        "los_40_que_3a_no_bloquea": {"n": len(M3a), "por_categoria": dict(Counter(cat[i] for i in M3a))},
        "de_los_40_la_3b_bloquea": {"n": len(M3a & B3b), "por_categoria": dict(Counter(cat[i] for i in M3a & B3b))},
        "de_los_40_la_3b_bloquea_con_firma_de_capa_app": {"n": len(M3a & app_layer), "por_categoria": dict(Counter(cat[i] for i in M3a & app_layer))},
        "de_los_40_la_config2_bloquea": {"n": len(M3a & B2), "por_categoria": dict(Counter(cat[i] for i in M3a & B2))},
        "pasan_ambas_capas_3a_y_3b": sorted(M3a - B3b),
        "cmdi_en_los_40": sum(1 for i in M3a if cat[i] == "cmdi"),
        "cmdi_en_los_37": sum(1 for i in M3a & app_layer if cat[i] == "cmdi"),
    },
    "A3": {
        "corpus_por_categoria": {},
        "metodo": "training/leakage_check.py (repositorio logSguarDian, solo lectura) contra train, val y test; igualdad normalizada del campo completo y subcadena normalizada/literal; script attack-sim/leakage_check_round4_20261025.py",
        "en_los_40": {},
        "en_los_37": {},
    },
    "A4": {},
}
rep = json.load(open(A + "leakage_report_round4_20261025.json"))
for c in CATS:
    u = rep["por_categoria"][c]["union_particiones"]
    out["A3"]["corpus_por_categoria"][c] = {"n": rep["por_categoria"][c]["n"], **u}
for label, S in (("en_los_40", M3a), ("en_los_37", M3a & app_layer)):
    for c in CATS:
        sub = [i for i in S if cat[i] == c]
        out["A3"][label][c] = {"n": len(sub),
                               "igualdad_normalizada": sorted(i for i in sub if leak[i]["igualdad_normalizada_campo_completo"]),
                               "subcadena_normalizada": sorted(i for i in sub if leak[i]["subcadena_normalizada"]),
                               "subcadena_exacta": sorted(i for i in sub if leak[i]["subcadena_exacta"])}
pct = re.compile(r"%[0-9a-fA-F]{2}")
pre = lambda i: cat[i] in ("path_traversal", "cmdi") and bool(pct.search(corpus[i]["payload"]))
out["A4"] = {
    "diferencia_entre_ejecutores": "solo cambia la construccion de la peticion cuando la categoria es path_traversal o cmdi y el payload contiene al menos un %XX; en cualquier otro caso las peticiones son identicas byte a byte",
    "payloads_afectados_en_el_corpus": {c: sum(1 for i in ids if cat[i] == c and pre(i)) for c in CATS},
    "payloads_afectados_entre_los_40": sorted(i for i in M3a if pre(i)),
    "payloads_afectados_entre_los_37": sorted(i for i in M3a & app_layer if pre(i)),
    "payloads_afectados_entre_los_3_que_pasan_ambas_capas": sorted(i for i in M3a - B3b if pre(i)),
}
r5 = {}
for c in ("2", "3a", "3b"):
    r5[c] = {r["id"]: r for r in json.load(open(f"{A}results_combined_config{c}_run1_20261025.json"))["results"]}
ids5 = list(r5["3a"])
W5 = {i for i in ids5 if not r5["3a"][i]["blocked"]}
B3b5 = {i for i in ids5 if r5["3b"][i]["blocked"]}
B2h5 = {i for i in ids5 if json.load(open(A + "results_s1_config2_con_cabeceras_run1_20261025.json")) and False}
con = {r["id"]: r for r in json.load(open(A + "results_s1_config2_con_cabeceras_run1_20261025.json"))["results"]}
out["A5"] = {
    "ronda5_los_que_el_waf_no_bloquea": len(W5),
    "ronda5_de_esos_la_3b_bloquea": len(W5 & B3b5),
    "ronda5_3b_menos_3a": len(B3b5 - {i for i in ids5 if r5["3a"][i]["blocked"]}),
    "wilson_37_de_40": [37, 40, wilson(37, 40)],
    "wilson_48_de_51": [48, 51, wilson(48, 51)],
    "wilson_3_de_800": [3, 800, wilson(3, 800)],
    "wilson_48_de_800": [48, 800, wilson(48, 800)],
    "wilson_51_de_800": [51, 800, wilson(51, 800)],
    "ronda4_los_40_porcentaje": round(100 * 37 / 40, 1),
    "ids_ronda5_de_los_51_que_la_3b_no_bloquea": sorted(W5 - B3b5),
    "config2_con_cabeceras_bloquea_de_los_51": len(W5 & {i for i in con if con[i]["blocked"]}),
}
json.dump(out, open("docs/evidence/r5-verificacion-ronda4-20261025.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
