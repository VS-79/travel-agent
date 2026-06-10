import requests
from langchain_core.tools import tool
from app.config import settings

@tool
def get_weather(city: str) -> str:
    """Get current weather and forecast for a city. 
    Use this before recommending outdoor activities or planning a trip itinerary."""
    try:
        url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": city,
            "appid": settings.openweather_api_key,
            "units": "metric",
            "cnt": 6
        }
        r = requests.get(url, params=params)
        data = r.json()

        if "list" not in data:
            return f"Could not fetch weather for {city}. Error: {data.get('message', 'unknown')}"

        result = f"Weather forecast for {city}:\n"
        for item in data["list"]:
            result += f"- {item['dt_txt']}: {item['main']['temp']}°C, {item['weather'][0]['description']}\n"

        return result

    except Exception as e:
        return f"Weather tool error: {str(e)}"