#!/usr/bin/env python3
"""
Slack bot server — responds to @mentions by running a fresh digest.
Run with: .venv/bin/python bot.py
"""

import os
import sqlite3
import uvicorn
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier

from summarizer import build_digest, list_all_joined_channels, summarize

load_dotenv()

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
SLACK_CLIENT_ID = os.environ["SLACK_CLIENT_ID"]
SLACK_CLIENT_SECRET = os.environ["SLACK_CLIENT_SECRET"]
BASE_URL = os.environ["BASE_URL"]  # e.g. https://abc123.ngrok-free.app

SLACK_USER_SCOPES = "channels:history,channels:read,groups:history,groups:read,chat:write,users:read"

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")

app = FastAPI()
bot = WebClient(token=SLACK_BOT_TOKEN)
verifier = SignatureVerifier(SLACK_SIGNING_SECRET)


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tokens (
            slack_user_id TEXT PRIMARY KEY,
            user_token     TEXT NOT NULL,
            display_name   TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_token(slack_user_id: str, user_token: str, display_name: str = None):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT OR REPLACE INTO tokens (slack_user_id, user_token, display_name) VALUES (?, ?, ?)",
        (slack_user_id, user_token, display_name),
    )
    conn.commit()
    conn.close()


def get_token(slack_user_id: str) -> tuple[str, str] | tuple[None, None]:
    """Returns (user_token, display_name) or (None, None) if not found."""
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT user_token, display_name FROM tokens WHERE slack_user_id = ?",
        (slack_user_id,),
    ).fetchone()
    conn.close()
    return (row[0], row[1]) if row else (None, None)


init_db()


# ---------------------------------------------------------------------------
# OAuth — install flow
# ---------------------------------------------------------------------------

@app.get("/install", response_class=HTMLResponse)
async def install():
    oauth_url = (
        "https://slack.com/oauth/v2/authorize"
        f"?client_id={SLACK_CLIENT_ID}"
        f"&user_scope={SLACK_USER_SCOPES}"
        f"&redirect_uri={BASE_URL}/slack/oauth/callback"
    )
    return HTMLResponse(f"""
    <html><body style="font-family:sans-serif;max-width:500px;margin:80px auto;text-align:center">
      <h2>Slack Daily Digest Bot</h2>
      <p>Connect your Slack account so the bot can summarize <em>your</em> channels.</p>
      <a href="{oauth_url}" style="
        display:inline-block;background:#4a154b;color:white;
        padding:12px 24px;border-radius:6px;text-decoration:none;font-size:16px">
        Sign in with Slack
      </a>
    </body></html>
    """)


@app.get("/slack/oauth/callback")
async def oauth_callback(code: str):
    auth_client = WebClient()
    resp = auth_client.oauth_v2_access(
        client_id=SLACK_CLIENT_ID,
        client_secret=SLACK_CLIENT_SECRET,
        code=code,
        redirect_uri=f"{BASE_URL}/slack/oauth/callback",
    )

    slack_user_id = resp["authed_user"]["id"]
    user_token = resp["authed_user"]["access_token"]

    # Look up their display name
    user_client = WebClient(token=user_token)
    try:
        info = user_client.users_info(user=slack_user_id)
        display_name = info["user"].get("display_name") or info["user"].get("real_name", slack_user_id)
    except Exception:
        display_name = slack_user_id

    save_token(slack_user_id, user_token, display_name)

    return HTMLResponse(f"""
    <html><body style="font-family:sans-serif;max-width:500px;margin:80px auto;text-align:center">
      <h2>You're connected, {display_name}!</h2>
      <p>Go to any Slack channel and type <strong>@Daily Summarizer</strong> to get your personalized digest.</p>
    </body></html>
    """)


# ---------------------------------------------------------------------------
# Event endpoint
# ---------------------------------------------------------------------------

@app.post("/slack/events")
async def slack_events(request: Request, background_tasks: BackgroundTasks):
    body_bytes = await request.body()

    if not verifier.is_valid_request(body_bytes, dict(request.headers)):
        raise HTTPException(status_code=403, detail="Invalid signature")

    body = await request.json()

    if body.get("type") == "url_verification":
        return JSONResponse({"challenge": body["challenge"]})

    event = body.get("event", {})
    if event.get("type") == "app_mention":
        background_tasks.add_task(handle_mention, event)

    return JSONResponse({"ok": True})


# ---------------------------------------------------------------------------
# Mention handler
# ---------------------------------------------------------------------------

def handle_mention(event: dict):
    channel = event["channel"]
    thread_ts = event.get("thread_ts", event["ts"])
    slack_user_id = event.get("user")

    user_token, display_name = get_token(slack_user_id)

    if not user_token:
        bot.chat_postMessage(
            channel=channel,
            thread_ts=thread_ts,
            text=(
                f"Hi! I don't have access to your Slack account yet.\n\n"
                f"Visit *{BASE_URL}/install* to connect and get your personalized digest."
            ),
        )
        return

    bot.chat_postMessage(
        channel=channel,
        thread_ts=thread_ts,
        text="Pulling your Slack messages from the last 24 hours... ⏳",
    )

    try:
        user_client = WebClient(token=user_token)
        oldest_ts = (datetime.now(timezone.utc) - timedelta(hours=24)).timestamp()
        channels = list_all_joined_channels(client=user_client)
        digest = build_digest(channels, oldest_ts, client=user_client)

        if not digest.strip():
            bot.chat_postMessage(
                channel=channel,
                thread_ts=thread_ts,
                text="No messages found in the last 24 hours.",
            )
            return

        user_name = display_name or "you"
        summary = summarize(digest, user_name=user_name)
        today = datetime.now().strftime("%A, %B %d")

        bot.chat_postMessage(
            channel=channel,
            thread_ts=thread_ts,
            text=f"*Daily Digest — {today}*\n\n{summary}",
            unfurl_links=False,
        )

    except Exception as e:
        bot.chat_postMessage(
            channel=channel,
            thread_ts=thread_ts,
            text=f"Something went wrong: {e}",
        )


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
