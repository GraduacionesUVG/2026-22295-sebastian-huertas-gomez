#!/usr/bin/env node
// Extracts a post-warmup p95 (and p50/p99) from an Artillery JSON report
// (`artillery run -o report.json`), discarding the warmup phase instead of
// trusting `aggregate` (which mixes warmup + measured traffic together).
//
// Why this exists: Artillery's `aggregate.summaries['http.response_time']`
// is computed over the WHOLE run, including the warmup phase defined in
// artillery-baseline.yml / artillery-attack-load.yml. Artillery 2.x does
// not expose a way to scope `aggregate` to a subset of phases, and its
// percentile sketches (t-digest) aren't safely mergeable by hand from
// outside the tool. The `intermediate` array in the report, however,
// already contains one self-contained summary (with its own p50/p95/p99
// and sample count) per ~10s wall-clock bucket. This script:
//   1. Finds the earliest bucket start (`period`) in the report - the test
//      origin.
//   2. Discards every bucket that starts before `origin + warmupMs`.
//   3. Combines the surviving buckets' percentiles into one number via a
//      count-weighted average.
//
// Caveat, stated explicitly rather than hidden: a count-weighted average of
// per-bucket p95 values is an APPROXIMATION of the true p95 of the pooled
// post-warmup samples, not a mathematically exact merge (that would require
// re-deriving p95 from the underlying digest, which Artillery's JSON report
// does not expose). It is a reasonable approximation when buckets are
// similarly sized and the distribution is stable within the measured phase
// (true here - IF/RF inference cost does not drift over a 60s steady-state
// run per the sibling repo's own chunked-timing investigation, see
// docs/vulnerable-app-evaluation/config2-latency-evaluation.md around the
// "regrowth under sustained load" section). Do not use this script's output
// as a substitute for a from-scratch statistical re-analysis if the thesis
// write-up needs a rigorous confidence interval - it's a pragmatic
// warmup-exclusion tool for a CI harness, not a stats package.
//
// Usage: node parse-latency-report.js <report.json> [warmupMs=15000] [metric=http.response_time]

const fs = require('fs');

const [, , reportPath, warmupMsArg, metricArg] = process.argv;
if (!reportPath) {
  console.error('usage: node parse-latency-report.js <report.json> [warmupMs=15000] [metric=http.response_time]');
  process.exit(1);
}
const warmupMs = warmupMsArg ? parseInt(warmupMsArg, 10) : 15000;
const metric = metricArg || 'http.response_time';

const report = JSON.parse(fs.readFileSync(reportPath, 'utf8'));
const periods = report.intermediate || [];
if (periods.length === 0) {
  console.error(`no 'intermediate' periods found in ${reportPath} - cannot exclude warmup`);
  process.exit(1);
}

const origin = Math.min(...periods.map((p) => p.period));
const measured = periods.filter((p) => p.period - origin >= warmupMs);

if (measured.length === 0) {
  console.error(
    `every period in ${reportPath} falls inside the ${warmupMs}ms warmup window - ` +
      `the run is too short for this warmupMs, or warmupMs is misconfigured`
  );
  process.exit(1);
}

let totalCount = 0;
let weightedP50 = 0;
let weightedP95 = 0;
let weightedP99 = 0;
let weightedMean = 0;

for (const p of measured) {
  const s = (p.summaries || {})[metric];
  if (!s || !s.count) continue;
  totalCount += s.count;
  weightedP50 += s.p50 * s.count;
  weightedP95 += s.p95 * s.count;
  weightedP99 += s.p99 * s.count;
  weightedMean += s.mean * s.count;
}

if (totalCount === 0) {
  console.error(`metric '${metric}' has zero samples across the post-warmup periods in ${reportPath}`);
  process.exit(1);
}

const result = {
  reportPath,
  metric,
  warmupMs,
  bucketsTotal: periods.length,
  bucketsDiscardedAsWarmup: periods.length - measured.length,
  bucketsMeasured: measured.length,
  sampleCount: totalCount,
  p50: +(weightedP50 / totalCount).toFixed(2),
  p95: +(weightedP95 / totalCount).toFixed(2),
  p99: +(weightedP99 / totalCount).toFixed(2),
  mean: +(weightedMean / totalCount).toFixed(2),
  note: 'p50/p95/p99 are count-weighted averages of per-bucket percentiles from post-warmup buckets only - see file header comment for why this is an approximation, not an exact merge.',
};

console.log(JSON.stringify(result, null, 2));
