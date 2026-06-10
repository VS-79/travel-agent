from fastapi import APIRouter, Depends
from app.api.schemas import ChatRequest, ChatResponse
from app.memory.short_term import ShortTermMemory
from app.memory.long_term import LongTermMemory
from app.memory.session_store import SessionStore
from app.agent.agent import TravelAgent
from app.agent.prompts import SYSTEM_PROMPT
from app.agent.preference_extractor import extract_preferences
from app.dependencies import get_memory, get_long_term_memory, get_session_store, get_agent

router = APIRouter()

def build_system_prompt(user_id: str, long_term: LongTermMemory) -> str:
    preferences = long_term.get_preferences(user_id, "travel preferences", top_k=5)
    if not preferences:
        return SYSTEM_PROMPT

    prefs_text = "\n".join(f"- {p}" for p in preferences)
    return f"""{SYSTEM_PROMPT}

## Known User Preferences (from past sessions):
{prefs_text}

Use these preferences to personalise your recommendations without asking again."""

@router.post("/chat", response_model=ChatResponse)
async def chat(
    req: ChatRequest,
    mem: ShortTermMemory = Depends(get_memory),
    long_term: LongTermMemory = Depends(get_long_term_memory),
    store: SessionStore = Depends(get_session_store),
    travel_agent: TravelAgent = Depends(get_agent)
):
    session = store.get_or_create(req.user_id)
    mem.add(req.user_id, "user", req.message)
    system_prompt = build_system_prompt(req.user_id, long_term)
    preferences = long_term.get_preferences(req.user_id, "travel preferences", top_k=5)

    reply = travel_agent.run(
        user_message=req.message,
        conversation_history=mem.get(req.user_id),
        user_preferences=preferences,
        system_prompt=system_prompt
    )

    mem.add(req.user_id, "assistant", reply)

    extracted = extract_preferences(mem.get(req.user_id))
    for pref in extracted:
        long_term.store_preference(req.user_id, pref)

    store.update_session(req.user_id, "trip_count", session.get("trip_count", 0) + 1)

    return ChatResponse(user_id=req.user_id, reply=reply)