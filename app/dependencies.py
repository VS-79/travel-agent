from anthropic import Anthropic
from app.memory.short_term import ShortTermMemory, memory
from app.memory.long_term import LongTermMemory, long_term_memory
from app.memory.session_store import SessionStore, session_store
from app.agent.agent import TravelAgent, agent
from app.config import settings

client = Anthropic(api_key=settings.anthropic_api_key)

def get_client() -> Anthropic:
    return client

def get_memory() -> ShortTermMemory:
    return memory

def get_long_term_memory() -> LongTermMemory:
    return long_term_memory

def get_session_store() -> SessionStore:
    return session_store

def get_agent() -> TravelAgent:
    return agent