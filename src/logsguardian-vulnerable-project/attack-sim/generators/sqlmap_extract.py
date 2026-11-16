"""Extracts candidate SQLi payloads from sqlmap traffic-log files (`-t`
option). sqlmap doesn't have a "dump payloads" mode, so the traffic file
(every raw HTTP request it sent) is the source of truth for what it tried.

Two traffic logs are expected, one per target in Table 14 of the protocol:
  - GET /posts/search?q=  -> attack-sim/sqlmap_out/traffic_search.txt
  - POST /login (username) -> attack-sim/sqlmap_out/traffic_login.txt

Only the payload actually placed in the targeted parameter is extracted
(the `q` query param for /posts/search, the `username` body param for
/login) - sqlmap also probes User-Agent/Referer/Cookie and injects
distractor extra query params (e.g. `&apca=...`) while testing, which are
not what we want as *the* candidate payload for that request spec.
"""
from __future__ import annotations

import re
import urllib.parse
from pathlib import Path

# Dynamism-probe / literal values sqlmap sends that carry no injection
# syntax (used to confirm the parameter is reflected/dynamic before trying
# real payloads). These are not attack payloads and are dropped.
_TRIVIAL_RE = re.compile(r"^[A-Za-z0-9_\-]{0,12}$")

# Heuristic: something that actually looks like an injection attempt -
# quotes, SQL keywords/operators, comment sequences, or boolean/UNION/time
# based syntax.
_SQLI_SIGNAL_RE = re.compile(
    r"""('|"|--|/\*|\bAND\b|\bOR\b|\bUNION\b|\bSELECT\b|\bSLEEP\b|\bBENCHMARK\b|
        \bWAITFOR\b|\bCASE\b|\bEXTRACTVALUE\b|\bCAST\b|\bCONVERT\b|
        information_schema|xp_cmdshell|\bEXEC\b|;|\bORDER\ BY\b|\bGROUP\ BY\b)""",
    re.IGNORECASE | re.VERBOSE,
)


def _is_attack_shaped(payload: str) -> bool:
    if not payload:
        return False
    if _TRIVIAL_RE.match(payload):
        return False
    return bool(_SQLI_SIGNAL_RE.search(payload))


def extract_search_q_payloads(traffic_file: Path) -> list[str]:
    """GET /posts/search?q=<payload>[&...] request lines."""
    payloads: list[str] = []
    seen: set[str] = set()
    line_re = re.compile(r"^GET /posts/search\?(\S+) HTTP/1\.1")
    with open(traffic_file, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            m = line_re.match(line)
            if not m:
                continue
            qs = urllib.parse.parse_qs(m.group(1), keep_blank_values=True)
            if "q" not in qs or not qs["q"]:
                continue
            payload = qs["q"][0]
            if not _is_attack_shaped(payload):
                continue
            if payload not in seen:
                seen.add(payload)
                payloads.append(payload)
    return payloads


def extract_login_username_payloads(traffic_file: Path) -> list[str]:
    """POST /login body: username=<payload>&password=... request lines.

    The traffic file interleaves request/response blocks; the body is the
    first blank-line-terminated line after the request headers for POST
    requests. We scan for lines shaped like `username=...&password=...`
    directly, which is simpler and robust to header-order changes.
    """
    payloads: list[str] = []
    seen: set[str] = set()
    body_re = re.compile(r"^username=([^&\n]*)&password=")
    with open(traffic_file, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            m = body_re.match(line)
            if not m:
                continue
            payload = urllib.parse.unquote_plus(m.group(1))
            if not _is_attack_shaped(payload):
                continue
            if payload not in seen:
                seen.add(payload)
                payloads.append(payload)
    return payloads


def extract_all(sqlmap_out_dir: Path) -> dict[str, list[str]]:
    search_file = sqlmap_out_dir / "traffic_search.txt"
    login_file = sqlmap_out_dir / "traffic_login.txt"
    result: dict[str, list[str]] = {"search_q": [], "login_username": []}
    if search_file.exists():
        result["search_q"] = extract_search_q_payloads(search_file)
    if login_file.exists():
        result["login_username"] = extract_login_username_payloads(login_file)
    return result


if __name__ == "__main__":
    out = extract_all(Path(__file__).parent.parent / "sqlmap_out")
    print(f"search_q: {len(out['search_q'])} candidates")
    for p in out["search_q"][:10]:
        print("  ", repr(p))
    print(f"login_username: {len(out['login_username'])} candidates")
    for p in out["login_username"][:10]:
        print("  ", repr(p))
