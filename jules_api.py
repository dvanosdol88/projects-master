import datetime
import json

from flask import Flask, jsonify, request
from infra.redis_client import client

app = Flask(__name__)

STREAM = "a2a_stream"


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

    client.xadd(STREAM, {"task": task, "created": _now()})
    return {"message": f"queued {task!r}"}, 201


@app.route("/tasks")
def list_tasks():
    entries = client.xrange(STREAM)
    tasks = [
        {
            "id": entry_id.decode(),
            "task": fields.get(b"task", b"").decode(),
            "created": fields.get(b"created", b"").decode(),
        }
        for entry_id, fields in entries
    ]
    return jsonify(tasks)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
