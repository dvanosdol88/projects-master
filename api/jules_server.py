import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

_tasks = []


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/health"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
        elif self.path.startswith("/tasks"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(_tasks).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path.startswith("/add_task"):
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode()
            try:
                data = json.loads(body)
                task = data.get("task", "").strip()
                if not task:
                    raise ValueError
            except Exception:
                self.send_response(400)
                self.end_headers()
                return
            _tasks.append({"task": task})
            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            resp = {"message": f"queued {task!r}", "total_tasks": len(_tasks)}
            self.wfile.write(json.dumps(resp).encode())
        else:
            self.send_response(404)
            self.end_headers()


def run():
    port = int(os.environ.get("A2A_JULES_PORT", "5000"))
    server = HTTPServer(("0.0.0.0", port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    run()
