"""T7: audits the final XSS corpus (post-T6 exclusion filter) against the
formal train/val/test splits, reusing training/leakage_check.py's own
loading and matching functions (read-only import from the sibling repo -
load_splits, load_unified_by_hash, build_class_text_pool, generic_template,
template_shape), not a reimplementation.

Two checks per split, both against the xss-labeled text pool only (this
corpus is entirely xss):

  - exact substring: is payload_raw a byte-identical substring of any
    xss-labeled path/query/body field in that split.
  - normalized substring: is generic_template(payload_raw) a substring of
    the same pool after generic_template() is applied to it too (URL-decode
    once, lowercase, digit runs -> N) - same rule T6 already used, applied
    here against the train/val/test partitions specifically rather than the
    full data_clean pool T6 checked.

Any normalized-equality hit here is, per the task, a failure of the T6
filter and is reported as such, not silently accepted.

Usage: python3 leakage_check_xss.py
Reads xss_corpus_filtered_20261025.jsonl, writes
leakage_report_xss_20261025.json.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ATTACK_SIM_DIR = Path(__file__).parent
TRAINING_REPO = Path("/Users/xtsebas/Universidad/logSguarDian")
LEAKAGE_CHECK_PATH = TRAINING_REPO / "training" / "leakage_check.py"

IN_PATH = ATTACK_SIM_DIR / "xss_corpus_filtered_20261025.jsonl"
REPORT_PATH = ATTACK_SIM_DIR / "leakage_report_xss_20261025.json"


def _load_leakage_check():
    spec = importlib.util.spec_from_file_location("leakage_check_ro", LEAKAGE_CHECK_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    lc = _load_leakage_check()

    print("Cargando splits train/val/test (sibling repo, solo lectura)...")
    splits = lc.load_splits()
    print("Cargando unified.jsonl por _row_hash (solo lectura)...")
    unified_by_hash = lc.load_unified_by_hash()

    candidates = [json.loads(l) for l in IN_PATH.read_text().splitlines() if l.strip()]
    print(f"Corpus a auditar: {len(candidates)} payloads xss")

    report: dict = {"n_corpus": len(candidates), "by_split": {}}
    any_normalized_hit = False

    for split_name, split_df in splits.items():
        raw_pool, tmpl_pool, missing = lc.build_class_text_pool(split_df, "xss", unified_by_hash)
        exact_hits = []
        normalized_hits = []
        for c in candidates:
            payload_raw = c["payload_raw"]
            if payload_raw and payload_raw in raw_pool:
                exact_hits.append(c["id"])
            tpl = lc.generic_template(payload_raw)
            if tpl and tpl in tmpl_pool:
                normalized_hits.append(c["id"])

        if normalized_hits:
            any_normalized_hit = True

        report["by_split"][split_name] = {
            "n_xss_rows_in_split": int((split_df["label"] == "xss").sum()),
            "missing_unified_lookups": missing,
            "exact_substring_hits": len(exact_hits),
            "exact_substring_hit_ids": exact_hits,
            "normalized_substring_hits": len(normalized_hits),
            "normalized_substring_hit_ids": normalized_hits,
        }
        print(f"  {split_name}: exact={len(exact_hits)} normalized={len(normalized_hits)}")

    report["t6_filter_failure"] = any_normalized_hit
    if any_normalized_hit:
        report["t6_filter_failure_note"] = (
            "Quedo al menos una coincidencia por igualdad normalizada contra "
            "train/val/test tras el filtro de T6 - es un fallo del filtro, "
            "reportado aqui sin ocultarlo, no corregido en esta tarea."
        )

    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nEscrito: {REPORT_PATH}")
    print(f"Fallo del filtro T6 (coincidencia normalizada tras el filtro): {any_normalized_hit}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
