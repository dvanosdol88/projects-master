import subprocess
import sys
import pathlib

CLI = pathlib.Path(__file__).parent.parent / "jack_cli.py"


def test_cli_help():
    """CLI should exit 0 when called with --help."""
    result = subprocess.run(
        [sys.executable, str(CLI), "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "usage" in result.stdout.lower()
