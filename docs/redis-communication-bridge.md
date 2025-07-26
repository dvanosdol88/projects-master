# Redis Communication Bridge

This document outlines the basic setup for enabling cross-host communication between different Claude instances using Redis.

## Redis Setup
- The broker is defined in `infra/broker/docker-compose-broker.yml`.
- Redis exposes port `6379` and is attached to the `agents-net` network so that external hosts can reach it.

## Claude Listener
Run `agents/dc/claude_listener.py` on each Claude machine with appropriate environment variables:

```bash
CHANNEL=DC \
RESPONSE_CHANNEL=UC \
REDIS_HOST=host.docker.internal \
CLAUDE_CMD=/path/to/claude \
python agents/dc/claude_listener.py
```

Each listener subscribes to its channel, runs the Claude CLI with the task, and publishes the output back to the peer channel.
Logs are written to `logs/agent_traffic.log` for auditing communication.
You may also use `bin/run_claude.sh` as a convenience wrapper around the Claude CLI.

## Triggering Tasks
Use `redis_trigger.py` to publish a message and wait for the reply:

```bash
python redis_trigger.py "Check this code" --to DC --reply UC
```

This sends the request on channel `DC` and prints the response from `UC`.
