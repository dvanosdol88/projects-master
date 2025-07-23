# Local Redis Broker

Start the broker:

```bash
docker-compose -f docker-compose-broker.yml up -d
```

Stop the broker:

```bash
docker-compose -f docker-compose-broker.yml down
```

### Re-queueing Messages

Failed messages are moved to `a2a_stream_deadletter` after three retries. To
re-queue them for processing:

```bash
redis-cli XRANGE a2a_stream_deadletter - + | while read id payload; do
  redis-cli XADD a2a_stream "$payload"
  redis-cli XDEL a2a_stream_deadletter "$id"
done
```
