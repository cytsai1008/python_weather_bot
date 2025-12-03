import google.generativeai as genai
import os
from typing import Dict, Optional


class GeminiService:
    """Service to generate weather-based suggestions using Gemini AI"""

    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("請設定 GEMINI_API_KEY 環境變數")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    async def get_weather_suggestions(self, location: str, weather_data: Dict) -> Optional[str]:
        """
        Generate personalized suggestions based on weather data

        Args:
            location: Location name
            weather_data: Dictionary containing combined period information
                         Format: {'location': str, 'periods': [period1, period2]}

        Returns:
            String with AI-generated suggestions or None if error
        """
        try:
            # Construct prompt for Gemini with combined period data
            prompt = self._create_prompt(location, weather_data)

            # Generate response
            response = await self._generate_async(prompt)

            # If Gemini fails, use simple suggestions as fallback
            if response is None:
                print("Gemini failed, using simple suggestions fallback")
                return self.get_simple_suggestion(weather_data)

            return response

        except Exception as e:
            print(f"Error generating suggestions: {e}")
            # Use simple suggestions as fallback
            return self.get_simple_suggestion(weather_data)

    def _create_prompt(self, location: str, weather_data: Dict) -> str:
        """Create a detailed prompt for Gemini with combined day/night periods"""

        location = weather_data.get('location', location)
        periods = weather_data.get('periods', [])

        # Build period information
        period_info = []
        for period in periods:
            label = period.get('period_label', '')
            weather_desc = period.get('weather_description', 'N/A')
            high_temp = period.get('high_temp', 'N/A')
            low_temp = period.get('low_temp', 'N/A')
            pop = period.get('pop', 'N/A')
            comfort = period.get('comfort', 'N/A')

            period_text = f"""【{label}】
天氣: {weather_desc}
溫度: {low_temp}°C ~ {high_temp}°C
降雨機率: {pop}%
舒適度: {comfort}"""
            period_info.append(period_text)

        periods_text = "\n\n".join(period_info)

        prompt = f"""你是一個專業的氣象顧問和生活建議專家。根據以下的天氣資料，請用繁體中文提供簡潔實用的生活建議。

地點: {location}

{periods_text}

請根據這兩個時段的天氣差異，提供以下方面的建議（保持簡潔，每項2-3行）：
1. 🌡️ 體感與舒適度
2. 👔 穿著建議（如果日夜溫差大，請提醒洋蔥式穿搭）
3. ☂️ 外出準備（如果不同時段降雨機率不同，請特別提醒）
4. 💡 生活小提示

請用友善、口語化的方式回答，並使用適當的emoji讓內容更生動。保持回答簡潔明瞭，總長度控制在250字以內。"""

        return prompt

    async def _generate_async(self, prompt: str) -> str:
        """Generate response asynchronously"""
        import asyncio

        try:
            # Run the synchronous Gemini API call in a thread pool
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.7,
                        top_p=0.9,
                        top_k=40,
                        max_output_tokens=2000,  # Increased for longer responses
                    )
                )
            )

            # Check if response has valid content
            if not response.candidates:
                print("Gemini: No candidates returned")
                return "無法生成建議，請稍後再試。"

            candidate = response.candidates[0]

            # Check finish reason
            # 1 = STOP (success), 2 = MAX_TOKENS, 3 = SAFETY, 4 = RECITATION, 5 = OTHER
            if candidate.finish_reason == 3:  # SAFETY
                print("Gemini: Response blocked by safety filters")
                return "抱歉，無法為此天氣生成建議。"

            if candidate.finish_reason == 2:  # MAX_TOKENS
                print("Gemini: Response truncated (max tokens)")
                # Still try to return partial response

            # Try to get text from response
            try:
                if response.text:
                    return response.text.strip()
            except ValueError:
                # response.text failed, try to extract from parts
                if candidate.content and candidate.content.parts:
                    text_parts = [part.text for part in candidate.content.parts if hasattr(part, 'text')]
                    if text_parts:
                        return ''.join(text_parts).strip()

            return "無法生成建議，請稍後再試。"

        except Exception as e:
            print(f"Gemini API error: {e}")
            # Return simple suggestion as fallback
            return None  # Signal to use fallback

    def get_simple_suggestion(self, weather_data: Dict) -> str:
        """
        Fallback method to provide simple suggestions without AI
        Handles combined period data structure
        """
        periods = weather_data.get('periods', [])

        if not periods:
            return "無法提供建議"

        # Get data from first period for general suggestions
        first_period = periods[0]
        high_temp = int(first_period.get('high_temp', 25))
        low_temp = int(first_period.get('low_temp', 15))

        # Check max rain probability across all periods
        max_pop = max([int(p.get('pop', 0)) for p in periods])

        suggestions = []

        # Temperature-based suggestions
        if high_temp >= 30:
            suggestions.append("🌡️ 天氣炎熱，記得多補充水分")
            suggestions.append("👕 建議穿著輕薄透氣的衣物")
        elif high_temp >= 25:
            suggestions.append("🌡️ 天氣溫暖舒適")
            suggestions.append("👕 短袖或薄長袖即可")
        elif high_temp >= 20:
            suggestions.append("🌡️ 氣溫適中，早晚稍涼")
            suggestions.append("👔 建議洋蔥式穿搭")
        else:
            suggestions.append("🌡️ 天氣偏冷，注意保暖")
            suggestions.append("🧥 建議穿著外套或厚衣物")

        # Temperature difference check
        if len(periods) >= 2:
            temp_diff = abs(int(periods[0].get('high_temp', 20)) - int(periods[1].get('high_temp', 20)))
            if temp_diff >= 5:
                suggestions.append("🌡️ 日夜溫差較大，建議洋蔥式穿搭")

        # Rain-based suggestions (check all periods)
        if max_pop >= 70:
            suggestions.append("☂️ 降雨機率高，務必攜帶雨具")
        elif max_pop >= 30:
            suggestions.append("☂️ 可能下雨，建議帶傘備用")

        # Check if rain differs between periods
        if len(periods) >= 2:
            pop1 = int(periods[0].get('pop', 0))
            pop2 = int(periods[1].get('pop', 0))
            if abs(pop1 - pop2) >= 30:
                if pop2 > pop1:
                    suggestions.append(f"☂️ {periods[1].get('period_label', '稍後')}降雨機率較高，記得帶傘")
                else:
                    suggestions.append(f"☀️ {periods[1].get('period_label', '稍後')}天氣會轉好")

        return "\n".join(suggestions)
