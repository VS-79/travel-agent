from anthropic import Anthropic
from app.config import settings
from app.agent.planner import create_plan
from app.agent.executor import execute_plan
from app.agent.prompts import SYSTEM_PROMPT
from app.tools import TOOLS

class TravelAgent:
    def __init__(self):
        self.client = Anthropic(api_key=settings.anthropic_api_key)
        self.tools = TOOLS

    def extract_city(self, message: str) -> str:
        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=50,
            messages=[{
                "role": "user",
                "content": f"Extract only the city name from this message, return just the city name with no other text: {message}"
            }]
        )
        return response.content[0].text.strip()

    def format_tool_results(self, results: list) -> str:
        formatted = ""
        for r in results:
            formatted += f"\n## {r['task'].replace('_', ' ').title()}\n"
            formatted += f"{r['result']}\n"
        return formatted

    def run(
        self,
        user_message: str,
        conversation_history: list,
        user_preferences: list = None,
        system_prompt: str = None,
        pet_friendly: bool = False
    ) -> str:
        city = self.extract_city(user_message)
        print(f"DEBUG: Detected city - {city}")

        plan = create_plan(user_message, city)
        print(f"DEBUG: Plan created - {[t['task'] for t in plan]}")

        task_results = execute_plan(plan, city, user_preferences, pet_friendly)
        tool_context = self.format_tool_results(task_results)

        pet_note = "\nIMPORTANT: This is a PET-FRIENDLY trip. Only recommend pet-friendly hotels, outdoor attractions and restaurants with outdoor seating. Include a Pet Travel Tips section." if pet_friendly else ""

        enriched_prompt = f"""{user_message}{pet_note}

I have already gathered the following information for you:
{tool_context}

Using this information, please provide a comprehensive and personalized response."""

        messages = conversation_history[:-1] + [
            {"role": "user", "content": enriched_prompt}
        ]

        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2048,
            system=system_prompt or SYSTEM_PROMPT,
            messages=messages
        )

        return response.content[0].text

agent = TravelAgent()