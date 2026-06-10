from app.tools import TOOLS
from app.tools.weather import get_weather
from app.tools.search import search_web
from app.tools.hotels import search_hotels

TOOL_MAP = {tool.name: tool for tool in TOOLS}

def execute_task(task: dict, city: str, preferences: list = None) -> dict:
    """Executes a single planning sub-task using the appropriate tool."""
    
    task_name = task.get("task")
    prefs_text = ", ".join(preferences) if preferences else "no specific preferences"
    result = ""

    try:
        if task_name == "check_weather":
            result = get_weather.invoke({"city": city})

        elif task_name == "find_attractions":
            query = f"top attractions and things to do in {city}"
            if preferences:
                query += f" for someone who {prefs_text}"
            result = search_web.invoke({"query": query})

        elif task_name == "find_restaurants":
            query = f"best restaurants in {city}"
            if preferences:
                query += f" for someone who enjoys {prefs_text}"
            result = search_web.invoke({"query": query})

        elif task_name == "find_hotels":
            budget = "luxury" if any("luxury" in p.lower() for p in (preferences or [])) else "moderate"
            result = search_hotels.invoke({"city": city, "budget": budget})

        elif task_name == "build_itinerary":
            result = f"Compiling 2-day itinerary for {city} based on gathered information"

        else:
            query = f"{task.get('description', '')} in {city}"
            result = search_web.invoke({"query": query})

    except Exception as e:
        result = f"Task {task_name} failed: {str(e)}"

    return {
        "task": task_name,
        "description": task.get("description"),
        "result": result
    }

def execute_plan(plan: list, city: str, preferences: list = None) -> list:
    """Executes all tasks in a plan and returns results."""
    results = []
    for task in plan:
        print(f"DEBUG: Executing task - {task.get('task')}")
        result = execute_task(task, city, preferences)
        results.append(result)
    return results