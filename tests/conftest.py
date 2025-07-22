import os
import signal
import subprocess
import sys

import pytest

from .utils import jules_server, wait_for_server, get_free_port


@pytest.fixture
def live_jules_server():
    with jules_server() as port:
        yield port


@pytest.fixture
def live_orchestrator():
    port = get_free_port()
    env = {**os.environ, "A2A_JULES_PORT": str(port), "A2A_TEST_MODE": "1"}
    proc = subprocess.Popen(
        [sys.executable, "orchestrator.py"],
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
