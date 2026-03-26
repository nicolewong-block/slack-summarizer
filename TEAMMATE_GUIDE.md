# Slack Daily Digest Bot — User Guide

Get AI-powered summaries of your Slack messages by simply @mentioning the bot!

---

## 🚀 Quick Start (2 minutes)

### Step 1: Connect Your Slack Account

Visit the installation page and click "Sign in with Slack":

👉 **https://jordan-spleenier-bigotedly.ngrok-free.dev/install**

You'll be asked to authorize the bot to:
- Read your public and private channels
- Read message history
- Post messages on your behalf

Click **Allow** to continue.

> **⚠️ Important for Block employees:** If you see "not authorized to install on infosec alerts", click **"Request approval"** on the OAuth screen. A Block Slack admin will approve the app, then you can complete the sign-in. This is a one-time security review.

### Step 2: Test It Out

In any Slack channel, @mention the bot:

```
@Daily Summarizer give me a digest
```

The bot will:
1. Read all your joined channels (public + private)
2. Collect messages from the last 24 hours
3. Use Claude AI to generate an intelligent summary
4. Reply in the thread with action items, key updates, and FYIs

That's it! 🎉

---

## 💡 How It Works

**Multi-User OAuth Flow:**
- When you connect via `/install`, the bot stores your personal Slack token securely
- When you @mention the bot, it uses *your* token to read *your* channels
- Each user gets personalized summaries based on their channel access
- Your token is stored locally in an encrypted SQLite database

**AI Summarization:**
- Powered by Claude Opus 4.6 with adaptive thinking
- Intelligently categorizes messages into:
  - 🎯 **Action Items** — things you need to do
  - 📢 **Key Updates** — important announcements and decisions
  - ℹ️ **FYIs** — good-to-know information
- Filters out noise and focuses on what matters

---

## 🔧 Advanced Usage

### Run Your Own Instance

Want to run the bot yourself or customize it? Here's how:

#### Prerequisites
- Mac with Python 3.12+ installed
- Block VPN access (for installing packages)
- Anthropic API key ([get one free](https://console.anthropic.com))

#### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nicolewong-block/slack-summarizer.git
   cd slack-summarizer
   ```

2. **Set up Python environment:**
   ```bash
   python3.12 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your credentials:
   ```env
   # Bot credentials (ask Nicole Wong for these)
   SLACK_BOT_TOKEN=xoxb-your-bot-token
   SLACK_SIGNING_SECRET=your-signing-secret
   SLACK_CLIENT_ID=5596012676549.10799568727585
   SLACK_CLIENT_SECRET=your-client-secret
   
   # Your personal Anthropic API key
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   
   # ngrok tunnel URL (update after starting ngrok)
   BASE_URL=https://your-ngrok-url.ngrok-free.dev
   ```

4. **Start ngrok tunnel:**
   ```bash
   ngrok http 8000
   ```
   
   Copy the HTTPS URL (e.g., `https://abc123.ngrok-free.dev`) and update `BASE_URL` in `.env`

5. **Run the bot server:**
   ```bash
   .venv/bin/python bot.py
   ```

The bot is now running! Visit `http://localhost:8000/install` to connect your account.

---

## 🤖 Standalone Daily Digest

Want automated daily summaries posted to a dedicated channel? Use the standalone script:

### Setup

1. **Create a summary channel in Slack:**
   - Create a new channel (e.g., `#yourname-daily-summary`)
   - Make sure you join it

2. **Get your Slack User Token:**
   - Go to [api.slack.com/apps](https://api.slack.com/apps)
   - Select "Daily Summarizer" app
   - Go to **OAuth & Permissions**
   - Copy your **User OAuth Token** (starts with `xoxp-`)

3. **Configure `.env`:**
   ```env
   SLACK_USER_TOKEN=xoxp-your-user-token
   ANTHROPIC_API_KEY=sk-ant-your-key
   SUMMARY_CHANNEL=yourname-daily-summary
   ```

4. **Test it:**
   ```bash
   .venv/bin/python summarizer.py
   ```
   
   Check your summary channel — you should see a digest within 30 seconds!

### Schedule Daily Digests

**Option 1: Cron (runs even when laptop is closed)**

Run every weekday at 8 AM:
```bash
(crontab -l 2>/dev/null; echo "0 8 * * 1-5 cd $HOME/slack-summarizer && .venv/bin/python summarizer.py >> summarizer.log 2>&1") | crontab -
```

**Option 2: launchd (macOS native, more reliable)**

Create `~/Library/LaunchAgents/com.slack.dailydigest.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.slack.dailydigest</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/YOUR_USERNAME/slack-summarizer/.venv/bin/python</string>
        <string>/Users/YOUR_USERNAME/slack-summarizer/summarizer.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/YOUR_USERNAME/slack-summarizer/summarizer.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/YOUR_USERNAME/slack-summarizer/summarizer.log</string>
</dict>
</plist>
```

Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.slack.dailydigest.plist
```

---

## 🔒 Security & Privacy

**What data does the bot access?**
- Only channels you've joined (public and private)
- Message content from the last 24 hours
- User display names for attribution

**Where is data stored?**
- Your Slack token is stored locally in `users.db` (SQLite)
- No message content is stored — only processed in memory
- Summaries are sent directly to Slack, not saved

**Who can see my summaries?**
- Only you! Summaries are posted in threads visible only to you
- If using standalone mode, summaries go to your private channel

**Can I revoke access?**
- Yes! Go to [slack.com/apps](https://slack.com/apps) → Daily Summarizer → Remove

---

## 🐛 Troubleshooting

### "Please visit /install to connect"
You haven't connected your Slack account yet. Visit the installation URL and authorize the bot.

### "Not authorized to install on infosec alerts"
This is expected for Block employees. Click **"Request approval"** and wait for a Slack admin to approve the app (usually within 1 business day).

### Bot doesn't respond to @mentions
1. Check that the bot server is running (`ps aux | grep bot.py`)
2. Verify ngrok tunnel is active (`curl https://your-ngrok-url.ngrok-free.dev/install`)
3. Check logs: `tail -f bot.log`

### "No messages found in the last 24 hours"
The bot only summarizes recent messages. If you just joined channels or it's a quiet day, there may be nothing to summarize.

### Installation fails on Block network
Make sure you're connected to **Block VPN** — the corporate network blocks PyPI. Use the internal Artifactory mirror:
```bash
.venv/bin/pip install -r requirements.txt --index-url https://artifactory.sqprod.co/artifactory/api/pypi/pypi/simple
```

### ngrok URL changed after restart
1. Update `BASE_URL` in `.env` with the new ngrok URL
2. Update the OAuth redirect URL in [Slack app settings](https://api.slack.com/apps)
3. Restart the bot: `pkill -f bot.py && .venv/bin/python bot.py &`

---

## 📞 Support

**Questions or issues?**
- Slack: **@Nicole Wong**
- GitHub: [github.com/nicolewong-block/slack-summarizer](https://github.com/nicolewong-block/slack-summarizer)
- Email: nicolewong@block.xyz

**Want to contribute?**
Pull requests welcome! The codebase is simple:
- `bot.py` — FastAPI server handling OAuth and @mentions
- `summarizer.py` — Core digest logic with Claude AI
- `requirements.txt` — Dependencies

---

## 📚 Technical Details

**Architecture:**
```
User @mentions bot
    ↓
Slack Event API → bot.py (FastAPI)
    ↓
Look up user token in users.db
    ↓
Use user token to fetch channels & messages
    ↓
summarizer.py builds digest
    ↓
Claude Opus 4.6 generates summary
    ↓
Post summary to thread
```

**Tech Stack:**
- Python 3.12
- FastAPI (web server)
- Slack SDK (API client)
- Anthropic SDK (Claude AI)
- SQLite (token storage)
- ngrok (local tunnel for development)

**Slack Permissions:**
- `channels:history` — Read public channel messages
- `channels:read` — List public channels
- `groups:history` — Read private channel messages
- `groups:read` — List private channels
- `chat:write` — Post summaries
- `users:read` — Get user display names

**Environment Variables:**
| Variable | Description | Example |
|----------|-------------|---------|
| `SLACK_BOT_TOKEN` | Bot token for posting messages | `xoxb-...` |
| `SLACK_USER_TOKEN` | Your personal token (standalone mode) | `xoxp-...` |
| `SLACK_SIGNING_SECRET` | Verify webhook requests | `abc123...` |
| `SLACK_CLIENT_ID` | OAuth client ID | `5596012676549.10799568727585` |
| `SLACK_CLIENT_SECRET` | OAuth client secret | `def456...` |
| `ANTHROPIC_API_KEY` | Claude API key | `sk-ant-...` |
| `BASE_URL` | Public URL for OAuth callbacks | `https://abc.ngrok-free.dev` |
| `SUMMARY_CHANNEL` | Channel for standalone digests | `nicole-daily-summary` |

---

## 🎯 Roadmap

Potential future enhancements:
- [ ] Custom time ranges (last 48 hours, last week, etc.)
- [ ] Channel filtering (exclude noisy channels)
- [ ] Multiple summary styles (brief, detailed, bullet points)
- [ ] Scheduled digests via bot commands
- [ ] Thread summarization (summarize specific threads)
- [ ] Sentiment analysis and tone detection
- [ ] Integration with other tools (Jira, GitHub, etc.)

Have ideas? Open an issue on GitHub!

---

**Built with ❤️ by Nicole Wong**  
*Making Slack more manageable, one digest at a time.*
