# Latency benchmark evidence: Linux run (2026-09-26)

Raw evidence from the CI latency benchmark run that produced the Linux
numbers for the Config 2 latency evaluation.

## Run identification

| Field | Value |
|---|---|
| Workflow | `.github/workflows/latency-benchmark.yml` |
| Run ID | 36276690236 |
| Artifact ID | 10917957439 |
| Commit | `f15a9e8` |
| Date | 2026-09-26 |
| Artifact expiry (original GitHub artifact) | 2026-10-26 |

## Runner

| Field | Value |
|---|---|
| OS / arch | Ubuntu (Azure runner), x86_64 |
| CPU | 2 vCPU |
| Memory | 7.8 GiB |
| Docker Engine | 28.0.4 |
| Docker Compose | v2.38.2 |

## Models used in the run

Both models are taken from commit `f15a9e8`
(`git show f15a9e8:models/<file>`):

| File | Size (bytes) | SHA-256 |
|---|---|---|
| `models/rf.onnx` | 8833043 | `a7c015f5a5fa3fabfd91b79ec9338dc7da6a68c392c19ded4b04cc6f0fb903b2` |
| `models/if.onnx` | 2094695 | `3cf8e45c285de19bc86e6dc284e502cd2c24becb888747b9645bed4cfb224417` |

## Archive contents

`latency-linux-2026-09-26.tgz` (SHA-256
`b96d901408547331fb4859a5dac4810abdb1caaeb2f15f3378877c2290187cec`)
extracts to `latency-linux-2026-09-26/`:

- `20260926-223609/`: 30 Artillery JSON reports (`<scenario>-<condition>-rep<n>.json`,
  3 scenarios x 2 conditions x 5 repetitions), their parsed p95 summaries
  (`*.parsed.json`), per-run logs (`*.log`), and parse-error logs (empty when the parse succeeded).
- `20260926-223609/summary.jsonl`: one line per scenario with the baseline and
  active p95 medians and the delta.
- `memory-cpu.csv`: `docker stats` samples for the `app` container, every ~5 s
  across the whole suite.
- `monitor-memory.log`: stderr of the monitor script.
- `memory-analysis.json`: output of `attack-sim/analyze-memory.js` on `memory-cpu.csv`.

## Notes for interpreting the numbers

- **p95 is approximate.** `parse-latency-report.js` computes each p95 as a
  count-weighted average of the per-interval p95 values after discarding the
  warmup intervals. It is not an exact percentile of the pooled samples.
- **Timeouts are not in `http.response_time`.** Requests that time out are not
  included in the response-time distribution the p95 is computed from.
- **`memory-cpu.csv` measures the container, not the process.** It comes from
  `docker stats` on the `app` container (`MemUsage` and `CPUPerc`), so it
  includes everything in the container cgroup, not only the Node heap.
- **Re-running.** The suite and monitor are in `attack-sim/`
  (`run_latency_suite.sh`, `monitor-memory.sh`, `analyze-memory.js`).
