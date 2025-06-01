import os

import redis

from ..models.user import get_user_by_email
from .redis_bloom_filter import RedisBloomFilter
from .db import SessionLocal
from .bloom import add_spam_email_to_db
from confluent_kafka import Consumer
import json
from .gmail import mark_message_as_spam

conf = {
    'bootstrap.servers': os.getenv("KAFKA_BROKER", "kafka:9092"),
    'group.id': 'auth-event-group-test',
    'auto.offset.reset': 'earliest',
}
KAFKA_TOPIC = "spam-events"
# Redis Setup
redis_client = redis.Redis(host=os.getenv('REDIS_HOST'), port=6379, db=0)
bloom = RedisBloomFilter(redis_client)
session = SessionLocal()

def handle_email_event(event_data):
    print("Handling event:", event_data)
    user = get_user_by_email(session, event_data["email"])
    add_spam_email_to_db(event_data["raw_email"], bloom, session)
    mark_message_as_spam(user, event_data["raw_email"]["id"])

def start_consumer():
    consumer = Consumer(conf)

    consumer.subscribe([KAFKA_TOPIC])
    print(f"Subscribed to topic: {KAFKA_TOPIC}")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                print("Waiting for message...")
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            print(f"Raw Kafka message: {msg.value()}")
            data = json.loads(msg.value().decode("utf-8"))
            handle_email_event(data)

    finally:
        consumer.close()
