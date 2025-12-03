# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Discord bot providing Taiwan weather forecasts with AI-powered lifestyle suggestions using:
- Taiwan Central Weather Administration (CWA) OpenData API for weather data
- Google Gemini AI for personalized recommendations
- Discord.py for bot functionality

## Development Commands

### Setup and Running
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys: DISCORD_BOT_TOKEN, CWA_API_KEY, GEMINI_API_KEY

# Run the bot
python bot.py
```

### Docker
```bash
# Build image
docker build -t taiwan-weather-bot .

# Run container
docker run -d --env-file .env --name weather-bot taiwan-weather-bot

# Using docker-compose
docker-compose up -d
```

## Architecture

### Core Components (3 files)

**bot.py** - Discord bot entry point and UI layer
- Handles Discord slash commands (`/weather`, `/help`)
- Manages interactive UI (dropdown selectors, embeds)
- Orchestrates data flow between weather_service and gemini_service
- Key function: `create_weather_embed()` - combines weather data + AI suggestions into Discord embed

**weather_service.py** - CWA API integration and time logic
- Fetches weather from F-C0032-001 endpoint (36-hour forecast)
- **Critical timezone handling**: All time logic uses UTC+8 (Taiwan timezone)
- Smart API requests: Only fetches needed time periods (not full 36 hours)
- Period labeling logic: Converts calendar periods to user-friendly labels

**gemini_service.py** - AI suggestion generation
- Uses Gemini 2.0 Flash model
- Receives combined day/night period data for context-aware suggestions
- Has fallback logic if AI fails (rule-based suggestions)

### Weather Data Flow

1. **API Request** (`weather_service.py:18-86`)
   - Determines current time period (daytime: 6:00-17:59, nighttime: 18:00-5:59)
   - Calculates appropriate `timeFrom`/`timeTo` to catch current period
   - Example at 18:42: requests from 18:00 (not 18:42) to catch period start

2. **Data Parsing** (`weather_service.py:88-216`)
   - Extracts 5 weather elements: Wx, PoP, MinT, MaxT, CI
   - Processes multiple time periods (typically 2-3 returned)
   - Applies period labeling logic (see Time Period Labeling below)

3. **AI Processing** (`gemini_service.py:17-87`)
   - Receives combined period data: `{'location': str, 'periods': [period1, period2]}`
   - Gemini sees both periods to provide context-aware suggestions
   - Example: "Today is sunny but bring umbrella for tonight"

4. **Display** (`bot.py:169-257`)
   - Shows first 2 periods only (user sees today + tonight OR tonight + tomorrow)
   - Creates Discord embed with weather data + AI suggestions

### Time Period Labeling Logic

**Critical behavior** (`weather_service.py:167-205`):

The API returns periods with start times (06:00 or 18:00), but labels must reflect user's current time:

- **Before midnight (18:00-23:59)**: Period starting 18:00 today = "今晚" (tonight)
- **After midnight (00:00-05:59)**: Period starting 18:00 yesterday = "昨晚" (last night)
- **After midnight (00:00-05:59)**: Period starting 06:00 today = "今天白天" (today daytime)

Key insight: After midnight, the night period that started yesterday becomes "last night" even though you're still in it.

### API Request Strategy

**Problem solved**: API periods start at fixed times (06:00, 18:00), but requests at arbitrary times (e.g., 18:42) would miss the current period.

**Solution** (`weather_service.py:35-55`):
- Round down to period start time
- Example: At 18:42, request from 18:00 (not 18:42)
- At 03:00, request from 18:00 yesterday

This ensures the current period is always included in the response.

### Timezone Handling

**All datetime operations use explicit UTC+8**:
```python
taiwan_tz = timezone(timedelta(hours=8))
current_time = datetime.now(taiwan_tz)
```

Never assume `datetime.now()` is in Taiwan time - the server may be anywhere. Always use `taiwan_tz`.

## Environment Variables

Required in `.env`:
- `DISCORD_BOT_TOKEN` - From Discord Developer Portal
- `CWA_API_KEY` - From https://opendata.cwa.gov.tw/
- `GEMINI_API_KEY` - From https://makersuite.google.com/

## Discord Bot Configuration

Bot requires specific Discord setup (see DISCORD_SETUP.md):
- **Scopes**: `bot`, `applications.commands`
- **Bot Permissions**: Send Messages, Embed Links, Use Application Commands
- **Privileged Intents**: None required
- **Installation contexts**: Both guild (servers) and user (DMs)

## Key Implementation Details

### Weather Data Structure

After parsing, data structure:
```python
{
  'periods': [
    {
      'period_label': '今晚',
      'weather_description': '陰天',
      'high_temp': '18',
      'low_temp': '17',
      'pop': '10',
      'comfort': '稍有寒意',
      'start_time': '2025-12-03 18:00:00',
      'end_time': '2025-12-04 06:00:00',
      'description': '12/03 18:00 - 12/04 06:00'
    },
    # ... more periods
  ]
}
```

### Gemini Prompt Strategy

Gemini receives **both periods** formatted as:
```
【今晚】
天氣: 陰天
溫度: 17°C ~ 18°C
降雨機率: 10%
舒適度: 稍有寒意

【明天白天】
天氣: 陰時多雲
溫度: 17°C ~ 19°C
降雨機率: 20%
舒適度: 稍有寒意
```

This allows AI to detect temperature changes, rain timing, and provide period-specific advice.

### Location Handling

Bot supports 22 Taiwan locations with multiple name formats:
- API names: "臺北市", "臺中市" (traditional characters with 臺)
- User input: "台北市", "Taipei", "taipei city" (flexible)
- Aliases mapped in `LOCATION_ALIASES` dict
- Autocomplete searches both Chinese and English names

## Debugging Notes

### Common Issues

**Period labels wrong after midnight**: Check timezone - ensure using `taiwan_tz` not `datetime.now()`

**Missing "tonight" period at 6 PM**: Verify API request starts from 18:00, not current time

**Gemini suggestions generic**: Ensure `combined_data` structure includes both periods with 'periods' key

### Testing Time-Dependent Logic

Simulate different times by replacing:
```python
current_time = datetime.now(taiwan_tz).replace(hour=X, minute=Y)
```

Test critical times: 00:00 (midnight), 06:00 (day start), 18:00 (night start), 23:59 (before midnight)
