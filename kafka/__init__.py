import json
from typing import Any

from aiokafka import AIOKafkaProducer

from settings import KAFKA_BOOTSTRAP_SERVERS

producer: AIOKafkaProducer | None = None


async def init_kafka_producer():
    global producer
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda v: str(v).encode("utf-8"),
    )
    await producer.start()


async def close_kafka_producer():
    global producer
    if producer:
        await producer.stop()


async def send_message(topic: str, key: str, value: Any):
    if producer:
        await producer.send_and_wait(topic, key=key, value=value)
