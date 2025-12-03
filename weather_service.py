import aiohttp
import os
from datetime import datetime, timedelta
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
        params = {
            'Authorization': self.api_key,
            'locationName': location
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
        """Parse CWA API response into simplified weather data"""

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

            # Extract weather information
            weather_info = {}

            # Get today's forecast (first time period)
            for element in weather_elements:
                element_name = element['elementName']
                time_data = element['time'][0]  # First time period (today)

                if element_name == 'Wx':
                    # Weather description
                    weather_info['weather_description'] = time_data['parameter']['parameterName']

                elif element_name == 'PoP':
                    # Probability of Precipitation
                    weather_info['pop'] = time_data['parameter']['parameterName']

                elif element_name == 'MinT':
                    # Minimum temperature
                    weather_info['low_temp'] = time_data['parameter']['parameterName']

                elif element_name == 'MaxT':
                    # Maximum temperature
                    weather_info['high_temp'] = time_data['parameter']['parameterName']

                elif element_name == 'CI':
                    # Comfort Index
                    weather_info['comfort'] = time_data['parameter']['parameterName']

            # Add time period
            weather_info['start_time'] = time_data.get('startTime', '')
            weather_info['end_time'] = time_data.get('endTime', '')

            # Add description
            start_time = datetime.fromisoformat(weather_info['start_time'].replace('Z', '+00:00'))
            end_time = datetime.fromisoformat(weather_info['end_time'].replace('Z', '+00:00'))

            weather_info['description'] = f"預報時間: {start_time.strftime('%m/%d %H:%M')} - {end_time.strftime('%m/%d %H:%M')}"

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
