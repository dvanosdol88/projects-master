"""Redis relay used by the UC agent to communicate with Claude."""

from __future__ import annotations

import logging
import os
import time
import uuid

import redis

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
AGENT_ID = os.getenv("AGENT_ID", "UC")
LOG_FILE = os.getenv("LOG_FILE", "logs/agent_traffic.log")

logging.basicConfig(
    filename=LOG_FILE, level=logging.INFO, format="%(asctime)s %(message)s"
)


def send_task(to_channel: str, task: str) -> str:
    client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    task_id = str(uuid.uuid4())
    client.publish(to_channel, task)
    logging.info(f"{AGENT_ID} → {to_channel} | {task_id} | {task}")
    return task_id


def listen_for_response(
    from_channel: str, task_id: str, *, timeout: float = 30, retries: int = 2
) -> str:
    for attempt in range(retries + 1):
        client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        pubsub = client.pubsub()
        pubsub.subscribe(from_channel)
        start = time.monotonic()
        while time.monotonic() - start < timeout:
            message = pubsub.get_message(timeout=1)
            if message and message.get("type") == "message":
                data = str(message["data"])
                logging.info(f"{AGENT_ID} ← {from_channel} | {task_id} | {data}")
                return data
            time.sleep(0.1)
        logging.warning(
            f"{AGENT_ID} timed out waiting for response on {from_channel} (attempt {attempt + 1}/{retries + 1})"
        )
    return ""


def send_and_wait(to_channel: str, reply_channel: str, task: str) -> str:
    task_id = send_task(to_channel, task)
    return listen_for_response(reply_channel, task_id)
