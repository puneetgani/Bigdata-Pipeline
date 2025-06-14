from clickhouse_driver import Client
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "puneet",
    bootstrap_servers=["localhost:9092"],
    auto_offset_reset="latest",
    enable_auto_commit=True,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
)
"""
The first argument is the topic,"puneet" in our case.

bootstrap_servers=['localhost:9092']:same as our producer

auto_offset_reset = 'earliest':one of the most important arguments.
It handles where the consumer restarts reading after breaking down or being turned off and
can be set either to earliest or latest.When set to latest,the consumer starts reading at
the end of the log.When set to earliest,the consumer starts reading at the latest committed offset.
And that's exactly what we want here.

enable_auto_commit = True:makes sure the consumer commits its read offset every interval.

auto_commit_interval_ms = 1000ms:sets the interval between two commits.
Since messages are coming in every five second,committing every second seems fair.

group_id = 'counters':this is the consumer group to which the consumer belongs.
Remember from the introduction that a consumer needs to be part of a consumer group to make the auto commit work.

The value deserializer deserializes the data into a common json format,the inverse of what our
value serializer was doing.
"""

client = Client(host='localhost')

for message in consumer:
    data = message.value
    name = data['name']
    address = data['address']
    created_at = data['created_at']
    client.execute(
        f"INSERT INTO myUsers (name, address, created_at) values('{name}','{address}','{created_at}')"
    )


