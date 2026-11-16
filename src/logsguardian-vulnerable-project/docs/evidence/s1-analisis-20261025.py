import json
from collections import Counter
from math import comb, sqrt

Z = 1.959963984540054
A = "attack-sim/"


def wilson(k, n):
    p = k / n
    d = 1 + Z * Z / n
    c = (p + Z * Z / (2 * n)) / d
    m = Z * sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / d
    return [round(max(0.0, c - m) * 100, 1), round(min(1.0, c + m) * 100, 1)]


def load(p):
    return {r["id"]: r for r in json.load(open(A + p))["results"]}


r1 = load("results_combined_config2_run1_20261025.json")
sin = load("results_s1_config2_sin_cabeceras_run1_20261025.json")
con = load("results_s1_config2_con_cabeceras_run1_20261025.json")
a3 = load("results_combined_config3a_run1_20261025.json")
b3 = load("results_combined_config3b_run1_20261025.json")
ids = list(r1)
assert ids == list(sin) == list(con) == list(a3) == list(b3)
cat = {i: r1[i]["category"] for i in ids}
blk = lambda m: {i for i in ids if m[i]["blocked"]}
B2, B2s, B2h, B3a, B3b = blk(r1), blk(sin), blk(con), blk(a3), blk(b3)

out = {
    "control_sin_cabeceras_frente_a_corrida1": {
        "ids_con_veredicto_o_status_distinto": [i for i in ids if (r1[i]["blocked"], r1[i]["status"]) != (sin[i]["blocked"], sin[i]["status"])]},
    "por_categoria": {},
    "a_bloqueado": sorted(B2h - B2),
    "a_no_bloqueado": sorted(B2 - B2h),
    "status_de_los_que_cambian": {i: [r1[i]["status"], con[i]["status"]] for i in sorted(B2 ^ B2h)},
    "totales": {"sin_cabeceras": len(B2), "con_cabeceras": len(B2h), "wilson_sin": wilson(len(B2), 800), "wilson_con": wilson(len(B2h), 800),
                "config3a": len(B3a), "config3b": len(B3b)},
    "cabeceras_y_waf": {
        "union_config2_con_cabeceras_o_3a": len(B2h | B3a),
        "3b_menos_config2_con_cabeceras": sorted(B3b - B2h),
        "config2_con_cabeceras_menos_3b": sorted(B2h - B3b),
        "de_los_13_que_la_3b_suma_a_la_config2_sin_cabeceras_los_que_la_config2_con_cabeceras_bloquea": sorted((B3b - B2) & B2h),
        "de_los_13_los_que_no": sorted((B3b - B2) - B2h),
        "de_los_51_que_la_3a_no_bloquea_la_config2_con_cabeceras_bloquea": len((set(ids) - B3a) & B2h),
    },
}
for k in ["sqli", "path_traversal", "cmdi", "xss"]:
    n = sum(1 for i in ids if cat[i] == k)
    k0 = sum(1 for i in B2 if cat[i] == k)
    k1 = sum(1 for i in B2h if cat[i] == k)
    up = sum(1 for i in B2h - B2 if cat[i] == k)
    down = sum(1 for i in B2 - B2h if cat[i] == k)
    out["por_categoria"][k] = {"n": n, "sin": [k0, wilson(k0, n)], "con": [k1, wilson(k1, n)], "pasan_a_bloqueado": up, "pasan_a_no_bloqueado": down, "diferencia": k1 - k0}
b, c = len(B2h - B2), len(B2 - B2h)
nn = b + c
p = min(1.0, 2 * sum(comb(nn, x) for x in range(0, min(b, c) + 1)) / 2 ** nn)
out["mcnemar_exacto_bilateral"] = {"discordantes": [b, c], "p": p}
json.dump(out, open("docs/evidence/s1-analisis-20261025.json", "w"), indent=1)
print(json.dumps(out, indent=1))
