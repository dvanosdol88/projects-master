import subprocess
import sys
import pathlib

CLI = pathlib.Path(__file__).parent.parent / "jack_cli.py"


import pytest


@pytest.mark.unit
def test_cli_help():
    """CLI should exit 0 when called with --help."""
    result = subprocess.run(
        [sys.executable, str(CLI), "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "usage" in result.stdout.lower()


@pytest.mark.integration
def test_jules_server_health(live_jules_server):
    import urllib.request

    url = f"http://127.0.0.1:{live_jules_server}/health"
    with urllib.request.urlopen(url) as resp:
        data = resp.read().decode()
    assert resp.status == 200


@pytest.mark.integration
def test_orchestrator_health(live_orchestrator):
    import urllib.request

    url = f"http://127.0.0.1:{live_orchestrator}/health"
    with urllib.request.urlopen(url) as resp:
        data = resp.read().decode()
    assert resp.status == 200
