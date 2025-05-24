import os
from ..models.user import get_user_by_email
from ..services.gmail import fetch_all_emails
from confluent_kafka import Consumer
import json

conf = {
    'bootstrap.servers': os.getenv("KAFKA_BROKER", "kafka:9092"),
    'group.id': 'auth-event-group-test',
    'auto.offset.reset': 'earliest',
}
KAFKA_TOPIC = "auth-events"
def handle_auth_event(event_data):
    print("Handling event:", event_data)
    user = get_user_by_email(event_data["email"])
    fetch_all_emails(user)
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
            handle_auth_event(data)

    finally:
        consumer.close()
