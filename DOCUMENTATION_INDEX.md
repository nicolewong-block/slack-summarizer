# 📚 Slack Daily Digest Bot — Documentation Index

All documentation for teammates to use and understand the bot.

---

## 🎯 For End Users (Your Teammates)

### **Start Here:** [HOW_TO_USE.md](HOW_TO_USE.md)
**Best for:** Teammates who just want to use the bot  
**Time:** 2 minutes to read, 1 minute to set up  
**Contents:**
- Step-by-step connection instructions
- How to @mention the bot
- Privacy & security info
- Troubleshooting common issues

### **Share This:** [SHARE_WITH_TEAMMATES.md](SHARE_WITH_TEAMMATES.md)
**Best for:** Quick reference card to share via Slack/email  
**Time:** 30 seconds to read  
**Contents:**
- Ultra-concise 2-step setup
- What users get (action items, updates, FYIs)
- Privacy summary
- Contact info

### **Announce With This:** [SLACK_ANNOUNCEMENT.md](SLACK_ANNOUNCEMENT.md)
**Best for:** Copy-paste templates for Slack announcements  
**Time:** Choose a template and post!  
**Contents:**
- 4 different announcement templates (short, detailed, technical, DM)
- Follow-up message after admin approval
- Tips for where/when to share

---

## 👨‍💻 For Developers & Power Users

### **Quick Reference:** [QUICK_START.md](QUICK_START.md)
**Best for:** Developers who want to run their own instance  
**Time:** 5 minutes to read, 15 minutes to set up  
**Contents:**
- Quick installation commands
- How to run the bot server
- How to run standalone daily digests
- Scheduling with cron

### **Complete Guide:** [TEAMMATE_GUIDE.md](TEAMMATE_GUIDE.md)
**Best for:** Comprehensive reference for all use cases  
**Time:** 15 minutes to read  
**Contents:**
- User guide (OAuth flow)
- Developer guide (run your own instance)
- Standalone daily digest setup
- Scheduling options (cron vs launchd)
- Security & privacy details
- Troubleshooting
- Technical architecture
- Roadmap

---

## ⚙️ Configuration

### [.env.example](.env.example)
**Best for:** Setting up environment variables  
**Contents:**
- All required environment variables with descriptions
- Separate sections for standalone mode vs bot server
- Notes about ngrok URLs and OAuth setup

---

## 📂 Original Documentation

### [README.md](README.md)
**Best for:** Original setup guide (now superseded by above docs)  
**Contents:**
- Original standalone setup instructions
- Step-by-step for personal daily digests
- Cron scheduling

---

## 🗺️ Documentation Map

```
For teammates who want to USE the bot:
├── Start: HOW_TO_USE.md (2-step setup)
└── Share: SHARE_WITH_TEAMMATES.md (one-pager)

For YOU to announce the bot:
└── SLACK_ANNOUNCEMENT.md (copy-paste templates)

For developers who want to RUN the bot:
├── Quick: QUICK_START.md (commands only)
└── Detailed: TEAMMATE_GUIDE.md (everything)

For configuration:
└── .env.example (environment variables)
```

---

## 📋 Recommended Sharing Flow

1. **Announce to team:**
   - Copy a template from `SLACK_ANNOUNCEMENT.md`
   - Post in your team channel
   - Include the install link: https://jordan-spleenier-bigotedly.ngrok-free.dev/install

2. **For individuals who ask questions:**
   - Send them `HOW_TO_USE.md` or `SHARE_WITH_TEAMMATES.md`
   - Answer specific questions using `TEAMMATE_GUIDE.md`

3. **For developers who want to contribute:**
   - Point them to `QUICK_START.md` for setup
   - Share `TEAMMATE_GUIDE.md` for architecture details
   - GitHub repo: https://github.com/nicolewong-block/slack-summarizer

4. **After admin approval:**
   - Post the follow-up message from `SLACK_ANNOUNCEMENT.md`
   - Remind people they can now complete setup

---

## 🎨 Customization Tips

**Personalizing for your team:**
- Update the ngrok URL if it changes
- Add team-specific troubleshooting tips
- Include screenshots if helpful
- Add examples of actual summaries
- Customize announcement templates with your team's tone

**Keeping docs updated:**
- Update ngrok URL in all docs when it changes
- Add new troubleshooting items as issues arise
- Document new features as you add them
- Keep the roadmap section current

---

## ✅ Documentation Checklist

Use this when sharing with teammates:

- [ ] Bot server is running (`ps aux | grep bot.py`)
- [ ] ngrok tunnel is active and URL is current
- [ ] BASE_URL in `.env` matches ngrok URL
- [ ] Slack app redirect URL matches ngrok URL
- [ ] You've tested the OAuth flow yourself
- [ ] You've prepared for "request approval" questions from Block employees
- [ ] You have contact info ready (Slack handle, email)
- [ ] You've chosen which announcement template to use
- [ ] You know which channels to post in

---

**Questions about the documentation?**  
Slack **@Nicole Wong** or open an issue on GitHub!

---

*Documentation created: March 26, 2026*  
*Last updated: March 26, 2026*
