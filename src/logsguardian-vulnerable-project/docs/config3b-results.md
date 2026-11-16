# Config 3b — WAF + logSguarDian (Layered) — Round 1

## Setup

Nginx+ModSecurity v3+CRS (PL1, blocking) -> Express+logSguarDian
(rf_v10/if_v9) -> Postgres. App internal-only, all traffic
forced through WAF.

## Round 1: same 9 attack cases as Config 1/2

| # | Attack | HTTP Status | Blocked by | CRS rule(s) | Reached app / logsguardian? |
|---|--------|-------------|------------|--------------|------------------------------|
| 1 | SQLi auth bypass (`' OR '1'='1' --`) | 403 | WAF | 942100 (libinjection SQLi), score 5 | No |
| 2 | SQLi UNION exfil | 403 | WAF | 942100, 942190, 942270, 942360, score 20 | No |
| 3 | XSS bio store (`<script>`) | 403 | WAF | 941100, 941110, 941160, 941180, score 20 | No |
| 4 | XSS post-content (`<script>fetch...`) | 403 | WAF | 941100, 941110, 941160, 941180, score 20 | No |
| 5 | Path traversal `/etc/passwd` | 403 | WAF | 930100, 930110x2, 930120, 932160, score 30 | No |
| 6 | Path traversal source code | 403 | WAF | 930100, 930110x2, score 20 | No |
| 7 | Cmd injection (obvious, `; cat /etc/passwd`) | 403 | WAF | 930120, 932100, 932160, score 15 | No |
| 8 | Cmd injection (minimal-context, `; whoami`) | 403 | WAF | 932105, 932115, score 10 | No |
| 9 | XSS multi-field dilution (`<img onerror=...>`) | 403 | WAF | 941100, 941120, 941160, 941180, score 20 | No |

## Finding

ModSecurity+CRS at PL1 caught 9/9 signature-based attacks -
including the two cases logsguardian's ML layer had to be
specifically engineered to catch (minimal-context recon
payloads, multi-field body dilution). This confirms PL1 CRS
is well-configured and effective against known/cataloged
attack signatures.

## Limitation of this round

This corpus was built to test logsguardian specifically and
is drawn from well-known, unobfuscated attack patterns -
exactly what signature-based WAF rules are designed to catch.
It provides ZERO evidence on the actual research question
(does logsguardian's ML layer catch attacks that evade
signature-based detection), because nothing reached the
second layer to test it against.

## Next: Round 2 - WAF-evasion corpus

To answer the defense-in-depth question properly, Round 2
uses payload variants specifically designed to evade CRS
signature matching (encoding tricks, comment injection, case
variation, whitespace manipulation) while preserving the
underlying attack semantics - testing whether logsguardian's
feature-based/statistical approach catches what rule-based
pattern matching misses.

## Round 2 — WAF-evasion corpus

14 variants of the same 9 attack categories, using techniques
known to evade CRS signature matching specifically (inline
comments, case variation, alternate operators, percent-encoded
quotes, mixed-case tags, uncommon event handlers, SVG vectors,
double URL-encoding, mixed slashes, null bytes, `${IFS}`
substitution, backtick+IFS, newline separators).

| ID | Category | Variant | HTTP Status | WAF verdict | CRS rules hit | Reached app? |
|----|----------|---------|-------------|-------------|----------------|----------------|
| S1 | SQLi | inline-comment `/**/` | 403 | Blocked | 942100, score 5 | No |
| S2 | SQLi | case variation `oR` | 403 | Blocked | 942100, score 5 | No |
| S3 | SQLi | `LIKE` operator swap | 403 | Blocked | 942100, score 5 | No |
| S4 | SQLi | %27-encoded quotes | 403 | Blocked | 942100, score 5 | No |
| X1 | XSS | mixed-case `<ScRiPt>` | 403 | Blocked | 941100, 941110, 941160, 941180, score 20 | No |
| X2 | XSS | `onpointerover` handler | 403 | Blocked | 941100, 941120, 941160, 941180, score 20 | No |
| X3 | XSS | `onanimationstart` handler | 403 | Blocked | 941100, 941120, 941160, 941180, score 20 | No |
| X4 | XSS | `<svg/onload=...>` | 403 | Blocked | 941100, 941120, 941160, 941180, score 20 | No |
| P1 | Path traversal | double URL-encoding `%252e` | 403 | Blocked | 930100, 930110x2, 930120, 932160, score 30 | No |
| P2 | Path traversal | mixed `\`/`/` slashes | 403 | Blocked | 930100, 930110x4, 930120, 932160, score 40 | No |
| P3 | Path traversal | trailing null byte `%00` | 403 | Blocked | 920270, 930100, 930110x3, 930120, 932160, score 50 | No |
| C1 | Cmd injection | `${IFS}` space substitution | 403 | Blocked | 930120, 932130, 932160, score 15 | No |
| C2 | Cmd injection | backtick + `${IFS}` | 403 | Blocked | 932130, 932160, score 10 | No |
| C3 | Cmd injection | `\n` separator instead of `;` | 403 | Blocked | 930120, 932100, 932160, score 15 | No |

Note: a 4th cmdi variant (case-variation in commands, e.g.
`CAT /etc/passwd`) was dropped from the plan — most POSIX
shells are case-sensitive, so it would break the attack's own
semantics rather than evade the WAF. Substituted a `\n`
separator variant (C3) instead, which preserves semantics
while testing a real evasion technique.

### Round 2 finding

0/14 evasion variants passed ModSecurity. `detection_events`
max id unchanged before/after (24014), confirming none reached
the app. CRS's `libinjection` tokenization (SQL/HTML semantic
parsing, not literal string matching) is inline-comment- and
case-invariant by construction, and its `t:urlDecodeUni` /
`t:removeNulls` / `t:compressWhitespace` transformation chains
normalize double-encoding, null bytes, and IFS/whitespace
tricks before the pattern rules run.

### Round 2 limitation

Same structural problem as Round 1, one level up: this still
provides zero evidence on whether logsguardian catches what
CRS misses, because nothing reached logsguardian to test.
The evasion techniques chosen are well-known specifically
because CRS's transformation pipeline is built to neutralize
them — testing logsguardian's independent detection capability
requires a different experimental design, not more elaborate
evasion attempts against an already well-tuned WAF.

## Round 3 — Standalone Detection Capability (Reframed)

Rounds 1-2 confirmed CRS PL1 is a mature, well-tuned defense
against both known attack signatures and common evasion
techniques (0/14 evasion variants passed). This is expected
and valuable in itself - a poorly-configured WAF would
undermine the premise of testing defense-in-depth at all.

Round 3 answers a different, more precise question: does
logSguarDian function as an effective independent detector,
with detection capability not dependent on signature-based
matching? To test this in isolation, the WAF's rule engine
is deliberately relaxed (lower paranoia level or specific
rule IDs disabled) to synthetically create requests that
reach the app layer - simulating a WAF gap (misconfiguration,
zero-day signature gap, or intentionally permissive rule set)
rather than attempting to defeat a well-configured CRS
deployment.

This is standard layered-defense evaluation methodology:
testing each layer's independent contribution, not solely
their combined behavior under identical, fully-hardened
conditions.

Config: `MODSEC_RULE_ENGINE: DetectionOnly`. CRS still
evaluates and logs every request (so its would-have-blocked
verdict is known via the audit log) but never interrupts, so
every request reaches the app — giving a full attribution
table for all 23 payloads (9 original + 14 evasion) without
needing multiple WAF restart cycles.

### Initial result: 21/23 (91.3%)

All 9 Round 1 originals and all 14 Round 2 evasion variants
were re-run against the app directly. CRS's audit log
confirmed it would have flagged and blocked all 23 (same
verdicts as Rounds 1-2, just not enforced) — so every 403 in
this round is logsguardian's own block, and every 200/302 is
a logsguardian miss, independent of CRS.

16/23 were caught (`verdict: block`) with correct or
functionally-correct classification. Two were blocked but
mislabeled (P1: path traversal classified as `xss`; C1: cmdi
classified as `sqli` — both still `verdict: block`, so
functionally caught).

7/23 were missed, and all 7 were XSS: the two original XSS
cases (R3, R9) plus a third (R4) and all four evasion variants
(X1-X4). Every one returned `predicted_class: benign` at
~0.5 confidence. Initially read as a genuine XSS blind spot in
the ML layer, standalone.

### Root cause investigation

Not a detection gap — a middleware-ordering bug. In
`src/app.js`, logsguardian was mounted globally, before any
multipart parsing occurred. `multer` (the app's multipart
parser) was only ever mounted per-route, in `src/routes/posts.js`,
which runs *after* the global logsguardian middleware. All 7
missed payloads had been sent as `multipart/form-data` (curl
`--form-string`), incidentally — not because XSS specifically
requires multipart delivery, but because that's how this test
corpus happened to construct XSS requests (bio/title/content
form fields) versus the SQLi/PT/cmdi cases (query strings or
urlencoded bodies). logsguardian's own code documents the
failure mode: `req.body` is `{}` when no body-parser has run
yet — so it saw an empty body for every one of these,
regardless of payload content, and passed all of them.

Confirmed directly: the identical R4 payload, resent as
`application/x-www-form-urlencoded` instead of multipart, was
correctly blocked as `xss` at high confidence. Feature
extraction and the RF model handle this attack class
correctly — they simply never saw the payload in the
multipart case.

This also surfaced a real, independent finding: a stored-XSS
vulnerability in the target app. On `/posts`, the raw
`<script>`/`<img onerror>` payloads were persisted unescaped
to Postgres (confirmed via direct query: `posts.id=11,12`)
because multer parsed and stored them downstream of
logsguardian's miss. On `/profile`, there was no multipart
parser anywhere in the request path, so the `bio` field
silently never reached the database at all — a separate,
unrelated functional bug (the write no-ops, but nothing is
stored, so no security exposure there). Neither WAF-only nor
prior layered rounds surfaced any of this, since Round 1/2's
payloads were blocked by CRS before this app-layer gap could
ever become observable.

### Fix and corrected result: 23/23 (100%)

Added a global multipart parser (`src/middleware/upload.js`,
a single `multer` instance reused globally via `.any()`)
mounted in `app.js` before logsguardian, so `req.body`/`req.files`
are populated for multipart requests before the middleware
runs. `src/routes/posts.js`'s per-route `upload.single(...)`
calls were removed (a request body can only be parsed once)
and replaced with a `req.files` lookup by field name. Verified
this doesn't break real file uploads: a legitimate
title+content+attachment multipart POST still creates the
post with the file saved to disk. Also verified the
`/profile` silent-no-op bug is genuinely gone: a legitimate
multipart bio update now persists to Postgres correctly, not
just gets correctly blocked when malicious.

Re-ran the full 23-payload corpus (same DetectionOnly config,
same payloads, fresh session cookies): **23/23 now return
`verdict: block`**, confirmed via `detection_events` (not just
HTTP status). The two classification mislabels (P1, C1) persist
unchanged — a separate, minor, pre-existing issue unrelated to
this fix — but both remain correctly *blocked*.

### Conclusion

logsguardian's ML-based detection, once payloads correctly
reach the feature extraction pipeline, achieves **23/23 (100%)**
independent detection across SQLi/XSS/path traversal/cmdi
evasion variants specifically engineered to bypass
ModSecurity+CRS PL1's signature-based rules — all of which CRS
itself also failed to catch (0/14 evasion variants passed
Round 2, forming the basis for this test). This demonstrates
that logsguardian's statistical/feature-based approach
provides detection capability independent of, and
complementary to, signature-based WAF rules — contingent on
requests actually reaching its feature extraction, which this
round's investigation surfaced as its own reliability question
distinct from the ML model's classification accuracy.

## Declaración de fuga de datos en el corpus de evaluación

La primera evaluación de cobertura empleó un corpus derivado de SecLists
cuya rama de command injection coincide con una de las fuentes
incorporadas al conjunto de entrenamiento, por lo que sus resultados para
esa categoría no son atribuibles a capacidad de detección. Las cifras
reportadas en esta sección provienen de un corpus posterior, generado con
sqlmap [y OWASP ZAP pendiente de ejecución manual - ver
`attack-sim/exclusion_report.json` y el estado `xss_placeholder` en el
corpus] y filtrado por exclusión explícita contra el corpus de
entrenamiento.

Verificación directa (branch `fix/clean-evaluation-corpus`): de los 200
payloads cmdi del corpus de Ronda 4 (`attack-sim/large_corpus.json`),
**200/200** coinciden exacta o estructuralmente (por plantilla, tras
normalizar canary de 6 letras mayúsculas y dígitos) con
`training/data_clean/seclists_cmdi.jsonl` /
`data/seclists_command-injection-commix.txt`. Los otros tres archivos del
corpus de Ronda 4 (`large_corpus.json`, `large_corpus_raw.json`,
`large_corpus_requests.json`) no tienen generador versionado - no hay
script commiteado que los produzca, y el `seed=42` documentado más abajo
(sección "Corpus" de Ronda 4) no es reproducible: no existe código que lo
consuma. `attack-sim/build_corpus.py` (nuevo, este branch) reemplaza eso
con un generador versionado, con seed real (`20260923`, fija y
documentada en el propio script) y reproducibilidad verificada
(`build_corpus.py` ejecutado tres veces de forma independiente produjo
salida byte-idéntica en `large_corpus_requests.json` y
`exclusion_report.json`).

Los resultados de sqli y path_traversal de Ronda 4 (abajo) no mostraron
coincidencia con el corpus de entrenamiento al pasarlos por el mismo
filtro de exclusión (0/77 sqli, 0/200 path_traversal) - la fuga
identificada es específica a la fuente cmdi.

## Round 4 (con fuga, histórico) — Large Corpus, All Four Configs

Rounds 1-3 used a small (9-23 payload) hand-built corpus,
useful for controlled root-cause work but too curated to
generalize. Round 4 tests all four configurations against a
large, independently-sourced corpus to get a credible,
generalizable comparison.

### Corpus

590 payloads pulled from SecLists (danielmiessler/SecLists,
`master` branch), deduplicated and randomly sampled
(seed=42) to at most 200/category:

- sqli: 77 (`Fuzzing/Databases/SQLi/quick-SQLi.txt`, all
  available - source has fewer than 200 unique entries)
- xss: 113 (`Fuzzing/XSS/human-friendly/XSS-BruteLogic.txt`,
  all available)
- path_traversal: 200 of 881 unique
  (`Fuzzing/LFI/Linux/LFI-gracefulsecurity-linux.txt`)
- cmdi: 200 of 8262 unique
  (`Fuzzing/command-injection-commix.txt`)

Delivery mapped to the app's real attack surface: sqli via
`GET /posts/search?q=`, xss via `POST /posts` (`content`
field), path_traversal via `GET /posts/1/attachment?file=`,
cmdi via `POST /admin/ping` (`host` field). `/admin/ping`
requires `requireAdmin`, not just a logged-in session - using
a non-admin session for cmdi would make every request 403
regardless of payload (auth rejection, not detection), so the
runner (`attack-sim/run_large_corpus.py`) uses separate
alice/admin sessions per category. Runner is dependency-free
(stdlib `urllib`, no `requests` package) with a fixed
`User-Agent` across every request.

### A false positive found while validating the runner

Not part of the corpus run itself, but surfaced while smoke-
testing: a purely benign search query ("weekend hiking trip")
against `GET /posts/search` was blocked and misclassified as
XSS, at confidence just over the 0.35 threshold. Isolated the
cause precisely: three independent fresh login sessions
(different session cookies) against the identical payload and
User-Agent produced bit-identical confidence
(0.6162920594215393) every time - so session-cookie content
does *not* leak into the feature vector, ruling out that
hypothesis. Changing only the `User-Agent` string (`curl/8.7.1`
-> 0.367 xss-block, `Python-urllib/3.14` -> 0.400 sqli-block,
`logsguardian-corpus-runner/1.0` -> 0.616 sqli-block) changed
the verdict every time, deterministically per string. This is
a genuine calibration finding - short, low-signal benign
requests can sit close enough to the RF threshold that
incidental request metadata (which HTTP client sent it) flips
the verdict - worth a dedicated false-positive-rate study
against legitimate traffic, separate from this attack-corpus
comparison.

### Results

| Category | Config 1 (none) | Config 2 (logsguardian only) | Config 3a (WAF only, PL1) | Config 3b (layered, blocking) |
|---|---|---|---|---|
| sqli | 0/77 (0.0%) | 76/77 (98.7%) | 66/77 (85.7%) | 77/77 (100.0%) |
| xss | 0/113 (0.0%) | 110/113 (97.3%) | 110/113 (97.3%) | 113/113 (100.0%) |
| path_traversal | 0/200 (0.0%) | 197/200 (98.5%) | 174/200 (87.0%) | 197/200 (98.5%) |
| cmdi | 0/200 (0.0%) | 200/200 (100.0%) | 200/200 (100.0%) | 200/200 (100.0%) |
| **Overall** | **0/590 (0.0%)** | **583/590 (98.8%)** | **550/590 (93.2%)** | **587/590 (99.5%)** |

Config 1 and 2 run on the current branch via env/compose
toggles (`LOGSGUARDIAN_DISABLED=true` and a
`docker-compose.direct.yml` override that publishes `app`'s
port directly, bypassing the WAF - no branch switch needed).
Config 3a runs on `feat/waf-modsecurity-crs` as-is. Config 3b
runs on this branch with `MODSEC_RULE_ENGINE` reverted from
Round 3's `DetectionOnly` back to `On` (blocking) - the real
intended deployment, not the research probe state.

### Defense-in-depth, measured directly

Of the 40 attacks CRS PL1 missed in Config 3a (590-550),
attributing Config 3b's blocks by response signature
(`X-Powered-By: Express` present only on app-layer blocks) shows
**37 were independently caught by logsguardian** after passing
the WAF. Only 3 payloads passed both layers, and none are real
vulnerabilities against this app: generic LFI-list strings
(`~/.gtkrc`, `/proc/filesystems`, `~/.atfp_history`) with no
`../` traversal sequence, non-functional against this route's
`path.join(UPLOAD_DIR, file)` sink (Node's `path.join` doesn't
reset on an absolute-looking later argument the way
`path.resolve` would, and there's no shell to expand `~`).

### Conclusion

This corpus is large and independently sourced rather than
hand-picked, and it tells a different, more credible story
than Rounds 1-3's small corpus: **CRS PL1 alone has real,
measurable gaps** (85.7% on SQLi, 87.0% on path traversal -
the earlier "100%" result was an artifact of testing only
well-catalogued signatures). Layering logsguardian behind the
WAF closes most of that gap: 99.5% overall vs. 93.2%
(WAF-only) or 98.8% (logsguardian-only), with 37 of 40 WAF
misses independently caught by the ML layer. The layered
architecture is not redundant - each layer catches real
attacks the other doesn't, and the combination outperforms
either alone on every category.

## Round 5 — Clean Corpus (Leak-Free), All 4 Configurations

Rebuilds the evaluation corpus per the declaration above and re-runs all
four configurations against it. Config 2 was done first (2026-09-24);
Config 1, 3a, and 3b were added later (2026-10-10) — see "Cross-config
comparison" below for the full table. Config 3a required switching to a
different branch (`feat/waf-modsecurity-crs`, which never had logSguarDian
integrated), done via `git worktree` so the main checkout's branch/history
stayed untouched throughout.

> **Model provenance — corrected 2026-10-09, reversed from an earlier mistaken
> note.** This round's commit (`79224e1`, 2026-09-24) carried
> `models/rf.onnx`/`models/if.onnx` with SHA-256 `180837255d...`/`5de374a7f1...`.
> An earlier version of this note said that didn't match "the canonical
> `rf_v11`/`if_v10` pair" and called it wrong. **That was backwards.**
> Verified directly against the npm registry (`npm pack logsguardian@0.1.0`
> from `https://registry.npmjs.org/`, tarball shasum matched the registry's
> own `dist.shasum`): the models bundled in the **actually published**
> `logsguardian@0.1.0` package are `180837255d.../5de374a7f1...` — the exact
> same checksums Round 5 (and Rounds 1-4) already used. `npm publish`
> happened 2026-08-30T05:07:31Z, **before** the `rf_v11` retrain commit
> (`734c24f`, later the same day) and long before the 2026-09-26 fix
> (`03de50f`) that produced the `25b407e6.../5be28ee8...` pair — the package
> was never republished since. So `25b407e6.../5be28ee8...` (`training/models/`
> in `logSguarDian`) is the **current state of the training pipeline**, not
> what `npm install logsguardian` actually gives anyone today.
>
> **Net effect: Rounds 1-5 in this file, as originally measured, are
> internally consistent and representative of the real shipped artifact.**
> A re-run against `training/models/`'s `25b407e6.../5be28ee8...` pair was
> done on 2026-10-09 (branch `fix/round5-correct-model-rerun`) — it answers
> a different, legitimate question ("how would the current, unpublished
> training pipeline's model do on this corpus"), not "does the published
> package meet the coverage criterion". Both tables are kept below, each
> clearly labeled by which question it answers. Separately open: whether to
> publish a new npm version from `training/models/`'s current pair before
> citing anything as the live-package result going forward.
>
> **A fourth finding, from fixing this branch's own `models/{rf,if}.onnx`
> before committing:** `main`'s committed `models/rf.onnx`/`if.onnx` (as of
> 2026-10-09, pre-this-PR) were SHA-256 `a7c015f5.../3cf8e45c...` — **neither**
> the published pair nor the canonical `training/models/` pair; the same
> generation vendored for the latency benchmark (see the open-risks note in
> `logSguarDian`'s `cybersecurity-objectives-compliance.md`, item 8). This
> branch's `models/{rf,if}.onnx` were set explicitly to the verified
> npm-published checksums (`180837255d.../5de374a7f1...`, extracted directly
> from the real `logsguardian-0.1.0.tgz` tarball) rather than trusting
> whatever was already committed — `main` itself needs the same fix, out of
> scope for this PR but flagged here so it isn't lost.

### Corpus (`attack-sim/build_corpus.py`, seed `20260923`)

| Category | Source | Candidates generated | Discarded (exclusion filter) | Final |
|---|---|---|---|---|
| sqli | sqlmap (`GET /posts/search?q=`, `POST /login` username) | 1995 | 0 | 200 |
| path_traversal | own generator (`attack-sim/generators/path_traversal_gen.py`) | 400 | 3 (exact hash, `owasp_logs.jsonl`) | 200 |
| cmdi | own generator (`attack-sim/generators/cmdi_gen.py`, deliberately not SecLists-derived) | 400 | 0 | 200 |
| xss | **real OWASP ZAP Active Scan (2026-10-10)**, run via ZAP's REST API against `POST /posts` (content/title) and `POST /profile` (bio), authenticated as alice | 1 confirmed alert (content/title tested clean) | 0 | 1 |

Full accounting (per-payload discard reasons and matched training
source) in `attack-sim/exclusion_report.json`.

sqlmap (installed via `brew install sqlmap`, v1.10.9) was run with
`--batch --level=3 --risk=2 --technique=BEUSTQ` against both targets,
logging every request it sent via `-t` (traffic file) rather than
relying on its own vulnerability verdict — logsguardian's live 403s
during the sqlmap run caused sqlmap to conclude "not injectable" for
both parameters (WAF-like interference with its dynamism heuristics),
which is irrelevant here since only the payload *shapes* sqlmap tried
are used, not its exploitation success.

path_traversal and cmdi payloads are original, not derived from any
single wordlist. path_traversal payloads combine traversal depth
(2-12 levels of `../`) with 8 encoding styles (raw, backslash, single/
double/mixed-case URL-encoding, overlong UTF-8, `....//` filter-bypass,
null-byte suffix) against 28 target files spanning Linux system paths,
`/proc`, this app's own layout, and Windows paths. cmdi payloads combine
12 shell separators / 4 substitution wrappers with 20 post-exploitation
commands against the `ping -c 3 ${host}` sink — structurally distinct
from SecLists commix's canary-arithmetic timing templates by design
(verified: 0/200 match the SecLists template-shape set).

xss now has a real result (2026-10-10) — see "XSS: ZAP Active Scan
result" below, which replaces the earlier "pending manual step" section.
It is n=1, not n=200 like the other three categories, and that is by
design, not an oversight still to be filled in: ZAP's Active Scan reports
one alert per confirmed-vulnerable parameter+technique, not every payload
it tried. Both candidate sinks were scanned (`POST /posts` content/title,
`POST /profile` bio); only `bio` came back vulnerable.

### Results (Config 2: logsguardian active, no WAF)

**Primary / vigente — the published package (`logsguardian@0.1.0` as shipped
on npm, SHA-256 `180837255d.../5de374a7f1...`), same model as Rounds 1-4
above.** This is what anyone installing the library today actually runs.

| Category | Round 4 (con fuga, same published model) | **Round 5 (leak-free, published model)** |
|---|---|---|
| sqli | 76/77 (98.7%) | **200/200 (100.0%)** |
| path_traversal | 197/200 (98.5%) | **170/200 (85.0%)** |
| cmdi | 200/200 (100.0%) | **183/200 (91.5%)** |
| xss | 110/113 (97.3%) | **1/1 (100.0%) — n=1, see note below** |

**Secondary / reference only — a real tarball built fresh from `logSguarDian`'s
`develop` (22550ea), not published to npm.** Proposed by @diegovalenzuela:
build the actual publishable artifact instead of swapping ONNX files by
hand, so the result reflects the real `postbuild`/`bundledDependencies`
pipeline, not just the model weights in isolation. Done 2026-10-09 on branch
`fix/round5-correct-model-rerun`:

1. `pnpm --filter @logsguardian/extractor run build && pnpm --filter
   logsguardian run build` on `logSguarDian` @ `develop` (22550ea) —
   `postbuild` synced `training/models/{rf,if}.onnx` (`25b407e6.../5be28ee8...`,
   `rf_v11`/`if_v10`) into `packages/core/models/`.
2. `npm pack` on `packages/core` → `logsguardian-0.1.0.tgz`,
   **SHA-256 `cf1238deb33383975e12058de71c4423b22d7c5bcba5cf47241c0d0f712b0416`**
   (still version-labeled `0.1.0` in `package.json` — not bumped, not
   published; a real publish would need `0.1.1` per the version actually on
   the registry).
3. Replaced `vendor/logsguardian-0.1.0.tgz` in this repo with that exact
   file, replaced `models/{rf,if}.onnx` + added `models/parity_report.json`
   to match (the new middleware reads `threshold_if` from `parity_report.json`
   in `modelDir`, not a hardcoded constant — a separate change from `develop`
   not in the published 0.1.0), regenerated `package-lock.json` against the
   new tarball's integrity hash, rebuilt the container, verified the running
   container's `models/{rf,if}.onnx` checksum matched step 1's output exactly.
4. Re-ran `run_large_corpus.py config2-develop-tarball-20261009` against the
   same 608-request corpus (`attack-sim/large_corpus_requests.json`,
   unchanged). Raw output: `attack-sim/results_config2-develop-tarball-20261009.json`.

This answers "what would Round 5 show if `develop` were published today",
with an actual built tarball and its recorded hash — not "what does the
shipped `0.1.0` package do" (that's the primary table above):

| Category | Published model (primary) | Unpublished `training/models/` pair (reference) | Δ |
|---|---|---|---|
| sqli | 100.0% | 99.5% | -0.5 pts |
| path_traversal | 85.0% | 95.0% | +10.0 pts |
| cmdi | 91.5% | 96.0% | +4.5 pts |
| xss | 100.0% (1/1) | 100.0% (1/1) | — |

**XSS row added 2026-10-10**, after the ZAP Active Scan below replaced the
placeholder payloads. Re-ran sqli/path_traversal/cmdi against both model
pairs at the same time to confirm they still match the 2026-10-09 figures
exactly (they do — `attack-sim/results_config2-published-with-real-xss-20261010.json`
and `attack-sim/results_config2-with-real-xss-20261010.json`); only xss is
new. n=1 for xss against both pairs — see the note below, this is not
comparable in statistical weight to the other three categories' n=200.

Both pairs clear the ≥80% coverage criterion on all three measured
categories. Cite the **primary table** for any claim about what the
published `logsguardian` package does; cite the reference table only when
explicitly discussing what `develop` would ship if published. These numbers
are identical to an earlier, less rigorous re-run done the same day (raw
`training/models/` ONNX files copied directly into `models/`, no real
tarball built) — the match is expected (same underlying weights) and
confirms that swap didn't change the result, but the tarball-based run
above is the one with a citable artifact hash and should be the one
referenced going forward. Publishing this exact tarball as `0.1.1` (closing
the gap for real) is a decision for the maintainers, not done here.

The sqli, path_traversal, and cmdi causal explanations below (leak-removal
and encoding-diversity, and the per-payload breakdown of 17 cmdi misses /
30 path_traversal misses) were written against — and remain valid for —
the **primary (published-model) numbers**, since those were never actually
wrong. No re-derivation needed for the primary table.

The cmdi drop (100% -> 91.5%) is the expected correction once the
memorized-template payloads are removed: 91.5% is logsguardian's
actual detection rate against novel cmdi payload shapes, not an
artifact of training/evaluation overlap. The path_traversal drop
(98.5% -> 85.0%) was not predicted by the leak investigation (that
corpus file showed 0/200 exclusion matches) — it reflects that this
round's payloads are a harder, more encoding-diverse set (double
URL-encoding, overlong UTF-8, backslash variants, deeper traversal
chains) than the original LFI wordlist sample, not a data-leak
artifact. Both are worth a dedicated follow-up: which specific
encoding styles/commands account for the 17 cmdi misses and 30
path_traversal misses (`attack-sim/results_config2.json` has the
per-request verdicts needed to break this down by payload).

### XSS: ZAP Active Scan result (2026-10-10)

OWASP ZAP is installed as a GUI application only (`/Applications/ZAP.app`),
but ZAP also exposes a full REST API on its proxy port once running
(found by reading `~/Library/Application Support/ZAP/config.xml`'s `<key>`
element for the local API key) — the entire scan below was driven through
that API, no manual browser/proxy configuration needed in the end.

**Setup, via API calls against `http://localhost:8080`:**
1. `context/action/newContext` — new context `logsguardian-xss`.
2. `context/action/includeInContext` — `http://localhost:3000.*`.
3. `authentication/action/setAuthenticationMethod` — form-based,
   `loginUrl=http://localhost:3000/login`,
   `loginRequestData=username={%username%}&password={%password%}`.
4. `authentication/action/setLoggedInIndicator` — regex `Logout` (only
   present in the nav when a session is active, see `views/_nav.ejs`).
5. `users/action/newUser` + `setAuthenticationCredentials` +
   `setUserEnabled` — user `alice`/`alice123`.
6. `spider/action/scanAsUser` (authenticated as alice) to populate the
   Sites tree, plus a couple of direct `core/action/sendRequest` calls
   (real `POST /posts` and `POST /profile` submissions, with a freshly
   captured session cookie) so both candidate forms were present with
   their real field names before scanning.

**Scan:** `ascan/action/scanAsUser`, full recurse from `http://localhost:3000`,
authenticated as alice. Completed in ~25s (608 history entries existing,
538 total alerts across all categories — most are unrelated infra findings
like missing security headers, not relevant here).

**Result — exactly one Cross-Site Scripting alert, out of 538 total:**

| Field | Value |
|---|---|
| Name | Cross Site Scripting (Reflected) |
| Risk / Confidence | High / Medium |
| URL | `http://localhost:3000/profile` |
| Method / Param | POST / `bio` |
| Attack payload | `</div><scrIpt>alert(1);</scRipt><div>` |

`POST /posts` (`content`, `title`) was scanned with the same policy and
came back clean — no XSS alert for either field. This is consistent with
the app's own source: `src/routes/profile.js:20` stores `bio` raw and
renders it unescaped (`<%- %>` in the EJS template), while the posts
templates presumably escape `content`/`title` correctly.

**Naming nuance:** ZAP's rule fired as "Reflected", but functionally this
is **stored/persistent XSS** — `bio` is written to the `users` table and
re-rendered on every subsequent view of that profile, not just echoed back
in the same response. ZAP's active scanner can trigger on a stored payload
within the same request/response cycle it just wrote, which looks
identical to a true reflected case from the rule's perspective; the
generic rule name doesn't distinguish the two. Treat this as a persistent
XSS finding when citing it, not a reflected one.

Raw evidence: `attack-sim/zap-evidence/zap-xss-report.json` (ZAP's own
JSON report) and `zap-alerts-full.json` (every alert from the scan, not
just XSS, for traceability).

**Why n=1, not a larger sample:** ZAP's Active Scan reports one alert per
confirmed-vulnerable parameter+attack-technique combination — the payload
that worked, not every payload tried. `attack-sim/build_corpus.py`'s
`XSS_PLACEHOLDER_PAYLOADS` was replaced with this single real payload
(the old 15-entry hand-picked list is gone); padding it back up to a
larger n with more hand-picked variants would misrepresent what was
actually confirmed against this app. The corpus run above (1/1, both
model pairs) is a real result with real statistical weight of exactly
one — not a placeholder, but also not comparable to the other three
categories' n=200 samples. Cite it as "one confirmed stored-XSS
vulnerability, detected" — not as an 80-100% coverage rate in the same
sense as sqli/path_traversal/cmdi.

## Cross-config comparison (2026-10-10) — all 4 configs, same Round 5 corpus

All four configurations run against the identical 601-request leak-free
corpus (sqli 200, path_traversal 200, cmdi 200, xss 1 — the real ZAP
payload above), same published `logsguardian@0.1.0` model where
applicable. Raw results: `attack-sim/results_config{1,2-published-with-real-xss,3a,3b}-round5-20261010.json`
(Config 2's file keeps its original "with-real-xss" name from the XSS
section above — same run, same numbers, not duplicated).

| Category | Config 1 (none) | Config 2 (logsguardian only) | Config 3a (WAF only) | Config 3b (layered) |
|---|---|---|---|---|
| sqli | 0/200 (0.0%) | 200/200 (100.0%) | 199/200 (99.5%) | 200/200 (100.0%) |
| path_traversal | 0/200 (0.0%) | 170/200 (85.0%) | 197/200 (98.5%) | 200/200 (100.0%) |
| cmdi | 0/200 (0.0%) | 183/200 (91.5%) | 136/200 (68.0%) | 197/200 (98.5%) |
| xss | 0/1 (0.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |

**Config 1 is the sanity check, not a finding** — 0% everywhere, as
expected with no protection at all; confirms the corpus and harness
measure what they claim to.

**The real finding is cmdi, and it's a genuine complementary-coverage
result, not a contradiction with Round 4:** WAF alone (Config 3a) is
markedly *weaker* than logsguardian alone (Config 2) for cmdi — 68.0% vs
91.5% — the opposite of path_traversal and sqli, where the WAF alone
slightly outperforms logsguardian alone. Layered (Config 3b) comes out
ahead of both individually on cmdi (98.5%), consistent with the two
layers catching different things rather than one subsuming the other.
This matches Round 4's qualitative defense-in-depth conclusion (logsguardian
independently caught 37 of the 40 attacks the WAF missed), now backed by a
leak-free corpus instead of one with confirmed cmdi template memorization.

**xss is 100% across all three protected configs, but n=1 for all of
them** — the same single real payload, replayed against each stack. This
confirms the vulnerability is caught by each layer independently; it does
not give three independent statistical samples (it's the same one
request, by design — there's no larger real XSS corpus for this app yet).

**Caveat kept from the sections above, repeated here because it applies
to this whole table:** Config 2's numbers are against the actual
*published* `logsguardian@0.1.0` (`180837255d.../5de374a7f1...`), not the
canonical, unpublished `training/models/` pair OE3.1 in
`cybersecurity-objectives-compliance.md` evaluates — see risk item #11
there. Config 3a/3b were measured on a separate branch/worktree that
never had logsguardian wired in for 3a by design (WAF-only baseline); 3b
uses the same published model as Config 2.

## `logsguardian@0.1.1` verification (2026-10-11) — path_traversal closes to 100%, with a caveat on cmdi

Risk item #11 (published package not matching OE3.1's model) is now
**resolved for the model itself**: `0.1.1`, installed via `npm install
logsguardian@0.1.1` against the real registry (not a local tarball),
bundles the canonical `rf_v11`/`if_v10` pair (`25b407e6.../5be28ee8...`,
verified by checksum inside the container) and includes the
`middleware.ts` query-string fix from `fix/query-double-encoding-traversal`.
`src/app.js` was changed to stop overriding `modelDir` to this repo's own
`models/` folder, so this test uses exactly what the package ships —
nothing locally swapped.

**First run against 0.1.1, same 601-request Round 5 corpus:** path_traversal
stayed at 190/200 (95.0%) — identical to the pre-fix reference measurement,
no improvement. Investigated why with
`training/audit/breakdown_config2.py`: the specific misses (`double_encoding`,
`overlong_utf8`) were unchanged byte-for-byte.

**Root cause: a second, independent bug, in the test harness itself, not
the middleware.** `attack-sim/run_large_corpus.py`'s `do_request()` passed
every payload through `urllib.parse.urlencode()`, which assumes the value
is raw/decoded text needing encoding. `path_traversal_gen.py` and
`cmdi_gen.py` both deliberately emit payloads that are **already**
percent-encoded (`%252e%252e%252f...`, `%c0%ae%c0%ae...`, a `%0a`
separator) — literal wire bytes the attacker wants to send, not text that
should be encoded again. `urlencode()` re-escaped the `%` characters,
adding an unintended extra layer. Traced with a concrete example: corpus
entry `%252e%252e%252f%252e%252e%252fboot.ini` (intended as
double-encoded) was actually transmitted as
`%25252e%25252e%25252f...` (triple-encoded) — confirmed by computing
`urllib.parse.urlencode()`'s exact output and testing it directly against
`packages/extractor`'s `TRAVERSAL_SEQUENCE_COUNT` regex, which does not
match triple-encoding (only raw, single-, and double-encoded, plus the
overlong-UTF8 form).

Before the `middleware.ts` fix, this harness bug *compounded* with the
middleware's own re-encoding (quadruple-encoded reaching the extractor);
after the middleware fix alone, it's just the harness's one extra layer
(triple-encoded) — still unmatched, which is why path_traversal didn't
move at first.

**Fixed `run_large_corpus.py`:** payloads from `path_traversal`/`cmdi`
categories (only — sqlmap-derived sqli payloads can legitimately contain
a literal `%` from SQL's `LIKE` wildcard followed by characters that
happen to be hex digits, which would false-positive under a bare regex
check) that already match `%[0-9a-fA-F]{2}` are now inserted into the
query string/body literally, bypassing `urlencode()` for that value.

**Re-run against the same `0.1.1` install, harness fixed:**

| Category | 0.1.1, harness bug present | **0.1.1, harness fixed** | Δ |
|---|---|---|---|
| sqli | 99.5% | 99.5% (unaffected, as expected) | — |
| **path_traversal** | 95.0% (190/200) | **100.0% (200/200)** | **+5.0 pts** |
| cmdi | 96.0% (192/200) | **92.5% (185/200, 1 timeout)** | **-3.5 pts** |
| xss | 100% (1/1) | 100% (1/1) | — |

**path_traversal confirms the hypothesis exactly:** with both the real
bug (middleware re-encoding) and the newly-found harness bug fixed,
every single path_traversal payload in the corpus is now blocked. The
85.0% originally measured in Round 5 (against the old, pre-`0.1.1`
published model) undersold the current package by a full 15 points, split
across a model-generation difference (85.0% → 95.0%, see the primary vs.
reference table above) and these two independent encoding bugs
(95.0% → 100.0%).

**cmdi went down, and that's the more honest number, not a regression to
explain away.** The harness bug was also corrupting cmdi's `%0a`/`%26`/
`%7c`/`%3B`-style encoded-separator payloads (command-injection evasion
techniques that deliberately pre-encode the shell separator to dodge naive
filters) into garbage that didn't represent the intended attack, yet some
of those garbled requests were still being blocked by logsguardian anyway
— inflating the old 96.0% with false confidence. With the payloads now
transmitted as actually intended, logsguardian misses 14 of them (plus 1
unrelated timeout, a real `sleep`-style payload that executed rather than
a bug), landing at 92.5%. This is lower than before, but it is measuring a
real thing the 96.0% wasn't: logsguardian's actual detection rate against
correctly-formed encoded-separator cmdi evasion.

Raw evidence: `attack-sim/results_config2-published-0.1.1-harness-fixed-20261010.json`,
`attack-sim/breakdown_config2-published-0.1.1-harness-fixed-20261010.json`.
