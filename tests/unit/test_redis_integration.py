import json
import importlib
import sys
from pathlib import Path
import types

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

# Provide a stub redis module if not installed
if 'redis' not in sys.modules:
    sys.modules['redis'] = types.SimpleNamespace(Redis=lambda **_: None)

from infra import redis_client


def test_add_task_enqueues(monkeypatch):
    records = {}

    class FakeClient:
        def xadd(self, stream, message):
            records['stream'] = stream
            records['message'] = message
        def xrange(self, stream):
            return []

    monkeypatch.setattr(redis_client, 'client', FakeClient())
    import jules_api
    importlib.reload(jules_api)

    with jules_api.app.test_client() as c:
        resp = c.post('/add_task', json={'task': 'hello'})
        assert resp.status_code == 201

    assert records['stream'] == 'a2a_stream'
    assert records['message']['task'] == 'hello'


def test_cli_list_reads(monkeypatch, capsys):
    outputs = [('1-0', {b'task': b'ping', b'created': b'now'})]

    class FakeClient:
        def xrange(self, stream):
            return outputs

    monkeypatch.setattr(redis_client, 'client', FakeClient())
    monkeypatch.setattr(sys, 'argv', ['jack_cli.py', 'list'])
    import jack_cli
    importlib.reload(jack_cli)
    jack_cli.main()

    captured = capsys.readouterr()
    tasks = json.loads(captured.out)
    assert tasks[0]['task'] == 'ping'

