# JACK Task Management
This guide shows how to send tasks to **Jules** (part of JACK) and check
status via `jack_cli.py`.

## Setup

1. Make sure Jules' Flask API is running. By default the CLI expects it at  
   `http://localhost:5000`.
2. (Linux/macOS) Make the script executable:
   ```bash
   chmod +x jack_cli.py
   ```
3. On Windows, call `python jack_cli.py` explicitly.

### Environment Variables

`orchestrator.py` reads the following variables when launching Jules:

- `A2A_JULES_PORT` – Port for the Jules server (defaults to 5000).
- `A2A_TEST_MODE` – When set, logs are written to `orchestrator-test.log`.

## Adding Tasks

Use `add` to queue a new task:
```bash
./jack_cli.py add "Finish documentation"
```

## Listing Tasks

See pending tasks with:
```bash
./jack_cli.py list
```

## Health Check

Verify Jules is running:
```bash
./jack_cli.py health
```

Use `--url` to target a different server.

For help on all commands:
```bash
./jack_cli.py --help
```
