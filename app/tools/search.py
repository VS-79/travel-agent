from langchain_core.tools import tool
from tavily import TavilyClient
from app.config import settings

@tool
def search_web(query: str) -> str:
    """Search the web for travel information, attractions, restaurants, 
    and things to do in a city. Use this to find current recommendations."""
    try:
        client = TavilyClient(api_key=settings.tavily_api_key)
        response = client.search(query=query, max_results=5)

        results = []
        for r in response.get("results", []):
            results.append(f"- {r['title']}: {r['content'][:200]}")

        return "\n".join(results) if results else "No results found."

    except Exception as e:
        return f"Search tool error: {str(e)}"