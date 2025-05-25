import os
import sys

from dotenv import load_dotenv
from app.models.user import Base
# Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))


from app.services.db import engine

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Done.")

if __name__ == "__main__":
    load_dotenv()
    init_db()
