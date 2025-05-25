import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from ..models.user import User
from .db import SessionLocal

def get_gmail_service(user: User):
    creds = Credentials(
        token=user.access_token,
        refresh_token=user.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET")
    )

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        db = SessionLocal()
        user.access_token = creds.token
        db.merge(user)
        db.commit()

    return build("gmail", "v1", credentials=creds)

