import os

import redis

from ..models.user import get_user_by_email
from ..services.bloom import process_email, preload_bloom_from_db
from .redis_bloom_filter import RedisBloomFilter
from .db import SessionLocal
from confluent_kafka import Consumer
import json

conf = {
    'bootstrap.servers': os.getenv("KAFKA_BROKER", "kafka:9092"),
    'group.id': 'auth-event-group-test',
    'auto.offset.reset': 'earliest',
}
KAFKA_TOPIC = "bloom-events"
# Redis Setup
redis_client = redis.Redis(host=os.getenv('REDIS_HOST'), port=6379, db=0)
bloom = RedisBloomFilter(redis_client)
session = SessionLocal()
# Load from Postgres on startup
preload_bloom_from_db(session, bloom)

def handle_email_event(event_data):
    print("Handling event:", event_data)
    user = get_user_by_email(session, event_data["email"])
    # process_email(user, event_data["raw_email"], bloom)
    # Store to Redis, log it, etc.

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
