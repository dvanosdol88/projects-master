import os
import signal
import socket
import subprocess
import sys
import time
from contextlib import contextmanager

import urllib.request
import json


def get_free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def wait_for_server(
    url: str, timeout: float = 10, initial_delay: float = 0.1, max_delay: float = 1.0
) -> None:
    delay = initial_delay
    start = time.monotonic()
    while True:
        try:
            with urllib.request.urlopen(url) as resp:
                if resp.status == 200:
                    return
        except Exception:
            pass
        if time.monotonic() - start > timeout:
            raise RuntimeError(f"server not available at {url}")
        time.sleep(delay)
        delay = min(delay * 2, max_delay)


@contextmanager
def jules_server(redis_db: int = 15):
    port = get_free_port()
    env = {**os.environ, "A2A_JULES_PORT": str(port), "REDIS_DB": str(redis_db)}
    proc = subprocess.Popen(
        [sys.executable, "api/jules_server.py"],
        env=env,
        preexec_fn=os.setsid if os.name != "nt" else None,
    )
    try:
        wait_for_server(f"http://127.0.0.1:{port}/health")
        yield port
    finally:
        if os.name == "nt":
            proc.terminate()
        else:
            os.killpg(os.getpgid(proc.pid), signal.SIGINT)
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
