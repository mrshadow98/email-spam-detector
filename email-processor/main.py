import os
from dotenv import load_dotenv

load_dotenv()
from app.services.consumer import start_consumer
if __name__ == "__main__":
    try:
        print(">>> main.py started")
        start_consumer()
    except Exception as e:
        print(f"!!! Error: {e}")
