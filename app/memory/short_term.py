import json
import redis
from app.config import settings

class ShortTermMemory:
    def __init__(self):
        self.use_redis = bool(settings.redis_url)
        if self.use_redis:
            try:
                self.client = redis.from_url(
                    settings.redis_url,
                    decode_responses=True,
                    ssl_cert_reqs=None
                )
                self.client.ping()
                print("DEBUG: Connected to Redis for short-term memory")
            except Exception as e:
                print(f"DEBUG: Redis connection failed, using in-memory: {e}")
                self.use_redis = False
                self._store = {}
        else:
            self._store = {}
            print("DEBUG: Using in-memory short-term memory")

    def add(self, user_id: str, role: str, content: str):
        if self.use_redis:
            history = self.get(user_id)
            history.append({"role": role, "content": content})
            self.client.setex(
                f"session:{user_id}",
                3600,
                json.dumps(history)
            )
        else:
            if user_id not in self._store:
                self._store[user_id] = []
            self._store[user_id].append({"role": role, "content": content})

    def get(self, user_id: str) -> list:
        if self.use_redis:
            try:
                data = self.client.get(f"session:{user_id}")
                return json.loads(data) if data else []
            except Exception as e:
                print(f"DEBUG: Redis get error: {e}")
                return []
        else:
            return self._store.get(user_id, [])

    def clear(self, user_id: str):
        if self.use_redis:
            try:
                self.client.delete(f"session:{user_id}")
            except Exception as e:
                print(f"DEBUG: Redis clear error: {e}")
        else:
            self._store[user_id] = []

memory = ShortTermMemory()