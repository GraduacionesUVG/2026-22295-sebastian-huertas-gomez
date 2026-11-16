#!/usr/bin/env node
// Parses the CSV written by attack-sim/monitor-memory.sh and checks for a
// leak signature (monotonic memory growth) plus reports peak/mean CPU and
// memory. Kept separate from monitor-memory.sh so the sampler stays a
// dumb, robust background loop and all the unit-parsing / trend logic is
// unit-testable-by-eyeball in one place.
//
// "No leak" here means a specific, falsifiable claim: the second half of
// the sampled window is not meaningfully higher than the first half. This
// is a coarse heuristic (a real leak-hunting session would want an actual
// linear regression + more samples), appropriate for a CI gate that has to
// produce a pass/warn signal automatically, not a forensic analysis.
//
// Usage: node analyze-memory.js <monitor-memory.csv>

const fs = require('fs');

const csvPath = process.argv[2];
if (!csvPath) {
  console.error('usage: node analyze-memory.js <monitor-memory.csv>');
  process.exit(1);
}

// docker's MemUsage field looks like "123.4MiB / 1.952GiB" - parse the
// used-side number+unit and normalize to MB.
function parseMemToMb(raw) {
  const used = raw.split('/')[0].trim();
  const m = used.match(/^([\d.]+)\s*([A-Za-z]+)$/);
  if (!m) return null;
  const value = parseFloat(m[1]);
  const unit = m[2].toLowerCase();
  const factors = { b: 1 / (1024 * 1024), kib: 1 / 1024, kb: 1 / 1024, mib: 1, mb: 1, gib: 1024, gb: 1024 };
  const factor = factors[unit];
  if (factor === undefined) return null;
  return value * factor;
}

function parseCpuToPct(raw) {
  const m = raw.trim().match(/^([\d.]+)%$/);
  return m ? parseFloat(m[1]) : null;
}

const lines = fs.readFileSync(csvPath, 'utf8').trim().split('\n');
const header = lines.shift();
if (!header || !header.startsWith('timestamp_iso')) {
  console.error(`${csvPath} does not look like a monitor-memory.sh CSV (unexpected header: ${header})`);
  process.exit(1);
}

const samples = [];
for (const line of lines) {
  if (!line.trim()) continue;
  const [timestamp, memRaw, cpuRaw] = line.split(',');
  const memMb = parseMemToMb(memRaw);
  const cpuPct = parseCpuToPct(cpuRaw);
  if (memMb === null || cpuPct === null) continue;
  samples.push({ timestamp, memMb, cpuPct });
}

if (samples.length < 4) {
  console.error(`only ${samples.length} valid samples in ${csvPath} - need at least 4 for a first-half/second-half comparison`);
  process.exit(1);
}

const half = Math.floor(samples.length / 2);
const firstHalf = samples.slice(0, half);
const secondHalf = samples.slice(half);

const mean = (arr, key) => arr.reduce((sum, s) => sum + s[key], 0) / arr.length;

const memFirstHalfMean = mean(firstHalf, 'memMb');
const memSecondHalfMean = mean(secondHalf, 'memMb');
const memGrowthPct = ((memSecondHalfMean - memFirstHalfMean) / memFirstHalfMean) * 100;

const memPeak = Math.max(...samples.map((s) => s.memMb));
const memMean = mean(samples, 'memMb');
const cpuPeak = Math.max(...samples.map((s) => s.cpuPct));
const cpuMean = mean(samples, 'cpuPct');

// Threshold: flag as a possible leak only if the second half runs at least
// 15% higher than the first half AND the absolute growth is more than a few
// MB (so normal sample-to-sample noise on a small idle process doesn't
// trip a false "leak" flag). 15% is a judgment call, not a value from the
// protocol (which specifies a leak-free requirement qualitatively, not a
// numeric growth threshold) - documented here so it can be argued with.
const POSSIBLE_LEAK = memGrowthPct > 15 && (memSecondHalfMean - memFirstHalfMean) > 5;

const windowStart = samples[0].timestamp;
const windowEnd = samples[samples.length - 1].timestamp;
const windowSeconds = (new Date(windowEnd) - new Date(windowStart)) / 1000;

const result = {
  csvPath,
  sampleCount: samples.length,
  windowStart,
  windowEnd,
  windowSeconds,
  windowMinutes: +(windowSeconds / 60).toFixed(1),
  memory: {
    firstHalfMeanMb: +memFirstHalfMean.toFixed(1),
    secondHalfMeanMb: +memSecondHalfMean.toFixed(1),
    growthPct: +memGrowthPct.toFixed(1),
    peakMb: +memPeak.toFixed(1),
    meanMb: +memMean.toFixed(1),
    possibleLeak: POSSIBLE_LEAK,
  },
  cpu: {
    peakPct: +cpuPeak.toFixed(1),
    meanPct: +cpuMean.toFixed(1),
  },
  verdict: POSSIBLE_LEAK
    ? 'WARN: second-half memory usage is >15% higher than first-half - review for a leak, do not treat as conclusive from this heuristic alone'
    : 'OK: no monotonic-growth signature detected at this heuristic threshold',
};

console.log(JSON.stringify(result, null, 2));
