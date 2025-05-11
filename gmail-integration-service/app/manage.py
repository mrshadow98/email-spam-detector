import os
import sys

from dotenv import load_dotenv
# Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from main.models.user import Base
from main.services.db import engine

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Done.")

if __name__ == "__main__":
    load_dotenv()
    init_db()
