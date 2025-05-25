from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from datetime import datetime

Base = declarative_base()

class SpamEmailHash(Base):
    __tablename__ = "spam_email_hashes"

    hash = Column(String, primary_key=True)
    subject = Column(String)
    sender = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
