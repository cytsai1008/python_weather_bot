import discord
from discord import app_commands
from discord.ui import Select, View
import os
import asyncio
from dotenv import load_dotenv
from weather_service import WeatherService
from gemini_service import GeminiService

# Load environment variables from .env file
load_dotenv()


# Location mapping: Chinese (API) -> English
LOCATION_NAMES = {
    "臺北市": "Taipei City",
    "新北市": "New Taipei City",
    "桃園市": "Taoyuan City",
    "臺中市": "Taichung City",
    "臺南市": "Tainan City",
    "高雄市": "Kaohsiung City",
    "基隆市": "Keelung City",
    "新竹市": "Hsinchu City",
    "新竹縣": "Hsinchu County",
    "苗栗縣": "Miaoli County",
    "彰化縣": "Changhua County",
    "南投縣": "Nantou County",
    "雲林縣": "Yunlin County",
    "嘉義市": "Chiayi City",
    "嘉義縣": "Chiayi County",
    "屏東縣": "Pingtung County",
    "宜蘭縣": "Yilan County",
    "花蓮縣": "Hualien County",
    "臺東縣": "Taitung County",
    "澎湖縣": "Penghu County",
    "金門縣": "Kinmen County",
    "連江縣": "Lienchiang County",
}

# Display name mapping: Common spelling -> API name
LOCATION_ALIASES = {
    "台北市": "臺北市",
    "台中市": "臺中市",
    "台南市": "臺南市",
    "台東縣": "臺東縣",
    "taipei": "臺北市",
    "new taipei": "新北市",
    "taoyuan": "桃園市",
    "taichung": "臺中市",
    "tainan": "臺南市",
    "kaohsiung": "高雄市",
    "keelung": "基隆市",
    "hsinchu city": "新竹市",
    "hsinchu county": "新竹縣",
    "miaoli": "苗栗縣",
    "changhua": "彰化縣",
    "nantou": "南投縣",
    "yunlin": "雲林縣",
    "chiayi city": "嘉義市",
    "chiayi county": "嘉義縣",
    "pingtung": "屏東縣",
    "yilan": "宜蘭縣",
    "hualien": "花蓮縣",
    "taitung": "臺東縣",
    "penghu": "澎湖縣",
    "kinmen": "金門縣",
    "lienchiang": "連江縣",
}


def get_weather_emoji(weather_description: str, pop: str) -> str:
    """
    Get appropriate emoji based on weather conditions

    Args:
        weather_description: Weather description from CWA API
        pop: Probability of precipitation

    Returns:
        Appropriate weather emoji
    """
    desc = weather_description.lower() if weather_description else ""
    rain_prob = int(pop) if pop and pop.isdigit() else 0

    # Rain conditions
    if "大雨" in desc or "豪雨" in desc:
        return "🌧️"
    elif "雨" in desc or rain_prob >= 70:
        return "🌦️"
    elif "雷" in desc:
        return "⛈️"
    elif "陣雨" in desc or "雷陣雨" in desc:
        return "🌩️"

    # Cloud conditions
    elif "晴" in desc and "雲" in desc:
        return "⛅"
    elif "多雲" in desc or "陰" in desc:
        return "☁️"
    elif "晴" in desc:
        return "☀️"

    # Special conditions
    elif "霧" in desc:
        return "🌫️"
    elif "雪" in desc:
        return "🌨️"

    # Default
    return "🌤️"


class LocationSelect(Select):
    def __init__(self, weather_service, gemini_service):
        self.weather_service = weather_service
        self.gemini_service = gemini_service

        # Taiwan counties and major cities
        options = [
            discord.SelectOption(label="台北市", value="臺北市", description="Taipei City"),
            discord.SelectOption(label="新北市", value="新北市", description="New Taipei City"),
            discord.SelectOption(label="桃園市", value="桃園市", description="Taoyuan City"),
            discord.SelectOption(label="台中市", value="臺中市", description="Taichung City"),
            discord.SelectOption(label="台南市", value="臺南市", description="Tainan City"),
            discord.SelectOption(label="高雄市", value="高雄市", description="Kaohsiung City"),
            discord.SelectOption(label="基隆市", value="基隆市", description="Keelung City"),
            discord.SelectOption(label="新竹市", value="新竹市", description="Hsinchu City"),
            discord.SelectOption(label="新竹縣", value="新竹縣", description="Hsinchu County"),
            discord.SelectOption(label="苗栗縣", value="苗栗縣", description="Miaoli County"),
            discord.SelectOption(label="彰化縣", value="彰化縣", description="Changhua County"),
            discord.SelectOption(label="南投縣", value="南投縣", description="Nantou County"),
            discord.SelectOption(label="雲林縣", value="雲林縣", description="Yunlin County"),
            discord.SelectOption(label="嘉義市", value="嘉義市", description="Chiayi City"),
            discord.SelectOption(label="嘉義縣", value="嘉義縣", description="Chiayi County"),
            discord.SelectOption(label="屏東縣", value="屏東縣", description="Pingtung County"),
            discord.SelectOption(label="宜蘭縣", value="宜蘭縣", description="Yilan County"),
            discord.SelectOption(label="花蓮縣", value="花蓮縣", description="Hualien County"),
            discord.SelectOption(label="台東縣", value="臺東縣", description="Taitung County"),
            discord.SelectOption(label="澎湖縣", value="澎湖縣", description="Penghu County"),
            discord.SelectOption(label="金門縣", value="金門縣", description="Kinmen County"),
            discord.SelectOption(label="連江縣", value="連江縣", description="Lienchiang County"),
        ]

        super().__init__(
            placeholder="請選擇縣市 / Select a location...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        selected_location = self.values[0]

        try:
            embed = await create_weather_embed(
                selected_location,
                self.weather_service,
                self.gemini_service
            )
            await interaction.followup.send(embed=embed)

        except Exception as e:
            print(f"Error: {e}")
            await interaction.followup.send(f"❌ 發生錯誤: {str(e)}")


async def create_weather_embed(location: str, weather_service, gemini_service) -> discord.Embed:
    """
    Create weather forecast embed for a given location

    Args:
        location: Location name (Chinese API format)
        weather_service: WeatherService instance
        gemini_service: GeminiService instance

    Returns:
        Discord Embed with weather information
    """
    # Fetch weather data
    weather_data = await weather_service.get_weather_forecast(location)

    if not weather_data:
        raise ValueError(f"無法取得 {location} 的天氣資料")

    # Prepare combined period data for Gemini (both day and night periods)
    periods = weather_data.get('periods', [])
    combined_data = {
        'location': location,
        'periods': periods[:2]  # Pass both day and night periods
    }

    # Get Gemini suggestions with both periods
    gemini_suggestion = await gemini_service.get_weather_suggestions(
        location, combined_data
    )

    # Get dynamic weather emoji from first period
    first_period = periods[0] if periods else {}
    weather_emoji = get_weather_emoji(
        first_period.get('weather_description', ''),
        first_period.get('pop', '0')
    )

    # Get English name
    english_name = LOCATION_NAMES.get(location, "")
    title = f"{weather_emoji} {location}"
    if english_name:
        title += f" ({english_name})"
    title += " 天氣預報"

    # Create embed
    embed = discord.Embed(
        title=title,
        color=discord.Color.blue(),
        description="今日與今晚天氣預報"
    )

    # Add weather information for first 2 time periods only
    # (Today + Tonight if daytime, Tonight + Tomorrow if nighttime)
    periods = weather_data.get('periods', [])[:2]  # Only show first 2 periods

    for idx, period in enumerate(periods):
        period_label = period.get('period_label', f"時段 {idx + 1}")

        # Determine emoji based on period label
        if "白天" in period_label or "今天" in period_label:
            period_emoji = "☀️"
        elif "晚" in period_label:
            period_emoji = "🌙"
        else:
            period_emoji = "⏰"

        # Get weather emoji for this period
        period_weather_emoji = get_weather_emoji(
            period.get('weather_description', ''),
            period.get('pop', '0')
        )

        # Build the field content
        field_content = f"**時間:** {period.get('description', '')}\n"
        field_content += f"**天氣:** {period_weather_emoji} {period.get('weather_description', 'N/A')}\n"
        field_content += f"**溫度:** {period.get('low_temp', 'N/A')}°C ~ {period.get('high_temp', 'N/A')}°C\n"
        field_content += f"**降雨機率:** ☔ {period.get('pop', 'N/A')}%\n"
        field_content += f"**舒適度:** {period.get('comfort', 'N/A')}"

        embed.add_field(
            name=f"{period_emoji} {period_label}",
            value=field_content,
            inline=False
        )

    # Add Gemini AI suggestions
    if gemini_suggestion:
        embed.add_field(
            name="🤖 AI 生活建議",
            value=gemini_suggestion,
            inline=False
        )

    embed.set_footer(text="資料來源: 中央氣象署開放資料平台")

    return embed


class LocationView(View):
    def __init__(self, weather_service, gemini_service):
        super().__init__(timeout=180)
        self.add_item(LocationSelect(weather_service, gemini_service))


class WeatherBot(discord.Client):
    def __init__(self):
        # Only need default intents for slash commands (no privileged intents required)
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.weather_service = WeatherService()
        self.gemini_service = GeminiService()

    async def setup_hook(self):
        await self.tree.sync()
        print("Commands synced!")


client = WeatherBot()


@client.event
async def on_ready():
    print(f'✅ Bot logged in as {client.user}')
    print(f'Bot is ready to serve weather forecasts!')


async def location_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    """Autocomplete for location parameter"""
    current_lower = current.lower()

    # Search in both Chinese and English names
    choices = []
    for chinese, english in LOCATION_NAMES.items():
        # Match Chinese name or English name
        if current_lower in chinese.lower() or current_lower in english.lower():
            choices.append(
                app_commands.Choice(name=f"{chinese} ({english})", value=chinese)
            )

    # Also check aliases
    for alias, chinese in LOCATION_ALIASES.items():
        if current_lower in alias.lower() and chinese not in [c.value for c in choices]:
            english = LOCATION_NAMES.get(chinese, "")
            choices.append(
                app_commands.Choice(name=f"{chinese} ({english})", value=chinese)
            )

    # Limit to 25 choices (Discord limit)
    return choices[:25]


@client.tree.command(name="weather", description="查詢台灣各縣市今日與今晚天氣 / Get Taiwan weather forecast")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(location="選擇縣市 (可輸入中文或英文) / Select location (Chinese or English)")
@app_commands.autocomplete(location=location_autocomplete)
async def weather(interaction: discord.Interaction, location: str = None):
    """Display location selector or direct weather forecast"""

    if location:
        # Direct weather query
        await interaction.response.defer(thinking=True)

        try:
            # Normalize location (handle aliases)
            normalized_location = LOCATION_ALIASES.get(location.lower(), location)

            # Check if valid location
            if normalized_location not in LOCATION_NAMES:
                await interaction.followup.send(
                    f"❌ 找不到地點: {location}\n請使用 `/weather` 查看所有可用地點"
                )
                return

            # Create and send weather embed
            embed = await create_weather_embed(
                normalized_location,
                client.weather_service,
                client.gemini_service
            )
            await interaction.followup.send(embed=embed)

        except Exception as e:
            print(f"Error: {e}")
            await interaction.followup.send(f"❌ 發生錯誤: {str(e)}")

    else:
        # Show dropdown selector
        view = LocationView(client.weather_service, client.gemini_service)
        await interaction.response.send_message(
            "請選擇要查詢的縣市 📍\nPlease select a location:",
            view=view
        )


@client.tree.command(name="help", description="顯示使用說明 / Show help")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def help_command(interaction: discord.Interaction):
    """Show help information"""
    embed = discord.Embed(
        title="🤖 台灣天氣預報機器人",
        description="提供台灣各縣市今日與今晚天氣預報與AI生活建議",
        color=discord.Color.green()
    )

    embed.add_field(
        name="📖 使用方式",
        value=(
            "**方法 1:** `/weather` - 顯示選單選擇縣市\n"
            "**方法 2:** `/weather location:台北市` - 直接查詢\n"
            "💡 支援中英文輸入 (例: Taipei, 台北市)\n"
            "💬 可在伺服器頻道或私訊中使用"
        ),
        inline=False
    )

    embed.add_field(
        name="📊 提供資訊",
        value="• 今日與今晚天氣預報\n• 各時段高低溫度\n• 降雨機率\n• 天氣狀況\n• 舒適度\n• AI生活建議",
        inline=False
    )

    embed.add_field(
        name="🔧 安裝方式",
        value="• 伺服器安裝：管理員邀請至伺服器\n• 個人安裝：安裝至你的帳號，隨處使用",
        inline=False
    )

    await interaction.response.send_message(embed=embed)


def main():
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        raise ValueError("請設定 DISCORD_BOT_TOKEN 環境變數")

    client.run(token)


if __name__ == "__main__":
    main()
