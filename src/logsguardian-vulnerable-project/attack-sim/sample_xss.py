"""T5: stratified sampling of the 400 XSS candidates down to a 200-payload
final corpus, with fixed rules decided before looking at any result:

- No value of any dimension (contexto, vector, funcion, codificacion,
  transporte, campo) exceeds 30% of the final corpus (60 of 200).
- At least 20 payloads per accepted transport (urlencoded, multipart,
  json - all three accepted per T3's empirical check).
- At least 30% of the final corpus has no literal "alert" substring in
  payload_raw (case-insensitive).

Deterministic: candidates are shuffled with the same seed as the
generator, then accepted greedily in that fixed order, skipping any
candidate that would push one of its dimension values over the 30% cap.
This is the whole sampling procedure - no manual curation, no discarding
on a case-by-case basis after the fact.

Usage: python3 sample_xss.py
Reads xss_candidates_20261025.jsonl, writes xss_corpus_sample_20261025.jsonl
(200 payloads, pre-exclusion-filter - see T6 for the exclusion step that
follows this one) and xss_sampling_report_20261025.json with the resulting
distribution and a pass/fail against each rule above.
"""
from __future__ import annotations

import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

SEED = 20261025
FINAL_N = 200
MAX_FRACTION_PER_VALUE = 0.30
MIN_PER_TRANSPORT = 20
MIN_NO_ALERT_FRACTION = 0.30

DIMENSIONS = ["contexto", "vector", "funcion", "codificacion", "transporte", "campo"]

# transporte y campo tienen exactamente 3 valores posibles cada uno; con un
# corpus de 200, el minimo matematico para el valor mas frecuente de una
# dimension de 3 valores es 200/3 = 66.67 (33.3%), por encima del 30%
# declarado en T5. Es una imposibilidad aritmetica, no un defecto del
# muestreador (verificado y reportado antes de tocar el codigo). Decision
# del usuario (2026-10-25): mantener el 30% estricto en las dimensiones con
# margen real (contexto, vector, funcion, codificacion - 7 a 10 valores
# cada una) y usar el reparto mas equilibrado posible en transporte/campo,
# declarado como desviacion en protocol-xss.md y en el entregable final.
RELAXED_CAP_DIMENSIONS = {"transporte", "campo"}
RELAXED_MAX_FRACTION_PER_VALUE = 0.34  # 68 de 200 - techo del reparto mas parejo posible para 3 valores

IN_PATH = Path(__file__).parent / "xss_candidates_20261025.jsonl"
OUT_PATH = Path(__file__).parent / "xss_corpus_sample_20261025.jsonl"
REPORT_PATH = Path(__file__).parent / "xss_sampling_report_20261025.json"


def has_alert(payload_raw: str) -> bool:
    return "alert" in payload_raw.lower()


def sample(candidates: list[dict]) -> list[dict]:
    rng = random.Random(SEED)
    order = list(candidates)
    rng.shuffle(order)

    cap_by_dim = {
        d: int(FINAL_N * (RELAXED_MAX_FRACTION_PER_VALUE if d in RELAXED_CAP_DIMENSIONS else MAX_FRACTION_PER_VALUE))
        for d in DIMENSIONS
    }
    counts: dict[str, Counter] = {d: Counter() for d in DIMENSIONS}
    selected: list[dict] = []

    for cand in order:
        if len(selected) >= FINAL_N:
            break
        would_exceed = False
        for d in DIMENSIONS:
            v = cand[d]
            if counts[d][v] + 1 > cap_by_dim[d]:
                would_exceed = True
                break
        if would_exceed:
            continue
        selected.append(cand)
        for d in DIMENSIONS:
            counts[d][cand[d]] += 1

    return selected


def verify(selected: list[dict]) -> dict:
    n = len(selected)
    report: dict = {"final_n": n, "cap_per_value": int(FINAL_N * MAX_FRACTION_PER_VALUE)}

    dim_report = {}
    all_within_cap = True
    for d in DIMENSIONS:
        c = Counter(x[d] for x in selected)
        max_v, max_n = c.most_common(1)[0] if c else (None, 0)
        cap_used = int(FINAL_N * (RELAXED_MAX_FRACTION_PER_VALUE if d in RELAXED_CAP_DIMENSIONS else MAX_FRACTION_PER_VALUE))
        within = max_n <= cap_used
        all_within_cap = all_within_cap and within
        dim_report[d] = {
            "counts": dict(c), "max_value": max_v, "max_count": max_n,
            "cap_applied": cap_used,
            "relaxed_cap": d in RELAXED_CAP_DIMENSIONS,
            "within_cap": within,
        }
    report["by_dimension"] = dim_report
    report["rule_cap_ok"] = all_within_cap
    report["nota_desviacion"] = (
        "transporte y campo tienen exactamente 3 valores posibles; el 30% es "
        "matematicamente inalcanzable con 200 payloads (minimo posible 33.3%). "
        "Se uso un tope relajado de 34% (68/200) solo para estas dos "
        "dimensiones, declarado como desviacion del plan. Las otras 4 "
        "dimensiones cumplen el 30% estricto."
    )

    transporte_counts = Counter(x["transporte"] for x in selected)
    min_transporte_ok = all(transporte_counts.get(t, 0) >= MIN_PER_TRANSPORT for t in ("urlencoded", "multipart", "json"))
    report["transporte_counts"] = dict(transporte_counts)
    report["rule_min_20_por_transporte_ok"] = min_transporte_ok

    no_alert = sum(1 for x in selected if not has_alert(x["payload_raw"]))
    no_alert_fraction = no_alert / n if n else 0
    report["no_alert_count"] = no_alert
    report["no_alert_fraction"] = no_alert_fraction
    report["rule_min_30pct_sin_alert_ok"] = no_alert_fraction >= MIN_NO_ALERT_FRACTION

    report["all_rules_pass"] = (
        report["rule_cap_ok"]
        and report["rule_min_20_por_transporte_ok"]
        and report["rule_min_30pct_sin_alert_ok"]
        and n == FINAL_N
    )
    return report


def main() -> int:
    candidates = [json.loads(l) for l in IN_PATH.read_text().splitlines() if l.strip()]
    selected = sample(candidates)
    report = verify(selected)

    with open(OUT_PATH, "w") as f:
        for c in selected:
            f.write(json.dumps(c) + "\n")
    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print(f"Seleccionados: {len(selected)} de {len(candidates)} candidatos")
    print(f"Reglas cumplidas: {report['all_rules_pass']}")
    print(json.dumps(report, indent=2))

    return 0 if report["all_rules_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
