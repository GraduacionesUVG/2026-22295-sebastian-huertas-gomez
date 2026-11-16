import importlib.util
import json
from pathlib import Path

ATTACK_SIM_DIR = Path(__file__).parent
TRAINING_REPO = Path("/Users/xtsebas/Universidad/logSguarDian")
LC_PATH = TRAINING_REPO / "training" / "leakage_check.py"
IN_PATH = ATTACK_SIM_DIR / "large_corpus_requests.json.leaked.bak"
OUT_PATH = ATTACK_SIM_DIR / "leakage_report_round4_20261025.json"
CLASSES = ["sqli", "path_traversal", "cmdi", "xss"]


def load_lc():
    spec = importlib.util.spec_from_file_location("leakage_check_ro", LC_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def field_sets(lc, split_df, label, unified_by_hash):
    tmpl_fn = lc.template_fn_for(label)
    sub = split_df[split_df["label"] == label]
    raw_fields = set()
    tmpl_fields = set()
    for rh in sub["_row_hash"]:
        rec = unified_by_hash.get(rh)
        if rec is None:
            continue
        for field in ("path", "query", "body"):
            val = rec.get(field)
            if not val:
                continue
            raw_fields.add(val)
            tmpl_fields.add(tmpl_fn(val))
    return raw_fields, tmpl_fields


def main():
    lc = load_lc()
    splits = lc.load_splits()
    unified = lc.load_unified_by_hash()
    corpus = json.loads(IN_PATH.read_text())
    report = {"corpus": IN_PATH.name, "por_categoria": {}, "por_payload": {}}
    for label in CLASSES:
        items = [c for c in corpus if c["category"] == label]
        tmpl_fn = lc.template_fn_for(label)
        entry = {"n": len(items), "regla_normalizacion": "template_shape" if label == "cmdi" else "generic_template", "por_particion": {}}
        union_exact, union_sub, union_eq = set(), set(), set()
        for split_name, split_df in splits.items():
            raw_pool, tmpl_pool, missing = lc.build_class_text_pool(split_df, label, unified)
            raw_fields, tmpl_fields = field_sets(lc, split_df, label, unified)
            exact_ids, sub_ids, eq_ids = [], [], []
            for c in items:
                p = c["payload"]
                if p and p in raw_pool:
                    exact_ids.append(c["id"])
                t = tmpl_fn(p)
                if t and t in tmpl_pool:
                    sub_ids.append(c["id"])
                if t and t in tmpl_fields:
                    eq_ids.append(c["id"])
            union_exact |= set(exact_ids)
            union_sub |= set(sub_ids)
            union_eq |= set(eq_ids)
            entry["por_particion"][split_name] = {
                "filas_clase": int((split_df["label"] == label).sum()),
                "sin_texto_en_unified": missing,
                "subcadena_exacta": len(exact_ids),
                "subcadena_normalizada": len(sub_ids),
                "igualdad_normalizada_campo_completo": len(eq_ids),
            }
        entry["union_particiones"] = {
            "subcadena_exacta": len(union_exact),
            "subcadena_normalizada": len(union_sub),
            "igualdad_normalizada_campo_completo": len(union_eq),
        }
        report["por_categoria"][label] = entry
        for c in items:
            report["por_payload"][c["id"]] = {
                "subcadena_exacta": c["id"] in union_exact,
                "subcadena_normalizada": c["id"] in union_sub,
                "igualdad_normalizada_campo_completo": c["id"] in union_eq,
            }
    OUT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=1))
    for label in CLASSES:
        e = report["por_categoria"][label]
        print(label, e["n"], e["union_particiones"])


main()
