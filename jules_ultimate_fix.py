import os
import subprocess
import sys
from pathlib import Path

# The 'app' object from jules_api.py will be imported by the subprocess
# running under the virtual environment's Python, so it's not needed here.


def main():
    print("🎯 JULES ULTIMATE FIX")
    print("=========================")

    current_cwd = os.getcwd()
    # The script should be run from the repository root.
    # All paths will be relative to this current working directory.
    print(f"✅ Working directory: {current_cwd}")

    venv_path = Path(current_cwd) / "a2a-env"
    if venv_path.exists() and venv_path.is_dir():
        print("✅ Virtual environment found")
    else:
        print(f"Error: Virtual environment not found at {venv_path}")
        print(
            "Please ensure the virtual environment 'a2a-env' exists in the current directory."
        )
        print("If missing, run these first from the a2a-system directory:")
        print("python3 -m venv a2a-env")
        print(
            "a2a-env/bin/pip install wheels/flask-3.1.1-py3-none-any.whl wheels/click-8.2.1-py3-none-any.whl wheels/werkzeug-3.1.3-py3-none-any.whl wheels/jinja2-3.1.6-py3-none-any.whl wheels/itsdangerous-2.2.0-py3-none-any.whl wheels/MarkupSafe-3.0.2-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl wheels/blinker-1.9.0-py3-none-any.whl"
        )
        sys.exit(1)

    python_executable_names = [
        venv_path / "bin" / "python",
        venv_path / "bin" / "python3",
    ]
    python_executable = None
    for name in python_executable_names:
        if name.exists() and name.is_file():
            python_executable = name
            break

    if not python_executable:
        print(
            f"Error: Python executable not found in venv (tried {[str(n) for n in python_executable_names]})"
        )
        if (venv_path / "bin").exists():
            bin_contents = list((venv_path / "bin").iterdir())
            print(f"Contents of {venv_path / 'bin'}: {bin_contents}")
        else:
            print(f"Directory {venv_path / 'bin'} does not exist.")
        sys.exit(1)

    print(f"✅ Using Python: {python_executable}")

    try:
        # Check Flask version using the venv Python
        flask_check_command = [
            str(python_executable),
            "-c",
            "import flask; print(f'Flask version: {flask.__version__}')",
        ]
        result = subprocess.run(
            flask_check_command, capture_output=True, text=True, check=True
        )
        flask_version_output = result.stdout.strip()
        print(f"✅ Flask test: {flask_version_output}")

    except subprocess.CalledProcessError as e:
        print(f"Error checking Flask version: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        print("Ensure Flask is installed in the virtual environment.")
        sys.exit(1)
    except FileNotFoundError:
        print(
            f"Error: The Python executable {python_executable} was not found for Flask check."
        )
        sys.exit(1)

    print("🚀 Starting Jules API Server...")
    # The Flask dev server will print its own "Running on http://..." message to stderr.
    # The instruction "🌐 Server URL: http://127.0.0.1:5006" is expected as part of this output.
    # To explicitly print it from *this* script before starting the blocking `app.run`,
    # one would typically start Flask in a separate thread or process.
    # Given the context of a "simple fix", we'll rely on Flask's own output.
    # However, to match the requested output format more closely if Flask's output isn't exactly "🌐 Server URL: ...",
    # we can print it beforehand.
    print("🌐 Server URL: http://127.0.0.1:5006")

    try:
        # Construct the command to run the Flask app using the venv Python
        run_server_command = [
            str(python_executable),  # This is a2a-env/bin/python
            "-c",
            "from jules_api import app; app.run(host='127.0.0.1', port=5006, debug=False)",
        ]
        print(f"Executing: {' '.join(run_server_command)}")  # For debugging
        # This will now block until the server is stopped.
        # Output from Flask (like "Running on http://127.0.0.1:5006/") will go to stdout/stderr.
        subprocess.run(run_server_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting Flask server with subprocess: {e}")
        if e.stdout:
            print(f"Stdout: {e.stdout.decode(errors='ignore')}")
        if e.stderr:
            print(f"Stderr: {e.stderr.decode(errors='ignore')}")
        sys.exit(1)
    except FileNotFoundError:
        print(
            f"Error: The Python executable {python_executable} was not found for running the server."
        )
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while trying to start Flask server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
