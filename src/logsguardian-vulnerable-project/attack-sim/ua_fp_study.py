#!/usr/bin/env python3
"""User-Agent false-positive study.

Precedent (docs/config3b-results.md, "A false positive found while
validating the runner"): a benign search query got blocked, and switching
ONLY the User-Agent string flipped the verdict deterministically. All prior
FP evidence (attack-sim/run_large_corpus.py, the "0 FP / 10,800 benign
requests" Artillery baseline) used a single fixed User-Agent on every
request, so it never exercised this axis.

This script drives GET /login (no session), GET /posts (with session), and
GET /profile (with session) - all with no query string and no body, i.e.
all request signal comes from headers/structure - against 5 real browser
User-Agent strings, and records the verdict logsguardian's SQLite event log
produced for each one.

Usage: python3 attack-sim/ua_fp_study.py [--base-url http://localhost:3000]

The app must already be running (docker compose ... up -d app db) and its
event DB must be reachable to read back verdicts. Since this script itself
has no DB access (it only speaks HTTP to the app), it relies on the app's
own JSON response to tell block vs pass (HTTP 403 body from logsguardian's
'block' mode vs the normal 200 page) - it does NOT attempt to read
predicted_class/confidence, which are pulled separately via
`docker compose exec app node -e "..."` against better-sqlite3, since this
container has no host-exposed DB port. Results here record only status code
+ blocked boolean; see ua_fp_study_results.json 'db_events' for
predicted_class/confidence, merged in by the caller after running this
script.
"""
import http.cookiejar
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "http://localhost:3000"
if "--base-url" in sys.argv:
    BASE_URL = sys.argv[sys.argv.index("--base-url") + 1]

USER_AGENTS = {
    "chrome_macos": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "firefox_macos": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:131.0) Gecko/20100101 Firefox/131.0",
    "safari_macos": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15",
    "chrome_windows": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "mobile_safari_ios": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Mobile/15E148 Safari/604.1",
}

ROUTES_NO_SESSION = ["/login"]
ROUTES_WITH_SESSION = ["/posts", "/profile"]


def make_opener():
    jar = http.cookiejar.CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))


def get(opener, path, ua):
    req = urllib.request.Request(BASE_URL + path, method="GET")
    req.add_header("User-Agent", ua)
    try:
        resp = opener.open(req, timeout=10)
        return resp.getcode()
    except urllib.error.HTTPError as e:
        return e.code


def login(opener, ua, username="alice", password="alice123"):
    data = urllib.parse.urlencode({"username": username, "password": password}).encode()
    req = urllib.request.Request(BASE_URL + "/login", data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("User-Agent", ua)
    try:
        resp = opener.open(req, timeout=10)
        return resp.getcode()
    except urllib.error.HTTPError as e:
        return e.code


def main():
    results = []
    for ua_label, ua_string in USER_AGENTS.items():
        # GET /login - fresh opener, no session, matches how a real browser
        # hits the app on first visit (app.js redirects '/' -> '/login').
        opener_anon = make_opener()
        for route in ROUTES_NO_SESSION:
            status = get(opener_anon, route, ua_string)
            results.append({
                "ua_label": ua_label,
                "user_agent": ua_string,
                "route": route,
                "session": False,
                "http_status": status,
                "blocked": status == 403,
            })
            print(f"[{ua_label}] GET {route} (no session) -> {status}")

        # Fresh session per UA (mirrors the precedent's isolation of session
        # content as a non-factor - each UA gets its own login).
        opener_session = make_opener()
        login_status = login(opener_session, ua_string)
        if login_status not in (200, 302):
            print(f"  WARNING: login failed for {ua_label}, status={login_status}", file=sys.stderr)
        for route in ROUTES_WITH_SESSION:
            status = get(opener_session, route, ua_string)
            results.append({
                "ua_label": ua_label,
                "user_agent": ua_string,
                "route": route,
                "session": True,
                "http_status": status,
                "blocked": status == 403,
            })
            print(f"[{ua_label}] GET {route} (session) -> {status}")

    out_path = "attack-sim/ua_fp_study_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    blocked_count = sum(1 for r in results if r["blocked"])
    print(f"\n{blocked_count}/{len(results)} combinations blocked. Written to {out_path}")


if __name__ == "__main__":
    main()
