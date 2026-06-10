from collections import defaultdict
from typing import List

class ShortTermMemory:
    def __init__(self):
        self._store: dict[str, List] = defaultdict(list)

    def add(self, user_id: str, role: str, content: str):
        self._store[user_id].append({"role": role, "content": content})

    def get(self, user_id: str) -> List:
        return self._store[user_id]

    def clear(self, user_id: str):
        self._store[user_id] = []

memory = ShortTermMemory()