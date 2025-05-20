from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from services.auth import get_auth_flow
from services.db import SessionLocal, engine
from services.producer import produce_auth_event
from models.user import Base, User, delete_user_by_email, insert_user
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# DB setup
Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/login")
def login():
    flow = get_auth_flow()
    auth_url, _ = flow.authorization_url(prompt="consent", include_granted_scopes="true")
    return RedirectResponse(auth_url)


@app.get("/oauth2callback")
async def oauth_callback(request: Request):
    flow = get_auth_flow()
    flow.fetch_token(authorization_response=str(request.url))

    credentials = flow.credentials
    user_info = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {credentials.token}"}
    ).json()

    db = SessionLocal()
    delete_user_by_email(db, user_info["email"])
    user = User(
        email=user_info["email"],
        name=user_info.get("name", ""),
        access_token=credentials.token,
        refresh_token=credentials.refresh_token,
    )
    insert_user(db, user)
    db.commit()
    print("Generating kafka event")
    produce_auth_event(user)
    return templates.TemplateResponse(
        "login.html", {"request": request, "message": f"Welcome, {user_info['email']}!"}
    )
