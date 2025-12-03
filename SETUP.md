# 📋 Detailed Setup Guide

This guide will walk you through setting up the Taiwan Weather Bot from scratch.

## Step 1: Install Python

1. Download Python 3.8 or higher from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Verify installation:
```bash
python --version
```

## Step 2: Get Discord Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Give it a name (e.g., "Taiwan Weather Bot")
4. Go to the "Bot" tab on the left
5. Click "Add Bot" and confirm
6. Under "Privileged Gateway Intents", enable:
   - ✅ Message Content Intent
7. Click "Reset Token" and copy the token (save it securely!)

## Step 3: Invite Bot to Your Server

1. In Discord Developer Portal, go to "OAuth2" > "URL Generator"
2. Select scopes:
   - ✅ bot
   - ✅ applications.commands
3. Select bot permissions:
   - ✅ Send Messages
   - ✅ Embed Links
   - ✅ Use Slash Commands
4. Copy the generated URL and open it in your browser
5. Select your server and authorize

## Step 4: Get CWA API Key

1. Visit [CWA OpenData Platform](https://opendata.cwa.gov.tw/index)
2. Click "會員專區" (Member Area) or "註冊" (Register)
3. Complete registration with email verification
4. After login, go to "API授權碼" (API Authorization Code)
5. Copy your authorization key

## Step 5: Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Select or create a Google Cloud project
5. Copy the API key

## Step 6: Setup Project

1. Open terminal/command prompt
2. Navigate to the project directory:
```bash
cd C:\Users\CYTsai\Documents\GitHub\python_weather_bot
```

3. Create virtual environment:
```bash
# Windows
python -m venv venv

# Linux/Mac
python3 -m venv venv
```

4. Activate virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

5. Install dependencies:
```bash
pip install -r requirements.txt
```

## Step 7: Configure Environment Variables

1. Copy the example file:
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

2. Open `.env` file in a text editor
3. Replace the placeholder values with your actual API keys:

```env
DISCORD_BOT_TOKEN=your_discord_bot_token_here
CWA_API_KEY=your_cwa_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

4. Save the file

## Step 8: Run the Bot

### Option A: Using the run script (recommended)

**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

### Option B: Manual run

1. Ensure virtual environment is activated
2. Run:
```bash
python bot.py
```

## Step 9: Test the Bot

1. Open Discord and go to your server
2. Type `/weather` in any channel
3. Select a location from the dropdown
4. You should receive a weather forecast!

## Verification Checklist

Before running, make sure:
- ✅ Python 3.8+ is installed
- ✅ Virtual environment is created and activated
- ✅ All packages are installed (`pip list` shows discord.py, aiohttp, etc.)
- ✅ `.env` file exists and contains all three API keys
- ✅ Discord bot is invited to your server
- ✅ Bot has proper permissions in Discord
- ✅ Message Content Intent is enabled in Discord Developer Portal

## Common Issues and Solutions

### Issue: "Module not found" error
**Solution:** Make sure you activated the virtual environment and ran `pip install -r requirements.txt`

### Issue: Bot doesn't respond
**Solution:**
- Wait 1-2 minutes after starting the bot for slash commands to sync
- Check bot has permissions in your Discord server
- Verify Message Content Intent is enabled

### Issue: "Invalid token" error
**Solution:**
- Double-check your Discord bot token in `.env`
- Make sure there are no extra spaces or quotes
- Token should be exactly as shown in Discord Developer Portal

### Issue: Weather data not loading
**Solution:**
- Verify your CWA API key is correct
- Try with a different location
- Check CWA API status: https://opendata.cwa.gov.tw/

### Issue: Gemini suggestions not working
**Solution:**
- Verify Gemini API key is correct
- Check you have API quota available
- Make sure billing is enabled in Google Cloud Console

## File Structure Explanation

```
python_weather_bot/
├── bot.py              # Main Discord bot - handles commands and UI
├── weather_service.py  # Fetches data from CWA API
├── gemini_service.py   # Generates AI suggestions using Gemini
├── requirements.txt    # Python package dependencies
├── .env               # Your API keys (DO NOT share!)
├── .env.example       # Template for .env file
├── run.bat            # Windows startup script
├── run.sh             # Linux/Mac startup script
├── README.md          # Project documentation
└── SETUP.md           # This file
```

## Next Steps

After successful setup:
1. Customize the AI prompt in `gemini_service.py` if desired
2. Add more locations if needed in `bot.py`
3. Explore CWA API for additional weather data
4. Join Discord and test all features

## Getting Help

If you encounter issues:
1. Check the console output for error messages
2. Verify all API keys are correct
3. Review the troubleshooting section in README.md
4. Check API service status for Discord, CWA, and Gemini

## Security Reminders

- ⚠️ Never share your `.env` file
- ⚠️ Never commit `.env` to git (it's in .gitignore)
- ⚠️ Regenerate tokens if accidentally exposed
- ⚠️ Keep your API keys secure

---

You're all set! Enjoy your Taiwan Weather Bot! 🌤️
