from fastapi import APIRouter, Depends
from app.memory.long_term import LongTermMemory
from app.dependencies import get_long_term_memory

router = APIRouter()

@router.get("/preferences/{user_id}")
def get_user_preferences(
    user_id: str,
    long_term: LongTermMemory = Depends(get_long_term_memory)
):
    preferences = long_term.get_preferences(user_id, "travel preferences", top_k=10)
    return {"user_id": user_id, "preferences": preferences}