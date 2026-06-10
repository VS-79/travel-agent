from anthropic import Anthropic
from app.config import settings

client = Anthropic(api_key=settings.anthropic_api_key)

def create_plan(user_message: str, city: str = None) -> list:
    """Breaks down a travel request into sub-tasks."""
    
    prompt = f"""You are a travel planning coordinator. 
Break down this travel request into specific sub-tasks that need to be completed.

User request: {user_message}
City: {city or 'unknown'}

Return a JSON array of sub-tasks in this exact format with no markdown or backticks:
[
  {{"task": "check_weather", "description": "Get weather forecast for the city"}},
  {{"task": "find_attractions", "description": "Search for top attractions"}},
  {{"task": "find_restaurants", "description": "Search for best restaurants"}},
  {{"task": "find_hotels", "description": "Search for accommodation options"}},
  {{"task": "build_itinerary", "description": "Compile everything into a 2-day itinerary"}}
]

Only include relevant tasks based on the request."""

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    import json
    try:
        text = response.content[0].text.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except:
        return [
            {"task": "check_weather", "description": "Get weather forecast"},
            {"task": "find_attractions", "description": "Search for attractions"},
            {"task": "find_hotels", "description": "Search for hotels"},
            {"task": "build_itinerary", "description": "Build 2-day itinerary"}
        ]