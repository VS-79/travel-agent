import json
from anthropic import Anthropic
from app.config import settings

client = Anthropic(api_key=settings.anthropic_api_key)

def extract_preferences(conversation: list) -> list:
    if not conversation:
        print("DEBUG: No conversation to extract from")
        return []

    convo_text = ""
    for msg in conversation:
        if isinstance(msg["content"], str):
            convo_text += f"{msg['role'].upper()}: {msg['content']}\n"

    if not convo_text.strip():
        print("DEBUG: Conversation text is empty after filtering")
        return []

    try:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=500,
            system="""Extract user travel preferences from this conversation.
Return a JSON array of preference strings only.
Example: ["prefers budget hotels", "loves Japanese food", "interested in culture"]
Return ONLY the JSON array with no markdown, no backticks, no extra text.""",
            messages=[{"role": "user", "content": convo_text}]
        )

        text = response.content[0].text.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        print(f"DEBUG: Claude returned (cleaned): {text}")

        preferences = json.loads(text)
        print(f"DEBUG: Extracted preferences: {preferences}")

        if isinstance(preferences, list):
            return preferences
        return []

    except json.JSONDecodeError as e:
        print(f"DEBUG: JSON parse error: {e}")
        return []
    except Exception as e:
        print(f"DEBUG: Extraction error: {e}")
        return []