import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from datetime import datetime

class LongTermMemory:
    def __init__(self, index_path: str = "data/faiss_index"):
        self.index_path = index_path
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dimension = 384
        self.metadata_file = os.path.join(index_path, "metadata.json")
        self.index_file = os.path.join(index_path, "index.faiss")
        self.metadata = []
        self.index = faiss.IndexFlatL2(self.dimension)
        self._load()

    def _load(self):
        os.makedirs(self.index_path, exist_ok=True)
        if os.path.exists(self.index_file) and os.path.exists(self.metadata_file):
            self.index = faiss.read_index(self.index_file)
            with open(self.metadata_file, "r") as f:
                self.metadata = json.load(f)

    def _save(self):
        faiss.write_index(self.index, self.index_file)
        with open(self.metadata_file, "w") as f:
            json.dump(self.metadata, f)

    def store_preference(self, user_id: str, preference: str):
        embedding = self.model.encode([preference])
        self.index.add(np.array(embedding, dtype=np.float32))
        self.metadata.append({
            "user_id": user_id,
            "preference": preference,
            "timestamp": datetime.now().isoformat()
        })
        self._save()

    def get_preferences(self, user_id: str, query: str, top_k: int = 5) -> list:
        if self.index.ntotal == 0:
            return []

        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(
            np.array(query_embedding, dtype=np.float32), top_k
        )

        results = []
        for idx in indices[0]:
            if idx != -1 and idx < len(self.metadata):
                entry = self.metadata[idx]
                if entry["user_id"] == user_id:
                    results.append(entry["preference"])

        return results

long_term_memory = LongTermMemory()