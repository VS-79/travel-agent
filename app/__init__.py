from app.tools.weather import get_weather
from app.tools.search import search_web
from app.tools.hotels import search_hotels
from app.tools.rag_retriever import rag_search

TOOLS = [get_weather, search_web, search_hotels, rag_search]