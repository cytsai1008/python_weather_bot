# 🌤️ Taiwan Weather Bot

A Discord bot that provides Taiwan weather forecasts with AI-powered lifestyle suggestions using data from Taiwan's Central Weather Administration (CWA) and Google's Gemini AI.

## ✨ Features

- 📍 **22 Taiwan Locations**: Select from all counties and major cities in Taiwan
- 🌡️ **Comprehensive Weather Data**: High/low temperatures, precipitation probability, comfort index
- 🤖 **AI Suggestions**: Personalized recommendations from Gemini 2.0 Flash for:
  - How the weather will feel
  - What to wear
  - What to prepare for outdoor activities
  - Lifestyle tips based on current conditions
- 💬 **Interactive UI**: Easy-to-use dropdown menu for location selection
- 📊 **Beautiful Embeds**: Clean, organized weather information display
- 🔧 **Flexible Installation**: Works as both User-Installable (use anywhere) and Guild-Installable (server bot)
- 💌 **DM Support**: Use the bot in direct messages or server channels

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Discord account and server
- API keys (see below)

### Required API Keys

1. **Discord Bot Token**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application
   - Go to "Bot" section and create a bot
   - Copy the token
   - Enable "Message Content Intent" in Bot settings
   - **⚠️ Important**: See [DISCORD_SETUP.md](DISCORD_SETUP.md) for detailed setup including User & Guild installation

2. **CWA API Key**
   - Visit [CWA OpenData Platform](https://opendata.cwa.gov.tw/index)
   - Register for an account
   - Get your API authorization key

3. **Gemini API Key**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create an API key for Gemini

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd python_weather_bot
```

2. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API keys
```

Your `.env` file should look like:
```env
DISCORD_BOT_TOKEN=your_discord_bot_token_here
CWA_API_KEY=your_cwa_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

5. Run the bot:
```bash
python bot.py
```

## 📖 Usage

### Commands

- `/weather` - Display location selector to get weather forecast (works in DMs and servers)
- `/help` - Show help information and bot features

### Installation Options

**Option 1: Guild Installation (Server Bot)**
1. Use the OAuth2 URL from Discord Developer Portal
2. Select your server (requires Manage Server permission)
3. Bot will be available to all server members
4. See [DISCORD_SETUP.md](DISCORD_SETUP.md) for detailed steps

**Option 2: User Installation (Personal Bot)**
1. Install the bot to your Discord account
2. Use it in DMs or ANY server (even where it's not installed as guild bot)
3. Commands follow you everywhere
4. See [DISCORD_SETUP.md](DISCORD_SETUP.md) for detailed steps

### How to Use

1. Type `/weather` in a server channel or DM

2. Select your desired location from the dropdown menu

3. Receive a detailed weather forecast with AI-powered suggestions!

4. Works anywhere - servers, DMs, group chats!

## 🏗️ Project Structure

```
python_weather_bot/
├── bot.py                  # Main Discord bot application
├── weather_service.py      # CWA OpenData API integration
├── gemini_service.py       # Gemini AI integration
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🔧 Configuration

### Supported Locations

The bot supports all 22 Taiwan counties and cities:
- 台北市, 新北市, 桃園市, 台中市, 台南市, 高雄市
- 基隆市, 新竹市, 新竹縣, 苗栗縣, 彰化縣, 南投縣
- 雲林縣, 嘉義市, 嘉義縣, 屏東縣, 宜蘭縣, 花蓮縣
- 台東縣, 澎湖縣, 金門縣, 連江縣

### Weather Data Fields

- **Temperature**: Daily high and low temperatures (°C)
- **Precipitation**: Probability of precipitation (%)
- **Weather Description**: Current weather conditions
- **Comfort Index**: Comfort level indicator

## 🤖 Gemini AI Integration

The bot uses Gemini 2.0 Flash to analyze weather data and provide:
- Temperature comfort analysis
- Clothing recommendations
- Outdoor activity preparation tips
- General lifestyle suggestions

The AI responses are:
- In Traditional Chinese (繁體中文)
- Concise and actionable (under 250 characters)
- Enhanced with relevant emojis
- Temperature-adaptive (0.7 temperature for natural responses)

## 🛠️ Development

### Adding New Features

To extend the bot's functionality:

1. **Add new weather parameters**: Modify `weather_service.py` to parse additional CWA API fields
2. **Customize AI prompts**: Edit `gemini_service.py` to change suggestion format
3. **Add new commands**: Add new `@client.tree.command` decorators in `bot.py`

### API Documentation

- [CWA OpenData API](https://opendata.cwa.gov.tw/dist/opendata-swagger.html)
- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Gemini API Documentation](https://ai.google.dev/docs)

## 🐛 Troubleshooting

### Common Issues

1. **Bot doesn't respond to commands**
   - Ensure the bot has proper permissions in your server
   - Check if slash commands are synced (wait a few minutes after starting)
   - Verify bot token is correct in `.env`

2. **Weather data not loading**
   - Verify your CWA API key is valid
   - Check API quota limits
   - Ensure location name matches exactly (use traditional characters)

3. **Gemini suggestions not working**
   - Verify Gemini API key is correct
   - Check API quota and billing
   - Review error messages in console

### Debug Mode

To enable detailed logging, add print statements or use Python's logging module:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📝 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

- Taiwan Central Weather Administration for providing open weather data
- Google for Gemini AI API
- Discord.py community

## 📧 Support

For issues and feature requests, please create an issue in the repository.

---

Made with ❤️ for Taiwan weather forecasting
