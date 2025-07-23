import pytest

try:
    import fakeredis
except Exception:
    fakeredis = None

from message_broker import Broker, StreamConsumer, tasks_retry_total, tasks_dlq_total


@pytest.mark.unit
@pytest.mark.skipif(fakeredis is None, reason="fakeredis not installed")
def test_dlq_and_metrics():
    client = fakeredis.FakeRedis()
    broker = Broker(client=client)
    client.xgroup_create("tasks", "g1", id="0-0", mkstream=True)
    broker.publish("tasks", {"task": "do"})

    consumer = StreamConsumer(broker, "tasks", "g1", "c1")

    def always_fail(_msg):
        raise RuntimeError("boom")

    for _ in range(3):
        with pytest.raises(RuntimeError):
            consumer.consume_one(always_fail)

    assert client.xlen("tasks_deadletter") == 1
    assert tasks_dlq_total.inc  # ensure attribute exists
