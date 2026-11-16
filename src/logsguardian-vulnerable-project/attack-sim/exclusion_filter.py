"""Exclusion filter: cross-checks candidate evaluation payloads against the
training corpus so that no payload (or, for cmdi, no payload built from the
same structural template) that the model has already seen during training
can enter the new evaluation corpus.

This is a lightweight, independent re-implementation written for the
evaluation-corpus rebuild (fix/clean-evaluation-corpus). It does not import
or depend on the Phase 1 dataset-construction pipeline (training/*), which
may be running concurrently in a sibling process - it only *reads* the
training corpus files as plain JSONL/text.

Two exclusion mechanisms:

1. Exact hash match: sha256 of the payload text (and, symmetrically, its
   URL-decoded/encoded counterpart) is compared against a set of hashes
   built from every non-empty `path`/`query`/`body` field across the
   training JSONL corpus (training/data_clean/*.jsonl in the sibling repo),
   bucketed by the record's `label`.

2. Template-shape match (cmdi only): normalizes the same way as
   training/parsers/parse_seclists_cmdi.py:44-50 - 6 consecutive uppercase
   letters (the random canary) -> "CANARY", runs of digits -> "N" - and
   compares against the shape set built from
   data/seclists_command-injection-commix.txt (the raw SecLists source used
   for cmdi training) plus every cmdi-labeled training payload, as a second
   safety net beyond the direct SecLists comparison.

A payload matching either mechanism is DISCARDED, not flagged.
"""
from __future__ import annotations

import hashlib
import json
import re
import urllib.parse
from dataclasses import dataclass, field
from pathlib import Path

# Sibling repo, READ-ONLY. Never written to by this script.
TRAINING_REPO = Path("/Users/xtsebas/Universidad/logSguarDian")
DATA_CLEAN_DIR = TRAINING_REPO / "training" / "data_clean"
SECLISTS_CMDI_RAW = TRAINING_REPO / "data" / "seclists_command-injection-commix.txt"

VALID_LABELS = {"sqli", "xss", "path_traversal", "cmdi", "benign"}

# Same normalization as training/parsers/parse_seclists_cmdi.py:44-50.
_CANARY_RE = re.compile(r"[A-Z]{6}")
_DIGIT_RE = re.compile(r"\d+")


def template_shape(text: str) -> str:
    shape = _CANARY_RE.sub("CANARY", text)
    shape = _DIGIT_RE.sub("N", shape)
    return shape


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def _variants(text: str) -> set[str]:
    """Both the raw string and its URL-decoded form, so an exclusion check
    matches regardless of which side (training data vs. candidate) happens
    to be percent-encoded."""
    out = {text}
    try:
        decoded = urllib.parse.unquote(text)
        if decoded != text:
            out.add(decoded)
    except Exception:
        pass
    return out


@dataclass
class TrainingIndex:
    # category -> set of sha256 hashes of payload text (raw + decoded variants)
    hashes_by_label: dict[str, set[str]] = field(default_factory=dict)
    # category -> hash -> source filename (first file seen with that hash)
    source_by_hash: dict[str, dict[str, str]] = field(default_factory=dict)
    # cmdi-specific: set of template shapes seen in training (seclists raw +
    # any cmdi-labeled training payload), and where each shape came from.
    cmdi_shapes: set[str] = field(default_factory=set)
    cmdi_shape_source: dict[str, str] = field(default_factory=dict)

    files_read: list[str] = field(default_factory=list)
    records_read: int = 0

    def add_training_string(self, label: str, text: str, source: str) -> None:
        if not text:
            return
        bucket = self.hashes_by_label.setdefault(label, set())
        src_bucket = self.source_by_hash.setdefault(label, {})
        for variant in _variants(text):
            h = sha256_hex(variant)
            if h not in bucket:
                bucket.add(h)
                src_bucket[h] = source
        if label == "cmdi":
            for variant in _variants(text):
                shape = template_shape(variant)
                if shape not in self.cmdi_shapes:
                    self.cmdi_shapes.add(shape)
                    self.cmdi_shape_source[shape] = source

    def match_exact(self, category: str, payload: str) -> tuple[bool, str | None]:
        bucket = self.hashes_by_label.get(category, set())
        src_bucket = self.source_by_hash.get(category, {})
        for variant in _variants(payload):
            h = sha256_hex(variant)
            if h in bucket:
                return True, src_bucket.get(h)
        return False, None

    def match_cmdi_template(self, payload: str) -> tuple[bool, str | None]:
        for variant in _variants(payload):
            shape = template_shape(variant)
            if shape in self.cmdi_shapes:
                return True, self.cmdi_shape_source.get(shape)
        return False, None


def build_training_index(
    data_clean_dir: Path = DATA_CLEAN_DIR,
    seclists_cmdi_raw: Path = SECLISTS_CMDI_RAW,
) -> TrainingIndex:
    idx = TrainingIndex()

    jsonl_files = sorted(data_clean_dir.glob("*.jsonl"))
    for fp in jsonl_files:
        idx.files_read.append(str(fp))
        with open(fp, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                idx.records_read += 1
                label = rec.get("label")
                if label not in VALID_LABELS:
                    continue
                for fname in ("path", "query", "body"):
                    val = rec.get(fname)
                    if isinstance(val, str) and val:
                        idx.add_training_string(label, val, fp.name)

    # Raw SecLists commix source: field-agnostic, one payload per line,
    # already percent-encoded. Same source parse_seclists_cmdi.py consumes.
    if seclists_cmdi_raw.exists():
        idx.files_read.append(str(seclists_cmdi_raw))
        with open(seclists_cmdi_raw, encoding="utf-8", errors="replace") as fh:
            for raw_line in fh:
                line = raw_line.strip()
                if not line:
                    continue
                idx.records_read += 1
                idx.add_training_string("cmdi", line, seclists_cmdi_raw.name)

    return idx


@dataclass
class ExclusionResult:
    kept: bool
    reason: str | None = None  # "exact_hash" | "cmdi_template" | None
    matched_source: str | None = None


def check_candidate(idx: TrainingIndex, category: str, payload: str) -> ExclusionResult:
    matched, source = idx.match_exact(category, payload)
    if matched:
        return ExclusionResult(kept=False, reason="exact_hash", matched_source=source)

    if category == "cmdi":
        matched, source = idx.match_cmdi_template(payload)
        if matched:
            return ExclusionResult(kept=False, reason="cmdi_template", matched_source=source)

    return ExclusionResult(kept=True)
