#!/usr/bin/env bash
# Samples `docker stats` for the `app` service (memory usage + CPU%) at a
# fixed interval and appends one CSV row per sample, until it receives
# SIGTERM/SIGINT (or COLLECT_SECONDS elapses, if set - mainly for local
# smoke-testing so it doesn't have to be babysat).
#
# Neither memory-under-sustained-load nor CPU sampling existed anywhere in
# this project before this script - there was no way to check for a leak
# (monotonic RSS growth) or characterize CPU cost under real load, only the
# isolated microbenchmark in the sibling repo
# (benchmarks/onnx-memory-pool.bench.js, 245.11MB, NOT a sustained-load
# number and not reproduced here - see this script's companion
# attack-sim/analyze-memory.js and the workflow file for how that relates).
#
# Intended usage: started in the background right before
# attack-sim/run_latency_suite.sh, stopped right after. The suite's full run
# (5 reps x 2 conditions x 3 scenarios, each with a warmup + measured phase)
# takes ~37-38 minutes at its default settings - sampling across that whole
# window is how this harness satisfies the protocol's ">=30min sustained
# load" requirement for the memory check, without running a separate
# dedicated stress phase. See .github/workflows/latency-benchmark.yml.
#
# Usage:
#   attack-sim/monitor-memory.sh <output-csv> [interval-seconds] [compose-args...]
# Defaults: interval-seconds=5, compose-args="-f docker-compose.yml -f docker-compose.direct.yml"
#
# Env:
#   COLLECT_SECONDS   if set, stop automatically after this many seconds
#                      instead of waiting for a signal (local smoke-testing).
#
# Output CSV columns: timestamp_iso,mem_usage_raw,cpu_perc_raw
#   mem_usage_raw is docker's own "<used> / <limit>" string (e.g.
#   "123.4MiB / 1.952GiB") and cpu_perc_raw is e.g. "12.34%" - deliberately
#   left as docker's raw strings here; unit normalization and the
#   leak/trend analysis both live in analyze-memory.js, not duplicated here.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

OUTPUT_CSV="${1:?usage: monitor-memory.sh <output-csv> [interval-seconds] [compose-args...]}"
shift
INTERVAL_S="${1:-5}"
if [[ "$INTERVAL_S" =~ ^-?[0-9]+$ ]]; then
  shift
else
  INTERVAL_S=5
fi

COMPOSE_ARGS=("$@")
if [ "${#COMPOSE_ARGS[@]}" -eq 0 ]; then
  COMPOSE_ARGS=(-f docker-compose.yml -f docker-compose.direct.yml)
fi

STOP=0
on_stop() { STOP=1; }
trap on_stop TERM INT

echo "timestamp_iso,mem_usage_raw,cpu_perc_raw" >"$OUTPUT_CSV"

start_ts=$(date +%s)
sample_count=0
while [ "$STOP" -eq 0 ]; do
  container_id="$(docker compose "${COMPOSE_ARGS[@]}" ps -q app || true)"
  if [ -n "$container_id" ]; then
    line="$(docker stats --no-stream --format '{{.MemUsage}}|{{.CPUPerc}}' "$container_id" 2>/dev/null || true)"
    if [ -n "$line" ]; then
      mem_raw="${line%%|*}"
      cpu_raw="${line##*|}"
      echo "$(date -u +%Y-%m-%dT%H:%M:%SZ),${mem_raw},${cpu_raw}" >>"$OUTPUT_CSV"
      sample_count=$((sample_count + 1))
    fi
  fi

  if [ -n "${COLLECT_SECONDS:-}" ]; then
    now=$(date +%s)
    if [ $((now - start_ts)) -ge "$COLLECT_SECONDS" ]; then
      break
    fi
  fi

  sleep "$INTERVAL_S" &
  wait $! || true
done

echo "[monitor-memory] stopped after ${sample_count} samples, written to ${OUTPUT_CSV}" >&2
