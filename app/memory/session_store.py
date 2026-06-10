from typing import Optional
from datetime import datetime

class SessionStore:
    def __init__(self):
        self._sessions: dict = {}

    def create_session(self, user_id: str):
        self._sessions[user_id] = {
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "preferences": {},
            "last_city": None,
            "trip_count": 0
        }

    def get_session(self, user_id: str) -> Optional[dict]:
        return self._sessions.get(user_id)

    def update_session(self, user_id: str, key: str, value):
        if user_id not in self._sessions:
            self.create_session(user_id)
        self._sessions[user_id][key] = value

    def get_or_create(self, user_id: str) -> dict:
        if user_id not in self._sessions:
            self.create_session(user_id)
        return self._sessions[user_id]

session_store = SessionStore()