import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from ..models.user import User
from db import SessionLocal
from producer import produce_email_event

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

def fetch_all_emails(user: User):
    service = get_gmail_service(user)
    result = service.users().messages().list(userId="me").execute()

    while result:
        messages = result.get("messages", [])
        for msg in messages:
            full_msg = service.users().messages().get(userId="me", id=msg["id"]).execute()
            produce_email_event(full_msg, user)

        next_page_token = result.get("nextPageToken")
        if next_page_token:
            result = service.users().messages().list(userId="me", pageToken=next_page_token).execute()
        else:
            break
