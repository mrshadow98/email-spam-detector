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
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def produce_auth_event(user):
    event_payload = {
        "email": user.email,
        "name": user.name,
        "event": "USER_LOGGED_IN"
    }

    producer.produce("auth-events", json.dumps(event_payload).encode("utf-8"), callback=delivery_report)
    producer.flush()
