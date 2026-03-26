# 🤖 How to Use the Slack Daily Digest Bot

**Get AI summaries of your Slack messages by @mentioning the bot!**

---

## Step 1: Connect Your Slack Account (one-time, 1 minute)

Click this link and sign in:

### 👉 **https://jordan-spleenier-bigotedly.ngrok-free.dev/install**

You'll see a page that says "Slack Daily Digest Bot" with a **"Sign in with Slack"** button.

Click the button, and Slack will ask you to authorize the bot to:
- Read your public channels
- Read your private channels  
- Read message history
- Post messages on your behalf

Click **"Allow"** to continue.

### ⚠️ Block Employees: Request Approval

If you see an error that says **"not authorized to install on infosec alerts"**:

1. Click the **"Request approval"** button on the OAuth screen
2. A Block Slack admin will review and approve the app (usually within 1 business day)
3. You'll get a notification when it's approved
4. Come back to the install link and try again

This is a one-time security review — you only need to do it once!

---

## Step 2: Get Your Summary

Once you're connected, using the bot is super simple!

In **any Slack channel**, just @mention the bot:

```
@Daily Summarizer give me a digest
```

The bot will:
1. ⏳ Reply "Pulling your Slack messages from the last 24 hours..."
2. 🤖 Read all your joined channels (public + private)
3. ✨ Use AI to create an intelligent summary
4. 📬 Post the summary in the thread

### What You'll Get

Your summary will include:

- **🎯 Action Items** — Things you need to do or respond to
- **📢 Key Updates** — Important announcements, decisions, and changes
- **ℹ️ FYIs** — Useful information to be aware of

The AI filters out noise and focuses on what actually matters to you!

---

## Examples

**Get a summary:**
```
@Daily Summarizer give me a digest
```

**Quick check:**
```
@Daily Summarizer what did I miss?
```

**After vacation:**
```
@Daily Summarizer catch me up
```

The bot understands natural language — just @mention it and ask!

---

## Privacy & Security

**What can the bot see?**
- Only channels **you** have joined (public and private)
- Only messages from the last 24 hours
- The bot uses **your** Slack account, so it sees exactly what you see

**Where is my data stored?**
- Your Slack token is stored securely in a local database
- No message content is saved — only processed in memory
- Summaries are posted directly to Slack threads (only you can see them)

**Can I disconnect?**
- Yes! Go to [slack.com/apps](https://slack.com/apps) → Daily Summarizer → Remove

---

## Troubleshooting

### "Please visit /install to connect"
You haven't connected your account yet. Go to the install link above and authorize the bot.

### "Not authorized to install on infosec alerts"
Click **"Request approval"** and wait for a Slack admin to approve (usually 1 business day).

### Bot doesn't respond
- Make sure you're @mentioning the bot correctly: `@Daily Summarizer`
- Check that the bot is in the channel (it should auto-join when mentioned)
- Try in a different channel

### "No messages found in the last 24 hours"
The bot only looks at the last 24 hours. If your channels have been quiet or you just joined them, there might not be anything to summarize yet.

---

## Questions?

Slack **@Nicole Wong** or check out the full documentation in `TEAMMATE_GUIDE.md`

---

**That's it! Enjoy your AI-powered Slack summaries! 🎉**
