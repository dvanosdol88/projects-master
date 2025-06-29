#!/usr/bin/env python3
"""Simple CLI to interact with Jules (part of JACK system).

Commands:
  add <task>   – add a task string
  list         – list queued tasks
  health       – check /health endpoint (expects 200)

Default base-URL = http://localhost:5000 (override with --url).
"""

import argparse
import json
import sys
import urllib.request
import urllib.error


def _post(url: str, payload: dict) -> str:
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as r:  # noqa: S310 (stdlib)
        return r.read().decode()


def _get(url: str) -> str:
    with urllib.request.urlopen(url) as r:  # noqa: S310
        return r.read().decode()


def main() -> None:
    p = argparse.ArgumentParser(prog="jack_cli")
    p.add_argument("command", choices=["add", "list", "health"])
    p.add_argument("message", nargs="?", help="task text for 'add'")
    p.add_argument(
        "--url",
        default="http://localhost:5000",
        help="Base Jules URL (default: %(default)s)",
    )
    a = p.parse_args()

    base = a.url.rstrip("/")
    try:
        if a.command == "add":
            if not a.message:
                p.error("'add' requires a task message")
            out = _post(f"{base}/add_task", {"task": a.message})
        elif a.command == "list":
            out = _get(f"{base}/tasks")
        else:  # health
            out = _get(f"{base}/health")
        print(out)
    except urllib.error.URLError as e:
        sys.exit(f"Request failed: {e}")


if __name__ == "__main__":
    main()
