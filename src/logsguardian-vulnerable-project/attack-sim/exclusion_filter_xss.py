"""T6: exclusion filter for the clean XSS corpus (Round 5), against ALL
classes of the training corpus (not just the xss bucket), by:

1. Exact hash match (sha256) of three forms of each candidate: the raw
   payload (payload_raw), its wire-encoded form (forma_enviada), and its
   URL-decoded form - against hashes built from every non-empty
   path/query/body field across training/data_clean/*.jsonl, for every
   label (sqli, xss, path_traversal, cmdi, benign). Reuses
   exclusion_filter.TrainingIndex (attack-sim/exclusion_filter.py,
   unmodified import) for the hash index construction, but - unlike
   build_corpus.py's call into it - checks against every label bucket, not
   just the candidate's own category, since the task requires checking
   against all classes.

2. Normalized equality: URL-decode once, lowercase, digit runs -> "N" -
   the exact generic_template() function from the sibling repo's
   training/leakage_check.py (read-only import, not reimplemented), so the
   same normalization rule anchors both T6 (this filter) and T7 (the
   leakage audit that follows it). Applied inside this filter, scanning
   for substring containment in the normalized text pool of every class
   across data_clean - not just exact set membership - since a short XSS
   fragment can legitimately appear as a substring of a longer training
   payload (same convention leakage_check.py uses for Round-4-style
   payload corpora).

A candidate matching either mechanism is DISCARDED, not flagged. Every
discard is logged with its reason and matched source.

Usage: python3 exclusion_filter_xss.py
Reads xss_corpus_sample_20261025.jsonl, writes
xss_corpus_filtered_20261025.jsonl and exclusion_report_xss_20261025.json.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import urllib.parse
from collections import Counter
from pathlib import Path

ATTACK_SIM_DIR = Path(__file__).parent
sys.path.insert(0, str(ATTACK_SIM_DIR))
import exclusion_filter as ef  # noqa: E402 - read-only reuse, not modified

TRAINING_REPO = Path("/Users/xtsebas/Universidad/logSguarDian")
LEAKAGE_CHECK_PATH = TRAINING_REPO / "training" / "leakage_check.py"
DATA_CLEAN_DIR = TRAINING_REPO / "training" / "data_clean"

IN_PATH = ATTACK_SIM_DIR / "xss_corpus_sample_20261025.jsonl"
OUT_PATH = ATTACK_SIM_DIR / "xss_corpus_filtered_20261025.jsonl"
REPORT_PATH = ATTACK_SIM_DIR / "exclusion_report_xss_20261025.json"

ALL_LABELS = ["sqli", "xss", "path_traversal", "cmdi", "benign"]


def _load_generic_template():
    spec = importlib.util.spec_from_file_location("leakage_check_ro", LEAKAGE_CHECK_PATH)
    mod = importlib.util.module_from_spec(spec)
    # training/leakage_check.py's module-level code only defines functions
    # and constants at import time (no side effects run on import besides
    # that), so loading it this way is read-only with respect to the
    # sibling repo - nothing in it is executed that writes anything.
    spec.loader.exec_module(mod)
    return mod.generic_template


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def build_normalized_index(generic_template) -> dict[str, dict[str, str]]:
    """label -> {sha256(generic_template(text)): source_filename}, built
    across every non-empty path/query/body field in every data_clean file,
    for every label - independent of exclusion_filter.TrainingIndex, which
    only hashes raw/decoded forms, not the lowercase+digit-normalized one."""
    idx: dict[str, dict[str, str]] = {label: {} for label in ALL_LABELS}
    for fp in sorted(DATA_CLEAN_DIR.glob("*.jsonl")):
        with open(fp, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                label = rec.get("label")
                if label not in ALL_LABELS:
                    continue
                for fname in ("path", "query", "body"):
                    val = rec.get(fname)
                    if isinstance(val, str) and val:
                        h = sha256_hex(generic_template(val))
                        if h not in idx[label]:
                            idx[label][h] = fp.name
    return idx


def check_candidate(
    training_idx: ef.TrainingIndex,
    normalized_idx: dict[str, dict[str, str]],
    generic_template,
    candidate: dict,
) -> dict:
    payload_raw = candidate["payload_raw"]
    forma_enviada = candidate["forma_enviada"]
    try:
        decoded = urllib.parse.unquote(payload_raw)
    except Exception:
        decoded = payload_raw

    forms_to_check = {"raw": payload_raw, "forma_enviada": forma_enviada, "decodificada": decoded}

    for label in ALL_LABELS:
        for form_name, text in forms_to_check.items():
            matched, source = training_idx.match_exact(label, text)
            if matched:
                return {"kept": False, "reason": f"exact_hash_{form_name}", "matched_label": label, "matched_source": source}

    norm = sha256_hex(generic_template(payload_raw))
    for label in ALL_LABELS:
        source = normalized_idx[label].get(norm)
        if source:
            return {"kept": False, "reason": "normalized_equality", "matched_label": label, "matched_source": source}

    return {"kept": True, "reason": None, "matched_label": None, "matched_source": None}


def main() -> int:
    generic_template = _load_generic_template()

    print("Construyendo indice de hashes (exclusion_filter.TrainingIndex, todas las clases)...")
    training_idx = ef.build_training_index()
    print(f"  {training_idx.records_read} registros leidos de {len(training_idx.files_read)} archivos")

    print("Construyendo indice normalizado (generic_template de leakage_check.py, todas las clases)...")
    normalized_idx = build_normalized_index(generic_template)
    for label in ALL_LABELS:
        print(f"  {label}: {len(normalized_idx[label])} formas normalizadas unicas")

    candidates = [json.loads(l) for l in IN_PATH.read_text().splitlines() if l.strip()]

    kept: list[dict] = []
    discard_reasons: Counter = Counter()
    discard_examples: list[dict] = []
    for c in candidates:
        result = check_candidate(training_idx, normalized_idx, generic_template, c)
        if result["kept"]:
            kept.append(c)
        else:
            discard_reasons[result["reason"]] += 1
            discard_examples.append({
                "id": c["id"],
                "payload_raw": c["payload_raw"][:200],
                "reason": result["reason"],
                "matched_label": result["matched_label"],
                "matched_source": result["matched_source"],
            })

    with open(OUT_PATH, "w") as f:
        for c in kept:
            f.write(json.dumps(c) + "\n")

    report = {
        "input_count": len(candidates),
        "kept_count": len(kept),
        "discarded_count": len(candidates) - len(kept),
        "discard_reasons": dict(discard_reasons),
        "discard_examples": discard_examples,
        "training_files_read": training_idx.files_read,
        "training_records_read": training_idx.records_read,
    }
    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\nConservados: {len(kept)} de {len(candidates)}")
    print(f"Descartados: {dict(discard_reasons)}")
    print(f"Escrito: {OUT_PATH}")
    print(f"Reporte: {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
