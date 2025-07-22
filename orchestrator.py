import os
import signal
import subprocess
import sys


def main() -> None:
    port = os.environ.get("A2A_JULES_PORT", "5000")
    env = {**os.environ, "A2A_JULES_PORT": str(port)}

    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_name = "orchestrator.log"
    if os.environ.get("A2A_TEST_MODE"):
        log_name = "orchestrator-test.log"
    log_path = os.path.join(log_dir, log_name)

    with open(log_path, "w") as log:
        proc = subprocess.Popen(
            [sys.executable, "api/jules_server.py"],
            env=env,
            stdout=log,
            stderr=log,
            preexec_fn=os.setsid if os.name != "nt" else None,
        )
        try:
            proc.wait()
        except KeyboardInterrupt:
            pass
        finally:
            if os.name == "nt":
                proc.terminate()
            else:
                os.killpg(os.getpgid(proc.pid), signal.SIGINT)
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()


if __name__ == "__main__":
    main()
