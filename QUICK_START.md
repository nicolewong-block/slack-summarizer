# 🤖 Slack Daily Digest Bot — Quick Start

**Get AI-powered summaries of your Slack messages in seconds!**

---

## For Users (2 minutes)

### Step 1: Connect Your Account
Visit: **https://jordan-spleenier-bigotedly.ngrok-free.dev/install**

Click **"Sign in with Slack"** and authorize the bot.

> **Block employees:** If you see "not authorized to install on infosec alerts", click **"Request approval"**. A Slack admin will approve it within 1 business day.

### Step 2: Get Your Summary
In any Slack channel, type:
```
@Daily Summarizer give me a digest
```

The bot will reply with an AI summary of your last 24 hours of messages! 🎉

---

## What You Get

- 🎯 **Action Items** — things you need to do
- 📢 **Key Updates** — important announcements
- ℹ️ **FYIs** — good-to-know info

Powered by Claude Opus 4.6 with adaptive thinking.

---

## Questions?

Slack **@Nicole Wong** or see the full guide: `TEAMMATE_GUIDE.md`

---

## For Developers

**Run your own instance:**

```bash
# Clone and setup
git clone https://github.com/nicolewong-block/slack-summarizer.git
cd slack-summarizer
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt

# Configure (edit .env with your credentials)
cp .env.example .env

# Start ngrok tunnel
ngrok http 8000

# Update BASE_URL in .env with ngrok URL, then run bot
.venv/bin/python bot.py
```

**Standalone daily digest:**

```bash
# Configure SLACK_USER_TOKEN and SUMMARY_CHANNEL in .env
.venv/bin/python summarizer.py

# Schedule for 8 AM daily
(crontab -l 2>/dev/null; echo "0 8 * * * cd $HOME/slack-summarizer && .venv/bin/python summarizer.py >> summarizer.log 2>&1") | crontab -
```

See `TEAMMATE_GUIDE.md` for full documentation.
