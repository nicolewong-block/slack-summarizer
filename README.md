# Daily Slack Digest - @TLDRbot

Gets a summary of your Slack messages every morning — action items, key updates, and FYIs posted to a personal Slack channel.

---

## Setup (takes ~10 minutes)

### Step 1 — Authorize the app
Click the link below and hit **Allow**:

👉 **[Add to Slack](https://slack.com/oauth/v2/authorize?client_id=5596012676549.10799568727585&scope=&user_scope=channels:history,channels:read,groups:history,groups:read,chat:write,users:read)**

After authorizing, you'll be taken to a page. Go back to the app settings and copy your **User OAuth Token** (starts with `xoxp-`). Save it somewhere — you'll need it in Step 4.

---

### Step 2 — Get your Anthropic API key
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign in (or create a free account)
3. Go to **API Keys** → **Create Key**
4. Copy the key (starts with `sk-ant-`). Save it — you'll need it in Step 4.

---

### Step 3 — Download the code
1. Open **Terminal** on your Mac (press `Cmd+Space`, type "Terminal", hit Enter)
2. Copy and paste these two lines one at a time, pressing Enter after each:

```
git clone https://github.com/nicolewong-block/slack-summarizer.git
```
```
cd slack-summarizer
```

---

### Step 4 — Add your credentials
In Terminal, paste this line:
```
cp .env.example .env && open -e .env
```

A file will open in TextEdit. Fill in your two keys:
```
SLACK_USER_TOKEN=paste-your-xoxp-token-here
ANTHROPIC_API_KEY=paste-your-sk-ant-key-here
SUMMARY_CHANNEL=your-name-daily-summary
```

Save and close the file.

---

### Step 5 — Create your summary channel in Slack
1. In Slack, create a new channel — name it whatever you put in `SUMMARY_CHANNEL` above (e.g. `sarah-daily-summary`)
2. Make sure you join it

---

### Step 6 — Install dependencies
Make sure you're on the **Block corporate network or VPN**, then paste into Terminal:

```
/opt/homebrew/bin/python3.12 -m venv .venv
```
```
.venv/bin/pip install -r requirements.txt
```

---

### Step 7 — Test it
```
.venv/bin/python summarizer.py
```

Check your summary channel in Slack — you should see a digest within about 30 seconds.

---

### Step 8 — Schedule it to run every morning at 8 AM
Paste this into Terminal:

```
(crontab -l 2>/dev/null; echo "0 8 * * * cd $HOME/slack-summarizer && .venv/bin/python summarizer.py >> summarizer.log 2>&1") | crontab -
```

That's it! You'll get a daily digest in your summary channel every morning. 🎉

---

## Troubleshooting

**"command not found" when running python** — make sure you're using `.venv/bin/python`, not just `python`

**"channel not found" error** — double check the channel name in `.env` matches exactly what you created in Slack, and that you've joined it

**No messages showing up** — the digest only includes messages from the last 24 hours, so if it's your first run there may not be much yet

**Questions?** Slack Nicole Wong
