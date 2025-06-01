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

def produce_email_event(email, user, email_id):
    event_payload = {
        "email": user.email,
        "name": user.name,
        "raw_email": email,
        "msg_id": email_id,
        "event": "EMAIL_LOADED"
    }

    producer.produce("email-events", json.dumps(event_payload).encode("utf-8"), callback=delivery_report)
    producer.flush()
