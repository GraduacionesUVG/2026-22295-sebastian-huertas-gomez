# Resource usage summary (memory and CPU, `app` container)

Archive: `latency-linux-2026-09-26.tgz`
SHA-256: `b96d901408547331fb4859a5dac4810abdb1caaeb2f15f3378877c2290187cec`
Samples: 374 | Repetitions: 30

## Segmentation rule

A sample belongs to repetition R when firstMetricAt <= timestamp <= lastMetricAt of R's Artillery report (epoch ms). Window A also drops samples with timestamp < firstMetricAt + 15 s (warmup). Window B keeps the whole repetition. Samples outside every repetition are out of window.

## Windows

- **A (primary):** measured period, first 15 s of each repetition dropped
- **B:** full repetition

## Per condition

| Scenario | Condition | Window | Reps | n | Mem MB mean / median / max | CPU % mean / median / max |
|---|---|---|---|---|---|---|
| attack | baseline | A | 5 | 45 | 63.22 / 66.24 / 69.21 | 16.07 / 16.08 / 28.82 |
| attack | baseline | B | 5 | 55 | 61.16 / 66.23 / 69.21 | 13.93 / 14.12 / 28.82 |
| attack | active | A | 5 | 43 | 394.78 / 401.00 / 405.70 | 101.25 / 100.93 / 120.60 |
| attack | active | B | 5 | 55 | 387.05 / 398.90 / 405.70 | 89.31 / 99.50 / 177.54 |
| normal | baseline | A | 5 | 45 | 65.18 / 66.25 / 68.83 | 14.48 / 14.18 / 20.61 |
| normal | baseline | B | 5 | 59 | 61.36 / 66.11 / 68.83 | 11.85 / 12.96 / 20.61 |
| normal | active | A | 5 | 44 | 397.51 / 399.25 / 421.10 | 103.32 / 101.59 / 126.95 |
| normal | active | B | 5 | 56 | 388.79 / 395.35 / 421.10 | 91.02 / 100.95 / 181.53 |
| volume | baseline | A | 5 | 43 | 83.29 / 81.47 / 119.10 | 82.34 / 82.04 / 89.99 |
| volume | baseline | B | 5 | 55 | 82.77 / 80.70 / 119.10 | 67.28 / 80.85 / 89.99 |
| volume | active | A | 5 | 50 | 459.15 / 475.55 / 494.80 | 115.29 / 112.92 / 149.33 |
| volume | active | B | 5 | 60 | 454.32 / 475.75 / 494.80 | 105.94 / 112.22 / 177.09 |

## Paired increments (active - baseline, per repetition)

Δ values are the mean of per-repetition pair differences. Relative values divide by the baseline mean.

| Scenario | Window | Pairs | Δ mem (MB) | Δ mem (%) | Δ CPU (pp) | Δ CPU (%) |
|---|---|---|---|---|---|---|
| attack | A | 5 | +331.86 | +524.95 | +85.12 | +529.61 |
| attack | B | 5 | +325.89 | +532.86 | +75.38 | +541.28 |
| normal | A | 5 | +332.02 | +509.41 | +88.93 | +614.35 |
| normal | B | 5 | +327.21 | +533.86 | +79.40 | +668.85 |
| volume | A | 5 | +375.92 | +451.65 | +32.99 | +40.09 |
| volume | B | 5 | +371.55 | +448.88 | +38.66 | +57.46 |

## Flags

Threshold: CPU difference between A and B above 5.0 pp.

- attack/active: mean CPU A vs B differs by 11.94 pp
- normal/active: mean CPU A vs B differs by 12.30 pp
- volume/baseline: mean CPU A vs B differs by 15.06 pp
- volume/active: mean CPU A vs B differs by 9.35 pp
- attack: paired CPU increment A vs B differs by 9.73 pp
- normal: paired CPU increment A vs B differs by 9.53 pp
- volume: paired CPU increment A vs B differs by 5.67 pp

## Samples out of window

### Window A: 104 samples out of window

| Timestamp (UTC) | Mem MB | CPU % | Reason | Repetition |
|---|---|---|---|---|
| 2026-09-26T22:36:11Z | 219.20 | 184.70 | outside_run | - |
| 2026-09-26T22:36:18Z | 216.50 | 198.60 | outside_run | - |
| 2026-09-26T22:36:24Z | 24.86 | 9.06 | outside_run | - |
| 2026-09-26T22:36:31Z | 35.42 | 6.53 | warmup | normal-baseline-rep1 |
| 2026-09-26T22:36:38Z | 26.53 | 4.20 | warmup | normal-baseline-rep1 |
| 2026-09-26T22:37:45Z | 66.51 | 1.05 | warmup | normal-baseline-rep2 |
| 2026-09-26T22:37:51Z | 65.58 | 2.82 | warmup | normal-baseline-rep2 |
| 2026-09-26T22:37:58Z | 29.15 | 5.39 | warmup | normal-baseline-rep2 |
| 2026-09-26T22:39:05Z | 66.11 | 1.87 | warmup | normal-baseline-rep3 |
| 2026-09-26T22:39:11Z | 29.79 | 4.69 | warmup | normal-baseline-rep3 |
| 2026-09-26T22:39:18Z | 36.28 | 4.19 | warmup | normal-baseline-rep3 |
| 2026-09-26T22:40:25Z | 66.95 | 1.97 | warmup | normal-baseline-rep4 |
| 2026-09-26T22:40:32Z | 67.46 | 2.71 | warmup | normal-baseline-rep4 |
| 2026-09-26T22:40:38Z | 29.27 | 4.18 | warmup | normal-baseline-rep4 |
| 2026-09-26T22:41:45Z | 68.41 | 1.86 | warmup | normal-baseline-rep5 |
| 2026-09-26T22:41:52Z | 67.54 | 2.93 | warmup | normal-baseline-rep5 |
| 2026-09-26T22:41:58Z | 32.29 | 3.36 | warmup | normal-baseline-rep5 |
| 2026-09-26T22:43:05Z | 67.23 | 0.00 | outside_run | - |
| 2026-09-26T22:43:12Z | 0.00 | 0.00 | outside_run | - |
| 2026-09-26T22:43:18Z | 226.70 | 175.31 | warmup | normal-active-rep1 |
| 2026-09-26T22:43:25Z | 252.10 | 181.53 | warmup | normal-active-rep1 |
| 2026-09-26T22:43:32Z | 269.00 | 29.50 | warmup | normal-active-rep1 |
| 2026-09-26T22:44:33Z | 391.60 | 1.03 | outside_run | - |
| 2026-09-26T22:44:40Z | 372.20 | 19.89 | warmup | normal-active-rep2 |
| 2026-09-26T22:44:46Z | 382.60 | 21.30 | warmup | normal-active-rep2 |
| 2026-09-26T22:45:54Z | 394.80 | 0.63 | outside_run | - |
| 2026-09-26T22:46:01Z | 394.90 | 19.90 | warmup | normal-active-rep3 |
| 2026-09-26T22:46:07Z | 381.60 | 21.45 | warmup | normal-active-rep3 |
| 2026-09-26T22:47:15Z | 400.70 | 0.01 | outside_run | - |
| 2026-09-26T22:47:22Z | 389.00 | 19.60 | warmup | normal-active-rep4 |
| 2026-09-26T22:47:29Z | 379.40 | 20.28 | warmup | normal-active-rep4 |
| 2026-09-26T22:48:37Z | 412.00 | 0.02 | warmup | normal-active-rep5 |
| 2026-09-26T22:48:43Z | 411.20 | 22.30 | warmup | normal-active-rep5 |
| 2026-09-26T22:48:50Z | 411.00 | 19.84 | warmup | normal-active-rep5 |
| 2026-09-26T22:49:58Z | 404.20 | 0.01 | outside_run | - |
| 2026-09-26T22:50:04Z | 0.00 | 0.00 | outside_run | - |
| 2026-09-26T22:50:11Z | 28.57 | 5.51 | warmup | attack-baseline-rep1 |
| 2026-09-26T22:50:18Z | 22.68 | 7.34 | warmup | attack-baseline-rep1 |
| 2026-09-26T22:51:25Z | 67.22 | 0.54 | outside_run | - |
| 2026-09-26T22:51:31Z | 67.36 | 4.48 | warmup | attack-baseline-rep2 |
| 2026-09-26T22:51:38Z | 67.50 | 2.57 | warmup | attack-baseline-rep2 |
| 2026-09-26T22:52:45Z | 66.50 | 0.53 | outside_run | - |
| 2026-09-26T22:52:51Z | 66.03 | 2.24 | warmup | attack-baseline-rep3 |
| 2026-09-26T22:52:58Z | 30.98 | 6.38 | warmup | attack-baseline-rep3 |
| 2026-09-26T22:54:05Z | 66.44 | 0.55 | outside_run | - |
| 2026-09-26T22:54:12Z | 66.18 | 2.32 | warmup | attack-baseline-rep4 |
| 2026-09-26T22:54:18Z | 33.69 | 7.22 | warmup | attack-baseline-rep4 |
| 2026-09-26T22:55:25Z | 67.86 | 0.51 | outside_run | - |
| 2026-09-26T22:55:32Z | 67.93 | 2.30 | warmup | attack-baseline-rep5 |
| 2026-09-26T22:55:38Z | 68.11 | 2.40 | warmup | attack-baseline-rep5 |
| 2026-09-26T22:56:45Z | 68.98 | 0.50 | outside_run | - |
| 2026-09-26T22:56:52Z | 68.55 | 0.00 | outside_run | - |
| 2026-09-26T22:56:59Z | 216.80 | 102.92 | outside_run | - |
| 2026-09-26T22:57:05Z | 225.30 | 175.09 | warmup | attack-active-rep1 |
| 2026-09-26T22:57:12Z | 247.80 | 177.54 | warmup | attack-active-rep1 |
| 2026-09-26T22:58:20Z | 389.70 | 0.00 | outside_run | - |
| 2026-09-26T22:58:27Z | 368.90 | 20.89 | warmup | attack-active-rep2 |
| 2026-09-26T22:58:34Z | 378.80 | 19.16 | warmup | attack-active-rep2 |
| 2026-09-26T22:59:42Z | 379.70 | 12.64 | warmup | attack-active-rep3 |
| 2026-09-26T22:59:48Z | 388.50 | 17.80 | warmup | attack-active-rep3 |
| 2026-09-26T22:59:55Z | 369.30 | 20.24 | warmup | attack-active-rep3 |
| 2026-09-26T23:00:56Z | 402.70 | 53.78 | outside_run | - |
| 2026-09-26T23:01:03Z | 402.40 | 14.69 | warmup | attack-active-rep4 |
| 2026-09-26T23:01:10Z | 375.30 | 20.52 | warmup | attack-active-rep4 |
| 2026-09-26T23:01:16Z | 380.00 | 38.35 | warmup | attack-active-rep4 |
| 2026-09-26T23:02:17Z | 403.10 | 0.51 | outside_run | - |
| 2026-09-26T23:02:24Z | 403.70 | 22.04 | warmup | attack-active-rep5 |
| 2026-09-26T23:02:31Z | 392.50 | 19.37 | warmup | attack-active-rep5 |
| 2026-09-26T23:03:38Z | 406.00 | 0.81 | outside_run | - |
| 2026-09-26T23:03:45Z | 405.80 | 0.06 | outside_run | - |
| 2026-09-26T23:03:52Z | 20.53 | 0.05 | outside_run | - |
| 2026-09-26T23:03:58Z | 61.65 | 14.82 | warmup | volume-baseline-rep1 |
| 2026-09-26T23:04:05Z | 64.15 | 13.77 | warmup | volume-baseline-rep1 |
| 2026-09-26T23:05:13Z | 108.40 | 0.01 | outside_run | - |
| 2026-09-26T23:05:19Z | 109.00 | 11.58 | warmup | volume-baseline-rep2 |
| 2026-09-26T23:05:26Z | 109.60 | 11.59 | warmup | volume-baseline-rep2 |
| 2026-09-26T23:06:33Z | 75.36 | 4.28 | outside_run | - |
| 2026-09-26T23:06:40Z | 74.10 | 14.26 | warmup | volume-baseline-rep3 |
| 2026-09-26T23:06:47Z | 75.82 | 12.29 | warmup | volume-baseline-rep3 |
| 2026-09-26T23:07:54Z | 79.55 | 11.47 | warmup | volume-baseline-rep4 |
| 2026-09-26T23:08:01Z | 78.14 | 12.40 | warmup | volume-baseline-rep4 |
| 2026-09-26T23:08:07Z | 78.53 | 11.45 | warmup | volume-baseline-rep4 |
| 2026-09-26T23:09:08Z | 80.38 | 65.23 | outside_run | - |
| 2026-09-26T23:09:15Z | 79.46 | 12.18 | warmup | volume-baseline-rep5 |
| 2026-09-26T23:09:21Z | 80.81 | 11.52 | warmup | volume-baseline-rep5 |
| 2026-09-26T23:09:28Z | 80.14 | 22.55 | warmup | volume-baseline-rep5 |
| 2026-09-26T23:10:29Z | 81.52 | 0.42 | outside_run | - |
| 2026-09-26T23:10:36Z | 80.77 | 0.06 | outside_run | - |
| 2026-09-26T23:10:42Z | 216.20 | 152.71 | outside_run | - |
| 2026-09-26T23:10:49Z | 255.10 | 168.60 | warmup | volume-active-rep1 |
| 2026-09-26T23:10:56Z | 276.20 | 177.09 | warmup | volume-active-rep1 |
| 2026-09-26T23:12:10Z | 483.80 | 1.24 | outside_run | - |
| 2026-09-26T23:12:17Z | 484.10 | 32.82 | warmup | volume-active-rep2 |
| 2026-09-26T23:12:24Z | 483.60 | 29.86 | warmup | volume-active-rep2 |
| 2026-09-26T23:13:38Z | 474.20 | 0.01 | outside_run | - |
| 2026-09-26T23:13:45Z | 475.20 | 29.79 | warmup | volume-active-rep3 |
| 2026-09-26T23:13:52Z | 403.60 | 32.21 | warmup | volume-active-rep3 |
| 2026-09-26T23:15:06Z | 485.70 | 66.48 | outside_run | - |
| 2026-09-26T23:15:13Z | 463.30 | 30.77 | warmup | volume-active-rep4 |
| 2026-09-26T23:15:20Z | 477.30 | 30.41 | warmup | volume-active-rep4 |
| 2026-09-26T23:16:34Z | 487.70 | 60.27 | outside_run | - |
| 2026-09-26T23:16:41Z | 491.30 | 30.70 | warmup | volume-active-rep5 |
| 2026-09-26T23:16:48Z | 492.40 | 29.78 | warmup | volume-active-rep5 |
| 2026-09-26T23:18:02Z | 493.50 | 0.01 | outside_run | - |

### Window B: 34 samples out of window

| Timestamp (UTC) | Mem MB | CPU % | Reason | Repetition |
|---|---|---|---|---|
| 2026-09-26T22:36:11Z | 219.20 | 184.70 | outside_run | - |
| 2026-09-26T22:36:18Z | 216.50 | 198.60 | outside_run | - |
| 2026-09-26T22:36:24Z | 24.86 | 9.06 | outside_run | - |
| 2026-09-26T22:43:05Z | 67.23 | 0.00 | outside_run | - |
| 2026-09-26T22:43:12Z | 0.00 | 0.00 | outside_run | - |
| 2026-09-26T22:44:33Z | 391.60 | 1.03 | outside_run | - |
| 2026-09-26T22:45:54Z | 394.80 | 0.63 | outside_run | - |
| 2026-09-26T22:47:15Z | 400.70 | 0.01 | outside_run | - |
| 2026-09-26T22:49:58Z | 404.20 | 0.01 | outside_run | - |
| 2026-09-26T22:50:04Z | 0.00 | 0.00 | outside_run | - |
| 2026-09-26T22:51:25Z | 67.22 | 0.54 | outside_run | - |
| 2026-09-26T22:52:45Z | 66.50 | 0.53 | outside_run | - |
| 2026-09-26T22:54:05Z | 66.44 | 0.55 | outside_run | - |
| 2026-09-26T22:55:25Z | 67.86 | 0.51 | outside_run | - |
| 2026-09-26T22:56:45Z | 68.98 | 0.50 | outside_run | - |
| 2026-09-26T22:56:52Z | 68.55 | 0.00 | outside_run | - |
| 2026-09-26T22:56:59Z | 216.80 | 102.92 | outside_run | - |
| 2026-09-26T22:58:20Z | 389.70 | 0.00 | outside_run | - |
| 2026-09-26T23:00:56Z | 402.70 | 53.78 | outside_run | - |
| 2026-09-26T23:02:17Z | 403.10 | 0.51 | outside_run | - |
| 2026-09-26T23:03:38Z | 406.00 | 0.81 | outside_run | - |
| 2026-09-26T23:03:45Z | 405.80 | 0.06 | outside_run | - |
| 2026-09-26T23:03:52Z | 20.53 | 0.05 | outside_run | - |
| 2026-09-26T23:05:13Z | 108.40 | 0.01 | outside_run | - |
| 2026-09-26T23:06:33Z | 75.36 | 4.28 | outside_run | - |
| 2026-09-26T23:09:08Z | 80.38 | 65.23 | outside_run | - |
| 2026-09-26T23:10:29Z | 81.52 | 0.42 | outside_run | - |
| 2026-09-26T23:10:36Z | 80.77 | 0.06 | outside_run | - |
| 2026-09-26T23:10:42Z | 216.20 | 152.71 | outside_run | - |
| 2026-09-26T23:12:10Z | 483.80 | 1.24 | outside_run | - |
| 2026-09-26T23:13:38Z | 474.20 | 0.01 | outside_run | - |
| 2026-09-26T23:15:06Z | 485.70 | 66.48 | outside_run | - |
| 2026-09-26T23:16:34Z | 487.70 | 60.27 | outside_run | - |
| 2026-09-26T23:18:02Z | 493.50 | 0.01 | outside_run | - |

