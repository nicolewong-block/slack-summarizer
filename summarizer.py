#!/usr/bin/env python3
"""
Daily Slack summarizer — reads all channels from the last 24 hours
and posts action items + key updates to #nicole-daily-summary.
"""

import os
import sys
import time
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import anthropic

load_dotenv()

SLACK_USER_TOKEN = os.environ["SLACK_USER_TOKEN"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
SUMMARY_CHANNEL_NAME = os.getenv("SUMMARY_CHANNEL", "nicole-daily-summary")

slack = WebClient(token=SLACK_USER_TOKEN)
claude = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


# ---------------------------------------------------------------------------
# Slack helpers
# ---------------------------------------------------------------------------

def get_user_display_name(user_id: str, cache: dict, client: WebClient = None) -> str:
    if user_id in cache:
        return cache[user_id]
    client = client or slack
    try:
        resp = client.users_info(user=user_id)
        name = resp["user"].get("display_name") or resp["user"].get("real_name", user_id)
    except SlackApiError:
        name = user_id
    cache[user_id] = name
    return name


def slack_call(fn, *args, **kwargs):
    """Call a Slack API function with simple rate-limit retry."""
    for attempt in range(10):
        try:
            return fn(*args, **kwargs)
        except SlackApiError as e:
            if e.response.get("error") == "ratelimited":
                wait = int(e.response.headers.get("Retry-After", 10))
                print(f"  Rate limited — waiting {wait}s...")
                time.sleep(wait)
            else:
                raise
    raise RuntimeError("Slack API still rate limited after retries")


def list_all_joined_channels(client: WebClient = None) -> list[dict]:
    """Return all public + private channels the user is a member of."""
    client = client or slack
    channels = []
    cursor = None
    while True:
        resp = slack_call(
            client.users_conversations,
            types="public_channel,private_channel",
            exclude_archived=True,
            limit=200,
            cursor=cursor,
        )
        channels.extend(resp["channels"])
        cursor = resp.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break
    return channels


def fetch_channel_messages(channel_id: str, oldest_ts: float, client: WebClient = None) -> list[dict]:
    """Fetch human messages in a channel since oldest_ts (unix timestamp)."""
    client = client or slack
    messages = []
    cursor = None
    while True:
        resp = slack_call(
            client.conversations_history,
            channel=channel_id,
            oldest=str(oldest_ts),
            limit=200,
            cursor=cursor,
        )
        messages.extend(resp.get("messages", []))
        cursor = resp.get("response_metadata", {}).get("next_cursor")
        if not cursor or not resp.get("has_more"):
            break

    return [
        m for m in messages
        if m.get("type") == "message"
        and not m.get("bot_id")
        and not m.get("subtype")
        and m.get("text", "").strip()
    ]


def find_channel_id_from_list(name: str, channels: list[dict]) -> str | None:
    """Find a channel ID by name from an already-fetched list."""
    return next((ch["id"] for ch in channels if ch.get("name") == name), None)


# ---------------------------------------------------------------------------
# Build the message digest
# ---------------------------------------------------------------------------

def build_digest(channels: list[dict], oldest_ts: float, client: WebClient = None) -> str:
    """Collect messages from all channels into a single formatted string."""
    client = client or slack
    user_cache: dict[str, str] = {}
    sections: list[str] = []

    for ch in channels:
        try:
            messages = fetch_channel_messages(ch["id"], oldest_ts, client=client)
        except (SlackApiError, RuntimeError) as e:
            print(f"  Skipping #{ch['name']}: {e.response['error']}")
            continue

        if not messages:
            continue

        lines = [f"\n=== #{ch['name']} ==="]
        for msg in reversed(messages):  # chronological order
            sender = get_user_display_name(msg.get("user", "unknown"), user_cache, client=client)
            lines.append(f"{sender}: {msg['text'].strip()}")

        sections.append("\n".join(lines))
        print(f"  #{ch['name']}: {len(messages)} message(s)")

    return "\n".join(sections)


# ---------------------------------------------------------------------------
# Claude summarization
# ---------------------------------------------------------------------------

def summarize(digest: str, user_name: str = "Nicole") -> str:
    today = datetime.now().strftime("%A, %B %d, %Y")

    with claude.messages.stream(
        model="claude-opus-4-6",
        max_tokens=4096,
        thinking={"type": "adaptive"},
        system=(
            f"You are a concise assistant helping {user_name} stay on top of their work. "
            f"You read their Slack messages and surface what actually needs their attention."
        ),
        messages=[{
            "role": "user",
            "content": f"""Here are {user_name}'s Slack messages from the past 24 hours ({today}):

{digest}

Write a brief daily digest. Use Slack mrkdwn formatting only: *bold* for emphasis, bullet points with •, no markdown headers (no ##), no double asterisks (**).

Format exactly like this (omit any section that has nothing to report):

✅ *Action Items*
• <who>: <what needs to be done>

📌 *Key Updates*
• <update>

👀 *FYI*
• <low priority item>

Be specific and concise. Skip pleasantries.""",
        }],
    ) as stream:
        msg = stream.get_final_message()
        return next(b.text for b in msg.content if b.type == "text")


# ---------------------------------------------------------------------------
# Post to Slack
# ---------------------------------------------------------------------------

def post_to_slack(text: str, channels: list[dict]) -> None:
    channel_id = find_channel_id_from_list(SUMMARY_CHANNEL_NAME, channels)
    if not channel_id:
        print(f"Error: #{SUMMARY_CHANNEL_NAME} not found. Create it and make sure you're a member.")
        sys.exit(1)

    today = datetime.now().strftime("%A, %B %d")
    slack.chat_postMessage(
        channel=channel_id,
        text=f"*Daily Digest — {today}*\n\n{text}",
        unfurl_links=False,
        unfurl_media=False,
    )
    print(f"Posted to #{SUMMARY_CHANNEL_NAME}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run() -> None:
    oldest_ts = (datetime.now(timezone.utc) - timedelta(hours=24)).timestamp()

    print("Fetching joined channels...")
    channels = list_all_joined_channels()
    print(f"Found {len(channels)} channel(s). Pulling messages...")

    digest = build_digest(channels, oldest_ts)

    if not digest.strip():
        print("No messages in the last 24 hours — nothing to summarize.")
        return

    print("Summarizing with Claude...")
    summary = summarize(digest)

    print("Posting to Slack...")
    post_to_slack(summary, channels)
    print("Done.")


if __name__ == "__main__":
    run()
