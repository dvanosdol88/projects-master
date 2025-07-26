import argparse
import os
import uuid

import redis

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))


def publish_task(client: redis.Redis, channel: str, message: str) -> str:
    task_id = str(uuid.uuid4())
    client.publish(channel, message)
    print(f"Sent task to {channel}: {message}")
    return task_id


def listen_for_reply(client: redis.Redis, channel: str) -> str:
    pubsub = client.pubsub()
    pubsub.subscribe(channel)
    for msg in pubsub.listen():
        if msg.get("type") == "message":
            data = msg["data"].decode()
            print(f"Received reply: {data}")
            return data
    return ""


def main() -> None:
    parser = argparse.ArgumentParser(description="Send a task via Redis pub/sub")
    parser.add_argument("message")
    parser.add_argument("--to", default="DC", help="channel to publish to")
    parser.add_argument("--reply", default="UC", help="channel to read reply from")
    args = parser.parse_args()

    client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
    publish_task(client, args.to, args.message)
    listen_for_reply(client, args.reply)


if __name__ == "__main__":
    main()
