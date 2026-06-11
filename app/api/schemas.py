from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    user_id: str
    message: str
    budget: Optional[str] = None
    pet_friendly: Optional[bool] = False
    language: Optional[str] = None

class ChatResponse(BaseModel):
    user_id: str
    reply: str

class TripRequest(BaseModel):
    user_id: str
    city: str
    budget: Optional[str] = "moderate"
    travel_style: Optional[str] = "general"
    pet_friendly: Optional[bool] = False