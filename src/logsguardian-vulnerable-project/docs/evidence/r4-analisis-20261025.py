import json
from collections import Counter
from math import sqrt

Z = 1.959963984540054
A = "attack-sim/"
CATS = ["sqli", "path_traversal", "cmdi", "xss"]


def wilson(k, n):
    p = k / n
    d = 1 + Z * Z / n
    c = (p + Z * Z / (2 * n)) / d
    m = Z * sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / d
    return [round(max(0.0, c - m) * 100, 1), round(min(1.0, c + m) * 100, 1)]


def load(p):
    return {r["id"]: r for r in json.load(open(A + p))["results"]}


sin = load("results_combined_config2_run1_20261025.json")
con = {f"run{i}": load(f"results_s1_config2_con_cabeceras_run{i}_20261025.json") for i in (1, 2, 3)}
a3 = load("results_combined_config3a_run1_20261025.json")
b3 = load("results_combined_config3b_run1_20261025.json")
ids = list(sin)
for m in list(con.values()) + [a3, b3]:
    assert list(m) == ids
cat = {i: sin[i]["category"] for i in ids}
blk = lambda m: {i for i in ids if m[i]["blocked"]}
B2s, B3a, B3b = blk(sin), blk(a3), blk(b3)
B2h = {r: blk(m) for r, m in con.items()}
W = set(ids) - B3a
bycat = lambda s: dict(Counter(cat[i] for i in s))
out = {"A1": {}, "A2": {}}

out["A1"]["por_corrida"] = {}
for r, m in con.items():
    out["A1"]["por_corrida"][r] = {c: [sum(1 for i in B2h[r] if cat[i] == c), 200, wilson(sum(1 for i in B2h[r] if cat[i] == c), 200)] for c in CATS}
    out["A1"]["por_corrida"][r]["total"] = [len(B2h[r]), 800, wilson(len(B2h[r]), 800)]
    out["A1"]["por_corrida"][r]["status_distintos_frente_a_run1"] = [i for i in ids if m[i]["status"] != con["run1"][i]["status"]]
verdict_diff = [i for i in ids if len({con[r][i]["blocked"] for r in con}) > 1]
out["A1"]["ids_con_veredicto_distinto_entre_las_tres_corridas"] = verdict_diff
out["A1"]["ids_con_status_distinto_entre_las_tres_corridas"] = [i for i in ids if len({con[r][i]["status"] for r in con}) > 1]

h = B2h["run1"]
out["A2"]["a_config2_con_cabeceras_run1"] = {"total": len(h), **{c: sum(1 for i in h if cat[i] == c) for c in CATS}}
out["A2"]["b_descomposicion"] = {
    "3b_menos_config2_sin_cabeceras": len(B3b) - len(B2s),
    "efecto_cabeceras_neto_sobre_la_libreria": len(h) - len(B2s),
    "aporte_waf_condiciones_equiparadas_3b_menos_config2_con_cabeceras": len(B3b) - len(h),
    "ids_aporte_waf": sorted(B3b - h),
    "categorias_aporte_waf": bycat(B3b - h),
    "los_3_los_bloquea_la_3a": sorted((B3b - h) & B3a),
    "los_3_no_los_bloquea_la_config2_con_cabeceras": sorted((B3b - h) - h),
    "config2_con_cabeceras_menos_3b": sorted(h - B3b),
    "suma_comprobada": (len(h) - len(B2s)) + (len(B3b) - len(h)) == len(B3b) - len(B2s) == 13,
}
up, down = sorted(h - B2s), sorted(B2s - h)
out["A2"]["c_cambios_por_cabeceras"] = {
    "a_bloqueado": up, "a_no_bloqueado": down, "brutos_a_bloqueado": len(up), "brutos_a_no_bloqueado": len(down), "neto": len(up) - len(down),
    "entre_los_51_que_el_waf_no_bloquea": {"a_bloqueado": [i for i in up if i in W], "a_no_bloqueado": [i for i in down if i in W],
                                           "neto": len([i for i in up if i in W]) - len([i for i in down if i in W]),
                                           "categorias": bycat([i for i in up if i in W])},
    "entre_los_que_el_waf_si_bloquea": {"a_bloqueado": [i for i in up if i not in W], "a_no_bloqueado": [i for i in down if i not in W],
                                        "neto": len([i for i in up if i not in W]) - len([i for i in down if i not in W]),
                                        "categorias_a_bloqueado": bycat([i for i in up if i not in W]),
                                        "categorias_a_no_bloqueado": bycat([i for i in down if i not in W])},
}
d = {}
for r in con:
    disc = [i for i in sorted(W) if (i in B2h[r]) != (i in B3b)]
    d[r] = {"n": len(W), "config2_con_cabeceras_bloquea": len(W & B2h[r]), "3b_bloquea": len(W & B3b), "ids_con_veredicto_distinto": disc,
            "coinciden": len(W) - len(disc)}
out["A2"]["d_cruce_51_waf_no_bloquea"] = d
out["A2"]["d_cruce_todos_los_800"] = {r: {"ids_distintos_frente_a_3b": sorted(B2h[r] ^ B3b)} for r in con}
json.dump(out, open("docs/evidence/r4-analisis-20261025.json", "w"), indent=1)
print(json.dumps(out, indent=1))
