import datetime
import json
from pathlib import Path

from flask import Flask, jsonify, request

app = Flask(__name__)
BASE = Path(__file__).parent
(BASE / "shared").mkdir(exist_ok=True)
TASKS_FILE = BASE / "shared" / "tasks.json"


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

    tasks = json.loads(TASKS_FILE.read_text()) if TASKS_FILE.exists() else []
    tasks.append({"task": task, "created": _now()})
    TASKS_FILE.write_text(json.dumps(tasks, indent=2))
    return {"message": f"queued {task!r}", "total_tasks": len(tasks)}, 201


@app.route("/tasks")
def list_tasks():
    tasks = json.loads(TASKS_FILE.read_text()) if TASKS_FILE.exists() else []
    return jsonify(tasks)


if __name__ == "__main__":
    import os

    port = int(os.environ.get("A2A_JULES_PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
