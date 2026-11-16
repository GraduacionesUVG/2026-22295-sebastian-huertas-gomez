"""Standalone raw-bytes capture server, used only by test_harness_encoding.py.

Listens on a local port and records exactly what arrives on the wire for
each request: the raw request path+query string as Python's http.server
exposes it (text copy of the request line, no decoding applied), and the
raw body bytes for POST. It never forwards to the real app and never
parses the payload - the point is to see what the harness actually put on
the wire, independent of how Express or logsguardian would later interpret
it.

Usage: python3 capture_server.py <port> <output_jsonl_path>
"""
from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer


class CaptureHandler(BaseHTTPRequestHandler):
    out_path = None

    def _record(self, method: str, raw_target: str, raw_body: str) -> None:
        with open(self.out_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "method": method,
                "raw_target": raw_target,
                "raw_body": raw_body,
            }) + "\n")

    def do_GET(self):
        self._record("GET", self.path, "")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"ok")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(length).decode("utf-8", errors="replace")
        self._record("POST", self.path, raw_body)
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"ok")

    def log_message(self, fmt, *args):
        pass


def main() -> None:
    port = int(sys.argv[1])
    out_path = sys.argv[2]
    CaptureHandler.out_path = out_path
    open(out_path, "w").close()
    server = HTTPServer(("127.0.0.1", port), CaptureHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
