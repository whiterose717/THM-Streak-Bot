# THM Streak Bot

Automatically maintains your TryHackMe daily streak using GitHub Actions. 100% free, no paid services.

## Features

- **Daily Streak Maintenance** — Runs automatically at 4:30 PM Sri Lanka time
- **Telegram Control** — Control the bot from your phone
- **Room Completion** — Solve all questions in any room
- **Free Proxy Support** — Works on GitHub Actions (bypasses Vercel blocks)
- **Writeup-Based Answers** — Uses community writeups for accurate answers

## Commands

| Command | Description |
|---------|-------------|
| `/now` | Run streak bot (maintain streak) |
| `/new` | Solve a brand NEW challenge |
| `/complete` | Solve ALL questions in a random uncompleted room |
| `/complete blue` | Solve ALL questions in a specific room |
| `/logs` | Get latest run logs |
| `/status` | Check bot status |
| `/help` | Show help |

## Setup Guide

### Prerequisites
- GitHub account
- TryHackMe account
- Telegram account

### Step 1: Fork the Repository

1. Go to the repository page
2. Click "Fork" to create your own copy

### Step 2: Create GitHub Secrets

Go to your fork → Settings → Secrets and variables → Actions → New repository secret

Create these secrets:

| Secret Name | Value |
|-------------|-------|
| `THM_EMAIL` | Your TryHackMe email |
| `THM_PASSWORD` | Your TryHackMe password |
| `TELEGRAM_BOT_TOKEN` | Bot token from @BotFather |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID |
| `THM_GH_PAT` | GitHub PAT with `repo` and `workflow` scopes |
| `THM_FIREFOX_COOKIES` | Base64-encoded Firefox cookies (see Step 3) |

### Step 3: Export Firefox Cookies

1. Install Firefox on your machine
2. Login to tryhackme.com in Firefox
3. Run the cookie export script:

```bash
# Install dependencies
pip install requests

# Export cookies (run this on your machine with Firefox)
python3 export_cookies.py
```

4. Copy the base64 output
5. Go to GitHub Secrets → `THM_FIREFOX_COOKIES` → Paste the base64 string

### Step 4: Create Telegram Bot

1. Open Telegram, search for @BotFather
2. Send `/newbot` and follow the instructions
3. Copy the bot token → Add as `TELEGRAM_BOT_TOKEN` secret
4. Send a message to your bot
5. Visit `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
6. Find your chat ID in the response → Add as `TELEGRAM_CHAT_ID` secret

### Step 5: Create GitHub PAT

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token"
3. Select scopes: `repo` and `workflow`
4. Copy the token → Add as `THM_GH_PAT` secret

### Step 6: Enable GitHub Actions

1. Go to your fork → Actions
2. Click "I understand my workflows, go ahead and enable them"
3. The bot will now run automatically every day at 4:30 PM Sri Lanka time

## How It Works

1. **Cookie-Based Auth** — Uses Firefox cookies (not username/password)
2. **Free Proxy Discovery** — Automatically finds working HTTPS proxies
3. **Known Rooms Database** — 17 rooms with verified answers hardcoded
4. **Writeup Fallback** — Fetches answers from thmrevenant GitHub repo
5. **Smart Matching** — Matches THM questions to writeup answers

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Telegram Bot    │────▶│  GitHub Actions   │────▶│  TryHackMe API  │
│  (Listener)      │     │  (THM Bot)        │     │  (via Proxy)    │
└─────────────────┘     └──────────────────┘     └─────────────────┘
        │                        │                        │
        │                        │                        │
        ▼                        ▼                        ▼
   User Commands          Workflow Runs            Streak Maintained
```

## Troubleshooting

### Bot not responding in Telegram
- Check if the Telegram Listener workflow is running
- Verify `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` secrets
- Send `/status` to check bot status

### Streak not maintained
- Check GitHub Actions logs
- Cookies may be expired — re-export and update `THM_FIREFOX_COOKIES`
- Check if proxy is working (look at logs for proxy errors)

### /complete not working
- Ensure `THM_GH_PAT` has `workflow` scope
- Check if listener has `actions: write` permission
- Look for error messages in Telegram

## Cookie Expiration

Firefox cookies expire after ~30 days. When they expire:

1. Login to tryhackme.com in Firefox
2. Re-run `export_cookies.py`
3. Update `THM_FIREFOX_COOKIES` secret

## Room Database

The bot includes 17 rooms with verified answers:

| Room | Questions | Difficulty |
|------|-----------|------------|
| blue | 11 | Easy |
| ice | 22 | Easy |
| kenobi | 11 | Easy |
| couch | 9 | Easy |
| internal | 2 | Easy |
| overpass | 2 | Easy |
| startup | 3 | Easy |
| rocket | 2 | Easy |
| res | 7 | Easy |
| lazyadmin | 2 | Easy |
| hackernote | 10 | Easy |
| temple | 2 | Easy |
| wonderland | 2 | Easy |
| welcome | 1 | Easy |
| skynet | 5 | Easy |
| snort | 9 | Medium |
| nmap | 42 | Easy |

## License

MIT License - Free to use and modify

## Credits

- Writeup answers from [thmrevenant/tryhackme](https://github.com/thmrevenant/tryhackme)
- Free proxy lists from [proxyscrape](https://proxyscrape.com)
