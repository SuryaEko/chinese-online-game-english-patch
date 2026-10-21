import http.server, urllib.parse


class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        t = q.get("text", [""])[0]
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(t.encode("utf-8"))

    def log_message(self, *a):
        pass


http.server.HTTPServer(("127.0.0.1", 8799), H).serve_forever()
