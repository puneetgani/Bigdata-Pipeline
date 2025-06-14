import sys
import os
import types

# Ensure the project root is on sys.path so kafkaApi can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Create a dummy kafka module with KafkaProducer to avoid import errors
kafka_dummy = types.ModuleType('kafka')
class DummyProducer:
    def __init__(self, *args, **kwargs):
        pass
kafka_dummy.KafkaProducer = DummyProducer
sys.modules.setdefault('kafka', kafka_dummy)

from kafkaApi import json_serializer


def test_json_serializer_bytes():
    assert json_serializer({"a": 1}) == b'{"a": 1}'
