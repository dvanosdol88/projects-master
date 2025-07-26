from __future__ import annotations

import logging
import os
import subprocess

import redis

CHANNEL = os.getenv("CHANNEL", "DC")
RESPONSE_CHANNEL = os.getenv("RESPONSE_CHANNEL", "UC")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
CLAUDE_CMD = os.getenv("CLAUDE_CMD", "claude")
AGENT_ID = os.getenv("AGENT_ID", "DC")
LOG_FILE = os.getenv("LOG_FILE", "logs/agent_traffic.log")

logging.basicConfig(
    filename=LOG_FILE, level=logging.INFO, format="%(asctime)s %(message)s"
)


def call_claude_cli(prompt: str) -> str:
    """Send the prompt to the Claude CLI and return its output."""
    try:
        result = subprocess.run(
            [CLAUDE_CMD],
            input=prompt.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=90,
        )
        output = result.stdout.decode().strip()
        if result.returncode != 0:
            raise RuntimeError(output)
        return output
    except Exception as exc:  # broad catch for a CLI wrapper
        return f"[ERROR]: Claude failed: {exc}"


def main() -> None:
    client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    pubsub = client.pubsub()
    pubsub.subscribe(CHANNEL)
    print(f"\U0001f50d Claude listener active on: {CHANNEL}")
    for message in pubsub.listen():
        if message.get("type") != "message":
            continue
        prompt = str(message["data"])
        print(f"\U0001f9e0 Claude received task: {prompt}")
        response = call_claude_cli(prompt)
        logging.info(
            f"{AGENT_ID} \u2192 {RESPONSE_CHANNEL} | {prompt} | {response[:100]}"
        )
        print(f"\U0001f4e4 Responding to {RESPONSE_CHANNEL}: {response[:200]}")
        client.publish(RESPONSE_CHANNEL, response)


if __name__ == "__main__":
    main()
