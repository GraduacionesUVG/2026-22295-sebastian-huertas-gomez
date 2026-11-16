import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    out_path = None
    protocol_version = "HTTP/1.1"

    def _rec(self, raw_body):
        with open(self.out_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "method": self.command,
                "raw_target": self.path,
                "version": self.request_version,
                "headers": [[k, v] for k, v in self.headers.items()],
                "raw_body": raw_body,
            }) + "\n")

    def _ok(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", "2")
        self.end_headers()
        self.wfile.write(b"ok")

    def do_GET(self):
        self._rec("")
        self._ok()

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(n).decode("utf-8", errors="replace")
        self._rec(body)
        self._ok()

    def log_message(self, fmt, *args):
        pass


Handler.out_path = sys.argv[2]
open(sys.argv[2], "w").close()
HTTPServer(("0.0.0.0", int(sys.argv[1])), Handler).serve_forever()
