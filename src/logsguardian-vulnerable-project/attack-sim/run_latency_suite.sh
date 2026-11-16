#!/usr/bin/env bash
# Runs the full latency benchmark suite: 3 scenarios (normal, attack,
# volume) x 2 conditions (baseline = LOGSGUARDIAN_DISABLED=true, active =
# LOGSGUARDIAN_DISABLED=false) x 5 repetitions each, drops the max and min
# of each 5-rep group, takes the median of the remaining 3, and reports
# Delta p95 = (active_median - baseline_median) / baseline_median * 100 per
# scenario. This is the script the CI workflow
# (.github/workflows/latency-benchmark.yml) invokes - kept here as a
# standalone script rather than inlined in the YAML so it's runnable and
# debuggable locally without touching CI.
#
# Prerequisites: the `app` and `db` services are already up (this script
# does NOT run the initial `docker compose up` itself - the caller controls
# that, since the caller also decides which compose files/ports to use; this
# script DOES recreate the `app` service on its own, to flip
# LOGSGUARDIAN_DISABLED between baseline and active runs). `artillery`,
# `node`, `curl` and `docker compose` must be on PATH.
#
# Usage:
#   attack-sim/run_latency_suite.sh [compose-args...]
# Example (matches the CI workflow):
#   attack-sim/run_latency_suite.sh -f docker-compose.yml -f docker-compose.direct.yml
#
# Env overrides (useful for a fast mechanical smoke test - e.g.
# WARMUP_S=11 MEASURED_S=12 REPS=3 - instead of the full run, which takes
# ~37-42 minutes for real at the defaults below: 3 scenarios x 2 conditions
# x 5 reps x 75s/rep = 2250s = 37.5min of Artillery alone, plus container
# recreate overhead):
#   TARGET_URL            default http://localhost:3000
#   WARMUP_S              default 15  (warmup phase duration, seconds)
#   MEASURED_S            default 60  (measured phase duration, seconds)
#   REPS                  default 5
#   WARMUP_RATE           default 5   (arrivalRate for the warmup phase)
#   MEASURED_RATE_NORMAL  default 25  (measured-phase arrivalRate for the
#                                      normal/volume scenarios - x4 req/VU
#                                      = ~100 req/s)
#   MEASURED_RATE_ATTACK  default 30  (measured-phase arrivalRate for the
#                                      attack scenario - weighted scenarios
#                                      average ~3.4 req/VU = ~100 req/s)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

TARGET_URL="${TARGET_URL:-http://localhost:3000}"
WARMUP_S="${WARMUP_S:-15}"
MEASURED_S="${MEASURED_S:-60}"
REPS="${REPS:-5}"
WARMUP_RATE="${WARMUP_RATE:-5}"
MEASURED_RATE_NORMAL="${MEASURED_RATE_NORMAL:-25}"
MEASURED_RATE_ATTACK="${MEASURED_RATE_ATTACK:-30}"
WARMUP_MS=$((WARMUP_S * 1000))

RESULTS_DIR="$REPO_ROOT/attack-sim/results/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$RESULTS_DIR"

COMPOSE_ARGS=("$@")
if [ "${#COMPOSE_ARGS[@]}" -eq 0 ]; then
  COMPOSE_ARGS=(-f docker-compose.yml -f docker-compose.direct.yml)
fi

# Logs go to stderr on purpose - several functions below are called via
# command substitution ($(...)) to capture a single computed value on
# stdout (a median, a delta), and stderr is how their progress logging
# stays visible in real time (including in CI logs) without polluting the
# captured value.
log() { echo "[run_latency_suite] $*" >&2; }

wait_for_app() {
  local tries=0
  until curl -sf -o /dev/null "$TARGET_URL/login"; do
    tries=$((tries + 1))
    if [ "$tries" -gt 60 ]; then
      echo "app did not become ready at $TARGET_URL/login after 60s" >&2
      exit 1
    fi
    sleep 1
  done
}

# Recreates the `app` container with LOGSGUARDIAN_DISABLED set to $1
# ("true"|"false"), then waits for it to answer. `db` is left untouched -
# its data (10-row or 2010-row seed, depending on which scenario block is
# running) persists across app restarts, which is the point: baseline and
# active runs within the same scenario block must see identical data.
set_middleware() {
  local disabled="$1"
  log "recreating app with LOGSGUARDIAN_DISABLED=${disabled}"
  LOGSGUARDIAN_DISABLED="$disabled" docker compose "${COMPOSE_ARGS[@]}" up -d --no-deps app
  wait_for_app
}

# Runs one artillery scenario file REPS times, parses each run's post-warmup
# p95 via parse-latency-report.js, drops max/min, leaves the median of the
# remaining 3 in $REPS_MEDIAN_RESULT. Writes every raw report + the summary
# into $RESULTS_DIR.
#
# Deliberately NOT called via command substitution ($(run_reps ...)) or
# piped (run_reps | tail -1) - both patterns run the function in a subshell,
# and a failing command's exit status inside that subshell does NOT reliably
# abort the OUTER script under `set -e` on every bash version (verified:
# silently swallowed on bash 3.2/macOS, the only bash available for this
# worktree's local validation; bash >=4.4's `shopt -s inherit_errexit` fixes
# it but that option doesn't exist on 3.2, and this script has to work
# identically on both this Mac and the ubuntu-latest CI runner). Using a
# global result variable plus explicit `|| { ...; exit 1; }` checks on every
# step means a failure is fatal and loud on both bash versions, not just
# the one CI happens to ship.
#
# Phase durations/rates are always passed via --overrides, built from the
# WARMUP_S/MEASURED_S/WARMUP_RATE/<measured_rate> env-configurable values -
# this file's own `phases:` blocks are only the defaults used when someone
# runs `artillery run artillery-baseline.yml` directly (no suite script), as
# in this repo's local-validation instructions. Keeping the suite's phase
# config here (not duplicated/hand-synced in the yml) avoids the two
# drifting apart.
#
# Args: <label> <yaml-file> <measured-rate>
REPS_MEDIAN_RESULT=""
run_reps() {
  local label="$1"
  local yaml_file="$2"
  local measured_rate="$3"
  local p95_values=()

  local overrides
  overrides="$(node -e "console.log(JSON.stringify({config:{phases:[{duration:${WARMUP_S},arrivalRate:${WARMUP_RATE},name:'warmup (discard from analysis)'},{duration:${MEASURED_S},arrivalRate:${measured_rate},name:'measured'}]}}))")" \
    || { log "FATAL: could not build --overrides JSON"; exit 1; }

  for i in $(seq 1 "$REPS"); do
    local report_path="$RESULTS_DIR/${label}-rep${i}.json"
    log "  ${label} rep ${i}/${REPS}..."
    if ! artillery run -t "$TARGET_URL" -o "$report_path" --overrides "$overrides" "$yaml_file" \
        >"$RESULTS_DIR/${label}-rep${i}.log" 2>&1; then
      log "FATAL: artillery run failed for ${label} rep ${i} - see $RESULTS_DIR/${label}-rep${i}.log"
      exit 1
    fi
    if ! node "$SCRIPT_DIR/parse-latency-report.js" "$report_path" "$WARMUP_MS" \
        >"$RESULTS_DIR/${label}-rep${i}.parsed.json" 2>"$RESULTS_DIR/${label}-rep${i}.parse-error.log"; then
      log "FATAL: parse-latency-report.js failed for ${label} rep ${i} - see $RESULTS_DIR/${label}-rep${i}.parse-error.log"
      log "       (common cause: WARMUP_S/MEASURED_S too short for artillery's ~10s reporting buckets - see that script's header comment)"
      exit 1
    fi
    local p95
    p95="$(node -e "console.log(require('$RESULTS_DIR/${label}-rep${i}.parsed.json').p95)")" \
      || { log "FATAL: could not read p95 from ${label} rep ${i}'s parsed report"; exit 1; }
    log "    p95 (post-warmup, approx) = ${p95}ms"
    p95_values+=("$p95")
  done

  # Sort, drop min and max, median of remaining N-2 (N=5 in the default
  # config -> 3 remain, matching the protocol's "median of 3" requirement;
  # this generalizes to any REPS>=3 for smoke-testing with fewer reps).
  local sorted
  sorted=($(printf '%s\n' "${p95_values[@]}" | sort -n))
  local n="${#sorted[@]}"
  if [ "$n" -lt 3 ]; then
    log "FATAL: REPS=$REPS gives only $n samples for ${label} - need at least 3 to drop one min and one max and still have a median"
    exit 1
  fi
  local trimmed=("${sorted[@]:1:$((n-2))}")
  local mid=$((${#trimmed[@]} / 2))
  local median="${trimmed[$mid]}"

  log "  ${label}: raw p95s=[${p95_values[*]}] sorted=[${sorted[*]}] trimmed(min/max dropped)=[${trimmed[*]}] median=${median}ms"
  REPS_MEDIAN_RESULT="$median"
}

run_scenario_block() {
  local scenario_label="$1"
  local yaml_file="$2"
  local measured_rate="$3"

  log "=== scenario: ${scenario_label} (measured arrivalRate=${measured_rate}) ==="

  log "-- baseline (LOGSGUARDIAN_DISABLED=true) --"
  set_middleware true
  run_reps "${scenario_label}-baseline" "$yaml_file" "$measured_rate"
  local baseline_median="$REPS_MEDIAN_RESULT"

  log "-- active (LOGSGUARDIAN_DISABLED=false) --"
  set_middleware false
  run_reps "${scenario_label}-active" "$yaml_file" "$measured_rate"
  local active_median="$REPS_MEDIAN_RESULT"

  local delta
  delta="$(node -e "console.log((((${active_median} - ${baseline_median}) / ${baseline_median}) * 100).toFixed(1))")" \
    || { log "FATAL: could not compute delta for ${scenario_label}"; exit 1; }

  log "=== ${scenario_label} RESULT: baseline_p95=${baseline_median}ms active_p95=${active_median}ms delta_p95=${delta}% ==="

  cat >>"$RESULTS_DIR/summary.jsonl" <<EOF
{"scenario":"${scenario_label}","baseline_p95_ms":${baseline_median},"active_p95_ms":${active_median},"delta_p95_pct":${delta}}
EOF
}

log "results directory: $RESULTS_DIR"
log "compose args: ${COMPOSE_ARGS[*]}"
log "warmup=${WARMUP_S}s measured=${MEASURED_S}s reps=${REPS}"

: >"$RESULTS_DIR/summary.jsonl"

# 1. Normal load - benign navigation only, small (10-row) dataset as
#    seeded by db/init.sql (the default, nothing extra to do here).
run_scenario_block "normal" "$SCRIPT_DIR/artillery-baseline.yml" "$MEASURED_RATE_NORMAL"

# 2. Attack load - benign + concurrent attack traffic, same 10-row dataset.
run_scenario_block "attack" "$SCRIPT_DIR/artillery-attack-load.yml" "$MEASURED_RATE_ATTACK"

# 3. Volume - benign navigation only (same scenario file as "normal"), but
#    against a realistic ~2010-row `posts` table. Seeding happens once here,
#    AFTER the normal/attack blocks above (which need the small dataset) and
#    BEFORE this block's baseline+active runs (which both need the large
#    one). db/seed-large.sql is additive/non-idempotent - this must run
#    exactly once per fresh db container, which is what a per-workflow-run
#    fresh `docker compose up` guarantees.
log "seeding realistic data volume (2010 rows) for the volume scenario..."
"$SCRIPT_DIR/seed-large-dataset.sh" "${COMPOSE_ARGS[@]}"
run_scenario_block "volume" "$SCRIPT_DIR/artillery-baseline.yml" "$MEASURED_RATE_NORMAL"

log "all scenarios complete. summary:"
cat "$RESULTS_DIR/summary.jsonl"
log "full results in $RESULTS_DIR"
