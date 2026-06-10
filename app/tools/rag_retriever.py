from langchain_core.tools import tool
from app.rag.retriever import multi_hop_retrieve

@tool
def rag_search(query: str) -> str:
    """Search the travel knowledge base for detailed information about 
    cities, attractions, culture, food, and travel tips. Use this for 
    in-depth local knowledge beyond web search."""
    try:
        city = None
        common_cities = ["tokyo", "paris", "singapore", "london", "bangkok", "barcelona", "dubai"]
        query_lower = query.lower()
        for c in common_cities:
            if c in query_lower:
                city = c.capitalize()
                break

        result = multi_hop_retrieve(query, city=city)

        if not result:
            return "No relevant information found in knowledge base."

        return result

    except Exception as e:
        return f"RAG search error: {str(e)}"