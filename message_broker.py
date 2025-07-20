"""Minimal publish/subscribe helpers for JACK message broker."""
from typing import Any

try:
    import redis  # type: ignore
except Exception:  # pragma: no cover - redis optional
    redis = None  # placeholder for environments without redis


class Broker:
    """Wrapper around Redis Streams for task messaging."""

    def __init__(self, url: str = "redis://localhost:6379/0") -> None:
        if redis is None:
            raise RuntimeError("redis-py not available")
        self.client = redis.Redis.from_url(url)

    def publish(self, stream: str, message: dict[str, Any]) -> None:
        self.client.xadd(stream, message)

    def consume(self, stream: str, last_id: str = "$"):
        return self.client.xread({stream: last_id}, block=0)
