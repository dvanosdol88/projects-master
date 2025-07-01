"""
Combined file-poller + Flask API.
Run:  python jules_with_api.py
"""
import threading, time, json, datetime
from pathlib import Path
from flask import Flask, request, jsonify

BASE = Path(__file__).parent
SHARED = BASE / "shared"
INBOX  = SHARED / "claude-to-jules-message.md"
OUTBOX = SHARED / "jules-to-cc.md"
TASKS  = SHARED / "tasks.json"
SHARED.mkdir(parents=True, exist_ok=True)

# ─── Flask API ────────────────────────────────────────────────────────────
app = Flask(__name__)

def _now():
    return datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"

@app.route("/health")
def health():
    return {"status": "ok", "server_time": _now()}

@app.route("/add_task", methods=["POST"])
def add_task():
    data = request.get_json(force=True)
    task = data.get("task", "").strip()
    if not task:
        return {"error": "task field required"}, 400
    tasks = json.loads(TASKS.read_text()) if TASKS.exists() else []
    tasks.append({"task": task, "created": _now()})
    TASKS.write_text(json.dumps(tasks, indent=2))
    return {"message": "queued", "total_tasks": len(tasks)}, 201

@app.route("/tasks")
def list_tasks():
    tasks = json.loads(TASKS.read_text()) if TASKS.exists() else []
    return jsonify(tasks)

def run_api():
    app.run(host="0.0.0.0", port=5000)

# ─── Markdown poller ─────────────────────────────────────────────────────
def poll_loop():
    while True:
        if INBOX.exists() and INBOX.stat().st_size:
            content = INBOX.read_text().strip()
            timestamp = _now()
            mode = "a" if OUTBOX.exists() else "w"
            with OUTBOX.open(mode) as f:
                f.write(f"{timestamp} - Received: {content}\n")
            INBOX.write_text("")
            print(f"Handled: {content}", flush=True)
        time.sleep(2)

# ─── Main ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    threading.Thread(target=run_api, daemon=True).start()
    print("API_STARTED", flush=True)
    poll_loop()
