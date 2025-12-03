# ⚡ Quick Start Guide

Get your Taiwan Weather Bot running in 5 minutes!

## Prerequisites Check

- ✅ Python 3.8+ installed
- ✅ Git installed (optional)
- ✅ Discord account
- ✅ Text editor

## Super Quick Setup

### 1. Install Dependencies (2 minutes)

```bash
# Navigate to project
cd python_weather_bot

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 2. Get API Keys (2 minutes)

**Discord Bot Token:**
- https://discord.com/developers/applications → New Application → Bot → Copy Token
- Enable "Message Content Intent"

**CWA API Key:**
- https://opendata.cwa.gov.tw/ → Register → Get Authorization Key

**Gemini API Key:**
- https://makersuite.google.com/app/apikey → Create API Key

### 3. Configure (1 minute)

```bash
# Copy example file
copy .env.example .env    # Windows
cp .env.example .env      # Mac/Linux

# Edit .env and paste your keys
DISCORD_BOT_TOKEN=your_token_here
CWA_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
```

### 4. Run!

```bash
# Windows
run.bat

# Mac/Linux
./run.sh

# Or manually
python bot.py
```

### 5. Install Bot (Choose One or Both!)

**📋 For full setup guide:** See [DISCORD_SETUP.md](DISCORD_SETUP.md)

**Quick Guild Install (Server Bot):**
1. Go to Discord Developer Portal → OAuth2 → URL Generator
2. Select: `bot` + `applications.commands`
3. Permissions: `Send Messages` + `Embed Links` + `Use Slash Commands`
4. Copy URL and open in browser
5. Select your server

**User Install (Personal Bot):**
- Enable in Discord Developer Portal → Installation
- Install to your account to use anywhere (DMs, all servers)
- See [DISCORD_SETUP.md](DISCORD_SETUP.md) for details

### 6. Test

**In a server channel or DM:**
```
/weather
```

Select a location and enjoy! 🎉

## Troubleshooting

**Bot not responding?**
- Wait 1-2 minutes for command sync
- Check bot permissions
- Verify token in .env

**API errors?**
- Double-check all 3 API keys
- Ensure no extra spaces in .env
- Test each API separately

## That's It!

Your bot is now running. Check out README.md for detailed features and customization options.

---

Need help? See SETUP.md for detailed instructions.
