import os
from ..models.user import get_user_by_email
from .db import SessionLocal
from confluent_kafka import Consumer
import json
from .producer import produce_bloom_event
from spam_detection import predict_spam

conf = {
    'bootstrap.servers': os.getenv("KAFKA_BROKER", "kafka:9092"),
    'group.id': 'auth-event-group-test',
    'auto.offset.reset': 'earliest',
}
KAFKA_TOPIC = "bloom-events"
session = SessionLocal()

def handle_email_event(event_data):
    print("Handling event:", event_data)
    user = get_user_by_email(session, event_data["email"])
    if event_data["is_spam_bloom"]:
        produce_bloom_event(email=event_data["raw_email"], user=user)
    else:
        spam = predict_spam(event_data["raw_email"])
        if spam:
            produce_bloom_event(email=event_data["raw_email"], user=user)



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
