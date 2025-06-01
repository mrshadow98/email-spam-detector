from confluent_kafka import Producer
import json
import os

conf = {
    'bootstrap.servers': os.getenv("KAFKA_BROKER", "localhost:9092")
}

producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")

def produce_bloom_event(email, user, is_spam_bloom = False):
    event_payload = {
        "email": user.email,
        "name": user.name,
        "raw_email": email,
        "event": "BLOOM_FILTERED",
        "is_spam_bloom": is_spam_bloom
    }

    producer.produce("bloom-events", json.dumps(event_payload).encode("utf-8"), callback=delivery_report)
    producer.flush()

