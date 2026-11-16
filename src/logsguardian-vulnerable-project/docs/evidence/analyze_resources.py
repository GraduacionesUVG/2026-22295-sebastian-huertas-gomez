#!/usr/bin/env python3
"""Summarize docker stats memory and CPU samples per latency benchmark condition.

Standard library only. The evidence archive is read in memory and never extracted.
Memory is reported in MB, where MB means MiB (binary), as docker stats prints it.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import re
import statistics
import tarfile
from dataclasses import dataclass
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_ARCHIVE = SCRIPT_DIR / "latency-linux-2026-09-26.tgz"
DEFAULT_JSON_OUTPUT = SCRIPT_DIR / "resources_summary.json"
DEFAULT_MARKDOWN_OUTPUT = SCRIPT_DIR / "resources_summary.md"

WARMUP_MS = 15_000
CPU_DIFFERENCE_FLAG_PP = 5.0
WINDOW_A = "A"
WINDOW_B = "B"
WINDOWS = (WINDOW_A, WINDOW_B)
BASELINE = "baseline"
ACTIVE = "active"
CONDITIONS = (BASELINE, ACTIVE)
CSV_FILE_NAME = "memory-cpu.csv"
REPORT_PATTERN = re.compile(r"(?P<scenario>[a-z]+)-(?P<condition>baseline|active)-rep(?P<rep>\d+)\.json")
MEMORY_USAGE_PATTERN = re.compile(r"^\s*([\d.]+)\s*([A-Za-z]+)\s*/")
UNIT_IN_BYTES = {
    "B": 1,
    "kB": 1000,
    "KiB": 1024,
    "MB": 1000**2,
    "MiB": 1024**2,
    "GB": 1000**3,
    "GiB": 1024**3,
}
BYTES_PER_MB = 1024**2
REASON_WARMUP = "warmup"
REASON_OUTSIDE_RUN = "outside_run"
SEGMENTATION_RULE = (
    "A sample belongs to repetition R when firstMetricAt <= timestamp <= lastMetricAt of R's "
    "Artillery report (epoch ms). Window A also drops samples with timestamp < firstMetricAt + 15 s "
    "(warmup). Window B keeps the whole repetition. Samples outside every repetition are out of window."
)


@dataclass(frozen=True)
class Sample:
    timestamp_ms: int
    mem_mb: float
    cpu_pct: float


@dataclass(frozen=True)
class Repetition:
    scenario: str
    condition: str
    number: int
    first_ms: int
    last_ms: int

    @property
    def key(self) -> str:
        return f"{self.scenario}-{self.condition}-rep{self.number}"


def read_archive(archive: Path) -> tuple[str, dict[str, bytes]]:
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    members: dict[str, bytes] = {}
    with tarfile.open(archive, "r:gz") as tar:
        for member in tar.getmembers():
            if member.isfile():
                members[member.name] = tar.extractfile(member).read()
    return digest, members


def parse_iso_ms(value: str) -> int:
    timestamp = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    return int(timestamp.timestamp() * 1000)


def parse_memory_mb(raw: str) -> float:
    match = MEMORY_USAGE_PATTERN.match(raw)
    if not match:
        raise ValueError(f"Unparseable docker memory value: {raw!r}")
    value, unit = match.groups()
    return float(value) * UNIT_IN_BYTES[unit] / BYTES_PER_MB


def load_samples(csv_bytes: bytes) -> list[Sample]:
    reader = csv.DictReader(io.StringIO(csv_bytes.decode("utf-8")))
    return [
        Sample(
            timestamp_ms=parse_iso_ms(row["timestamp_iso"]),
            mem_mb=parse_memory_mb(row["mem_usage_raw"]),
            cpu_pct=float(row["cpu_perc_raw"].rstrip("%")),
        )
        for row in reader
    ]


def load_repetitions(members: dict[str, bytes]) -> list[Repetition]:
    repetitions = []
    for name, content in members.items():
        match = REPORT_PATTERN.fullmatch(Path(name).name)
        if not match:
            continue
        aggregate = json.loads(content)["aggregate"]
        repetitions.append(
            Repetition(
                scenario=match["scenario"],
                condition=match["condition"],
                number=int(match["rep"]),
                first_ms=aggregate["firstMetricAt"],
                last_ms=aggregate["lastMetricAt"],
            )
        )
    repetitions.sort(key=lambda rep: rep.first_ms)
    check_no_overlap(repetitions)
    return repetitions


def check_no_overlap(repetitions: list[Repetition]) -> None:
    for previous, current in zip(repetitions, repetitions[1:]):
        if current.first_ms <= previous.last_ms:
            raise ValueError(f"Repetitions overlap: {previous.key} and {current.key}")


def window_start_ms(repetition: Repetition, window: str) -> int:
    if window == WINDOW_A:
        return repetition.first_ms + WARMUP_MS
    return repetition.first_ms


def in_window(sample: Sample, repetition: Repetition, window: str) -> bool:
    return window_start_ms(repetition, window) <= sample.timestamp_ms <= repetition.last_ms


def in_full_run(sample: Sample, repetition: Repetition) -> bool:
    return repetition.first_ms <= sample.timestamp_ms <= repetition.last_ms


def samples_for_repetition(samples: list[Sample], repetition: Repetition, window: str) -> list[Sample]:
    return [sample for sample in samples if in_window(sample, repetition, window)]


def describe(values: list[float]) -> dict[str, float] | None:
    if not values:
        return None
    return {
        "mean": round(statistics.fmean(values), 3),
        "median": round(statistics.median(values), 3),
        "max": round(max(values), 3),
    }


def summarize(samples: list[Sample]) -> dict:
    return {
        "n": len(samples),
        "mem_mb": describe([sample.mem_mb for sample in samples]),
        "cpu_pct": describe([sample.cpu_pct for sample in samples]),
    }


def group_stats(samples: list[Sample], repetitions: list[Repetition]) -> list[dict]:
    rows = []
    for scenario in sorted({rep.scenario for rep in repetitions}):
        for condition in CONDITIONS:
            for window in WINDOWS:
                matching = [rep for rep in repetitions if rep.scenario == scenario and rep.condition == condition]
                window_samples = [s for rep in matching for s in samples_for_repetition(samples, rep, window)]
                rows.append(
                    {
                        "scenario": scenario,
                        "condition": condition,
                        "window": window,
                        "reps": len(matching),
                        **summarize(window_samples),
                    }
                )
    return rows


def rep_mean(samples: list[Sample]) -> tuple[float, float]:
    return (
        statistics.fmean(sample.mem_mb for sample in samples),
        statistics.fmean(sample.cpu_pct for sample in samples),
    )


def paired_increments(samples: list[Sample], repetitions: list[Repetition], scenario: str, window: str) -> dict:
    pairs = []
    for number in sorted({rep.number for rep in repetitions if rep.scenario == scenario}):
        base = find_repetition(repetitions, scenario, BASELINE, number)
        active = find_repetition(repetitions, scenario, ACTIVE, number)
        if base is None or active is None:
            continue
        base_samples = samples_for_repetition(samples, base, window)
        active_samples = samples_for_repetition(samples, active, window)
        if not base_samples or not active_samples:
            continue
        base_mem, base_cpu = rep_mean(base_samples)
        active_mem, active_cpu = rep_mean(active_samples)
        pairs.append(
            {
                "rep": number,
                "baseline_mem_mb": round(base_mem, 3),
                "active_mem_mb": round(active_mem, 3),
                "baseline_cpu_pct": round(base_cpu, 3),
                "active_cpu_pct": round(active_cpu, 3),
            }
        )
    return {"scenario": scenario, "window": window, "pairs": pairs, "summary": summarize_pairs(pairs)}


def find_repetition(repetitions: list[Repetition], scenario: str, condition: str, number: int) -> Repetition | None:
    for repetition in repetitions:
        if (repetition.scenario, repetition.condition, repetition.number) == (scenario, condition, number):
            return repetition
    return None


def summarize_pairs(pairs: list[dict]) -> dict | None:
    if not pairs:
        return None
    base_mem = statistics.fmean(p["baseline_mem_mb"] for p in pairs)
    base_cpu = statistics.fmean(p["baseline_cpu_pct"] for p in pairs)
    mem_delta = statistics.fmean(p["active_mem_mb"] - p["baseline_mem_mb"] for p in pairs)
    cpu_delta = statistics.fmean(p["active_cpu_pct"] - p["baseline_cpu_pct"] for p in pairs)
    return {
        "pairs": len(pairs),
        "mem_mb_delta": round(mem_delta, 3),
        "mem_rel_pct": round(mem_delta / base_mem * 100, 2),
        "cpu_pp_delta": round(cpu_delta, 3),
        "cpu_rel_pct": round(cpu_delta / base_cpu * 100, 2),
    }


def out_of_window(samples: list[Sample], repetitions: list[Repetition], window: str) -> list[dict]:
    rows = []
    for sample in samples:
        if any(in_window(sample, rep, window) for rep in repetitions):
            continue
        owner = next((rep for rep in repetitions if in_full_run(sample, rep)), None)
        rows.append(
            {
                "timestamp_ms": sample.timestamp_ms,
                "mem_mb": round(sample.mem_mb, 3),
                "cpu_pct": round(sample.cpu_pct, 3),
                "reason": REASON_WARMUP if owner else REASON_OUTSIDE_RUN,
                "repetition": owner.key if owner else None,
            }
        )
    return rows


def find_flags(groups: list[dict], increments: list[dict]) -> list[str]:
    flags = []
    for scenario in sorted({g["scenario"] for g in groups}):
        for condition in CONDITIONS:
            a, b = (find_group(groups, scenario, condition, window) for window in WINDOWS)
            diff = abs(a["cpu_pct"]["mean"] - b["cpu_pct"]["mean"]) if a["cpu_pct"] and b["cpu_pct"] else None
            if diff is not None and diff > CPU_DIFFERENCE_FLAG_PP:
                flags.append(f"{scenario}/{condition}: mean CPU A vs B differs by {diff:.2f} pp")
    for scenario in sorted({inc["scenario"] for inc in increments}):
        a, b = (find_increment(increments, scenario, window) for window in WINDOWS)
        if not (a["summary"] and b["summary"]):
            continue
        diff = abs(a["summary"]["cpu_pp_delta"] - b["summary"]["cpu_pp_delta"])
        if diff > CPU_DIFFERENCE_FLAG_PP:
            flags.append(f"{scenario}: paired CPU increment A vs B differs by {diff:.2f} pp")
    return flags


def find_group(groups: list[dict], scenario: str, condition: str, window: str) -> dict:
    return next(g for g in groups if (g["scenario"], g["condition"], g["window"]) == (scenario, condition, window))


def find_increment(increments: list[dict], scenario: str, window: str) -> dict:
    return next(i for i in increments if (i["scenario"], i["window"]) == (scenario, window))


def analyze(archive: Path) -> dict:
    digest, members = read_archive(archive)
    csv_name = next((name for name in members if Path(name).name == CSV_FILE_NAME), None)
    if csv_name is None:
        raise FileNotFoundError(f"{CSV_FILE_NAME} not found in {archive}")
    samples = load_samples(members[csv_name])
    repetitions = load_repetitions(members)
    groups = group_stats(samples, repetitions)
    increments = [
        paired_increments(samples, repetitions, scenario, window)
        for scenario in sorted({rep.scenario for rep in repetitions})
        for window in WINDOWS
    ]
    return {
        "archive": {"path": archive.name, "sha256": digest},
        "segmentation_rule": SEGMENTATION_RULE,
        "warmup_ms": WARMUP_MS,
        "csv_samples": len(samples),
        "repetitions": len(repetitions),
        "windows": {WINDOW_A: "measured period, first 15 s of each repetition dropped", WINDOW_B: "full repetition"},
        "groups": groups,
        "increments": increments,
        "out_of_window": {window: out_of_window(samples, repetitions, window) for window in WINDOWS},
        "flags": find_flags(groups, increments),
        "cpu_flag_threshold_pp": CPU_DIFFERENCE_FLAG_PP,
    }


def format_stat(stat: dict | None) -> str:
    if stat is None:
        return "-"
    return f"{stat['mean']:.2f} / {stat['median']:.2f} / {stat['max']:.2f}"


def render_groups_table(groups: list[dict]) -> list[str]:
    lines = [
        "| Scenario | Condition | Window | Reps | n | Mem MB mean / median / max | CPU % mean / median / max |",
        "|---|---|---|---|---|---|---|",
    ]
    for g in groups:
        lines.append(
            f"| {g['scenario']} | {g['condition']} | {g['window']} | {g['reps']} | {g['n']} "
            f"| {format_stat(g['mem_mb'])} | {format_stat(g['cpu_pct'])} |"
        )
    return lines


def render_increments_table(increments: list[dict]) -> list[str]:
    lines = [
        "| Scenario | Window | Pairs | Δ mem (MB) | Δ mem (%) | Δ CPU (pp) | Δ CPU (%) |",
        "|---|---|---|---|---|---|---|",
    ]
    for inc in increments:
        s = inc["summary"]
        if s is None:
            lines.append(f"| {inc['scenario']} | {inc['window']} | 0 | - | - | - | - |")
            continue
        lines.append(
            f"| {inc['scenario']} | {inc['window']} | {s['pairs']} | {s['mem_mb_delta']:+.2f} "
            f"| {s['mem_rel_pct']:+.2f} | {s['cpu_pp_delta']:+.2f} | {s['cpu_rel_pct']:+.2f} |"
        )
    return lines


def render_out_of_window(rows_by_window: dict[str, list[dict]]) -> list[str]:
    lines = []
    for window in WINDOWS:
        rows = rows_by_window[window]
        lines.append(f"### Window {window}: {len(rows)} samples out of window")
        lines.append("")
        lines.append("| Timestamp (UTC) | Mem MB | CPU % | Reason | Repetition |")
        lines.append("|---|---|---|---|---|")
        for row in rows:
            stamp = dt.datetime.fromtimestamp(row["timestamp_ms"] / 1000, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            lines.append(
                f"| {stamp} | {row['mem_mb']:.2f} | {row['cpu_pct']:.2f} | {row['reason']} | {row['repetition'] or '-'} |"
            )
        lines.append("")
    return lines


def render_markdown(report: dict) -> list[str]:
    lines = [
        "# Resource usage summary (memory and CPU, `app` container)",
        "",
        f"Archive: `{report['archive']['path']}`",
        f"SHA-256: `{report['archive']['sha256']}`",
        f"Samples: {report['csv_samples']} | Repetitions: {report['repetitions']}",
        "",
        "## Segmentation rule",
        "",
        report["segmentation_rule"],
        "",
        "## Windows",
        "",
        f"- **A (primary):** {report['windows'][WINDOW_A]}",
        f"- **B:** {report['windows'][WINDOW_B]}",
        "",
        "## Per condition",
        "",
        *render_groups_table(report["groups"]),
        "",
        "## Paired increments (active - baseline, per repetition)",
        "",
        "Δ values are the mean of per-repetition pair differences. Relative values divide by the baseline mean.",
        "",
        *render_increments_table(report["increments"]),
        "",
        "## Flags",
        "",
        f"Threshold: CPU difference between A and B above {report['cpu_flag_threshold_pp']} pp.",
        "",
        *([f"- {flag}" for flag in report["flags"]] or ["No flags."]),
        "",
        "## Samples out of window",
        "",
        *render_out_of_window(report["out_of_window"]),
    ]
    return lines


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON_OUTPUT)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN_OUTPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = analyze(args.archive)
    args.json_output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    args.markdown_output.write_text("\n".join(render_markdown(report)) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
