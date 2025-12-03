import aiohttp
import os
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict


class WeatherService:
    """Service to fetch weather data from Taiwan CWA OpenData API"""

    def __init__(self):
        self.api_key = os.getenv('CWA_API_KEY')
        if not self.api_key:
            raise ValueError("請設定 CWA_API_KEY 環境變數")

        # CWA OpenData API endpoint for 36-hour weather forecast
        self.base_url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"

    async def get_weather_forecast(self, location: str) -> Optional[Dict]:
        """
        Fetch weather forecast for a specific location in Taiwan

        Args:
            location: Location name (縣市名稱)

        Returns:
            Dictionary containing weather data or None if not found
        """
        # Get current time in UTC+8 (Taiwan timezone)
        taiwan_tz = timezone(timedelta(hours=8))
        current_time = datetime.now(taiwan_tz)

        # Determine if it's daytime (6:00-17:59) or nighttime (18:00-5:59)
        is_daytime = 6 <= current_time.hour < 18

        # Adjust start time to catch the current period
        # API periods start at 06:00 and 18:00, so we need to request from the period start
        if is_daytime:
            # Start from 06:00 today to catch current daytime period
            start_time = current_time.replace(hour=6, minute=0, second=0, microsecond=0)
            # Fetch until tomorrow 00:00 (covers today + tonight)
            tomorrow = current_time.date() + timedelta(days=1)
            end_time = datetime.combine(tomorrow, datetime.min.time(), tzinfo=taiwan_tz)
        else:
            # Start from 18:00 today to catch current night period
            if current_time.hour >= 18:
                # After 6 PM - start from 18:00 today
                start_time = current_time.replace(hour=18, minute=0, second=0, microsecond=0)
            else:
                # Before 6 AM - start from 18:00 yesterday
                yesterday = current_time.date() - timedelta(days=1)
                start_time = datetime.combine(yesterday, datetime.min.time(), tzinfo=taiwan_tz).replace(hour=18)

            # Fetch until day after tomorrow 00:00 (covers tonight + all of tomorrow)
            day_after_tomorrow = current_time.date() + timedelta(days=2)
            end_time = datetime.combine(day_after_tomorrow, datetime.min.time(), tzinfo=taiwan_tz)

        # Format times for API (format: yyyy-MM-ddThh:mm:ss)
        time_from = start_time.strftime('%Y-%m-%dT%H:%M:%S')
        time_to = end_time.strftime('%Y-%m-%dT%H:%M:%S')

        params = {
            'Authorization': self.api_key,
            'locationName': location,
            'timeFrom': time_from,
            'timeTo': time_to
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status != 200:
                        print(f"API Error: Status {response.status}")
                        return None

                    data = await response.json()

                    if not data.get('success'):
                        print(f"API returned success=False")
                        return None

                    # Parse the weather data
                    return self._parse_weather_data(data, location)

        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return None

    def _parse_weather_data(self, data: dict, location: str) -> Dict:
        """
        Parse CWA API response into simplified weather data

        The API returns 36-hour forecast data divided into 3 time periods (each ~12 hours)
        Timestamps are in Taiwan time (UTC+8) format: "YYYY-MM-DD HH:MM:SS"

        Weather elements:
        - Wx: Weather phenomenon (天氣現象)
        - PoP: Probability of Precipitation (降雨機率)
        - MinT: Minimum Temperature (最低溫度)
        - MaxT: Maximum Temperature (最高溫度)
        - CI: Comfort Index (舒適度)
        """

        try:
            records = data['records']['location']

            # Find the location data
            location_data = None
            for loc in records:
                if loc['locationName'] == location:
                    location_data = loc
                    break

            if not location_data:
                return None

            weather_elements = location_data['weatherElement']


            # Extract weather information for all 3 time periods
            weather_info = {
                'periods': []  # Will store data for each time period
            }

            # Get the number of time periods (should be 3 for 36-hour forecast)
            num_periods = len(weather_elements[0]['time']) if weather_elements else 0

            # Extract data for each time period
            for period_idx in range(num_periods):
                period_data = {}

                for element in weather_elements:
                    element_name = element['elementName']
                    time_data = element['time'][period_idx]

                    if element_name == 'Wx':
                        # Weather description
                        period_data['weather_description'] = time_data['parameter']['parameterName']

                    elif element_name == 'PoP':
                        # Probability of Precipitation
                        period_data['pop'] = time_data['parameter']['parameterName']

                    elif element_name == 'MinT':
                        # Minimum temperature
                        period_data['low_temp'] = time_data['parameter']['parameterName']

                    elif element_name == 'MaxT':
                        # Maximum temperature
                        period_data['high_temp'] = time_data['parameter']['parameterName']

                    elif element_name == 'CI':
                        # Comfort Index
                        period_data['comfort'] = time_data['parameter']['parameterName']

                # Add time period
                period_data['start_time'] = time_data.get('startTime', '')
                period_data['end_time'] = time_data.get('endTime', '')

                # Parse timestamps (API returns in format "YYYY-MM-DD HH:MM:SS" already in Taiwan time)
                start_time_tw = datetime.strptime(period_data['start_time'], '%Y-%m-%d %H:%M:%S')
                end_time_tw = datetime.strptime(period_data['end_time'], '%Y-%m-%d %H:%M:%S')

                # Get current time in Taiwan timezone (UTC+8)
                taiwan_tz = timezone(timedelta(hours=8))
                current_time_tw = datetime.now(taiwan_tz).replace(tzinfo=None)

                # Determine period label based on date and time
                hour = start_time_tw.hour
                is_daytime = 6 <= hour < 18

                # Check if it's today, tonight, or tomorrow
                if start_time_tw.date() == current_time_tw.date():
                    # Same date
                    if is_daytime:
                        period_label = "今天白天"
                    else:
                        period_label = "今晚"
                elif start_time_tw.date() == (current_time_tw + timedelta(days=1)).date():
                    # Tomorrow
                    if is_daytime:
                        period_label = "明天白天"
                    else:
                        period_label = "明晚"
                else:
                    # Generic labels
                    if is_daytime:
                        period_label = "白天"
                    else:
                        period_label = "晚上"

                period_data['period_label'] = period_label
                period_data['description'] = f"{start_time_tw.strftime('%m/%d %H:%M')} - {end_time_tw.strftime('%m/%d %H:%M')}"

                weather_info['periods'].append(period_data)

            return weather_info

        except Exception as e:
            print(f"Error parsing weather data: {e}")
            return None

    async def get_detailed_forecast(self, location: str) -> Optional[Dict]:
        """
        Get more detailed weather information including wind, humidity, etc.
        This uses a different API endpoint for more detailed data
        """
        # Alternative endpoint for detailed forecast (if needed)
        detailed_url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-089"

        params = {
            'Authorization': self.api_key,
            'locationName': location
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(detailed_url, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    return None
        except Exception as e:
            print(f"Error fetching detailed forecast: {e}")
            return None
