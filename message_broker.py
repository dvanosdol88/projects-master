"""Minimal publish/subscribe helpers for JACK message broker.

This module now includes utilities for retry tracking, a dead-letter queue,
and Prometheus metrics exporting. The consumer helpers rely on Redis Streams.
"""

from typing import Any, Callable

try:  # pragma: no cover - optional dependency
    import redis  # type: ignore
except Exception:  # pragma: no cover - redis optional
    redis = None  # placeholder for environments without redis

try:  # pragma: no cover - optional dependency
    from prometheus_client import Counter, start_http_server
except Exception:  # pragma: no cover - metrics optional
    Counter = None  # type: ignore

    def start_http_server(_port: int = 8000) -> None:  # type: ignore
        """Fallback when prometheus_client is unavailable."""
        return


if Counter is not None:  # pragma: no cover - only when metrics available
    tasks_retry_total = Counter("tasks_retry_total", "Total task retries")
    tasks_dlq_total = Counter("tasks_dlq_total", "Total tasks sent to DLQ")
else:  # pragma: no cover - metrics disabled

    class _Dummy:
        def inc(self) -> None:  # type: ignore
            pass

    tasks_retry_total = tasks_dlq_total = _Dummy()


class Broker:
    """Wrapper around Redis Streams for task messaging."""

    def __init__(self, url: str = "redis://localhost:6379/0", *, client=None) -> None:
        if client is not None:
            self.client = client
        else:
            if redis is None:
                raise RuntimeError("redis-py not available")
            self.client = redis.Redis.from_url(url)

    def publish(self, stream: str, message: dict[str, Any]) -> None:
        self.client.xadd(stream, message)

    def consume(self, stream: str, last_id: str = "$"):
        return self.client.xread({stream: last_id}, block=0)


def start_metrics_server(port: int = 8000) -> None:
    """Start the Prometheus metrics exporter if available."""
    if Counter is not None:
        start_http_server(port)


class StreamConsumer:
    """Consume a stream with retry and DLQ handling."""

    def __init__(
        self, broker: Broker, stream: str, group: str, consumer: str = "worker"
    ) -> None:
        self.broker = broker
        self.stream = stream
        self.group = group
        self.consumer = consumer
        self.dlq = f"{stream}_deadletter"
        # Ensure group exists
        try:
            self.broker.client.xgroup_create(stream, group, id="0-0", mkstream=True)
        except Exception:
            pass  # group may already exist

    def _delivery_count(self, msg_id: str) -> int:
        try:
            info = self.broker.client.xpending_range(
                self.stream, self.group, msg_id, msg_id, 1
            )
            if info:
                item = info[0]
                if isinstance(item, dict):
                    return int(item.get("times-delivered", 1))
                return int(getattr(item, "times_delivered", 1))
        except Exception:
            pass
        return 1

    def consume_one(self, handler: Callable[[dict[str, Any]], None]) -> None:
        res = self.broker.client.xreadgroup(
            self.group, self.consumer, {self.stream: ">"}, count=1, block=0
        )
        if not res:
            return
        _, msgs = res[0]
        msg_id, fields = msgs[0]
        delivery = self._delivery_count(msg_id)
        try:
            handler(fields)
            self.broker.client.xack(self.stream, self.group, msg_id)
        except Exception:
            if delivery >= 3:
                self.broker.client.xadd(self.dlq, fields)
                self.broker.client.xack(self.stream, self.group, msg_id)
                tasks_dlq_total.inc()
            else:
                tasks_retry_total.inc()
