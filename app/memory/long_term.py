import json
import pickle
import numpy as np
import redis
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.config import settings

class LongTermMemory:
    def __init__(self):
        self.use_redis = bool(settings.redis_url)
        if self.use_redis:
            try:
                self.client = redis.from_url(
                    settings.redis_url,
                    decode_responses=False
                )
                self.client.ping()
                print("DEBUG: Connected to Redis for long-term memory")
            except Exception as e:
                print(f"DEBUG: Redis connection failed for LTM: {e}")
                self.use_redis = False

        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english'
        )
        self.matrix = None
        self.metadata = []
        self._load()

    def _load(self):
        """Load metadata and vectorizer from Redis or disk."""
        if self.use_redis:
            try:
                meta_data = self.client.get("ltm:metadata")
                if meta_data:
                    self.metadata = json.loads(meta_data.decode("utf-8"))

                vec_data = self.client.get("ltm:vectorizer")
                mat_data = self.client.get("ltm:matrix")
                if vec_data and mat_data:
                    self.vectorizer = pickle.loads(vec_data)
                    self.matrix = pickle.loads(mat_data)
                    print(f"DEBUG: Loaded {len(self.metadata)} preferences from Redis")
            except Exception as e:
                print(f"DEBUG: LTM Redis load error: {e}")
        else:
            import os
            index_path = settings.faiss_index_path
            metadata_file = os.path.join(index_path, "metadata.json")
            vectorizer_file = os.path.join(index_path, "ltm_vectorizer.pkl")
            matrix_file = os.path.join(index_path, "ltm_matrix.pkl")

            if os.path.exists(metadata_file):
                with open(metadata_file, "r") as f:
                    self.metadata = json.load(f)
            if os.path.exists(vectorizer_file):
                with open(vectorizer_file, "rb") as f:
                    self.vectorizer = pickle.load(f)
            if os.path.exists(matrix_file):
                with open(matrix_file, "rb") as f:
                    self.matrix = pickle.load(f)

    def _save(self):
        """Save metadata and vectorizer to Redis or disk."""
        if self.use_redis:
            try:
                self.client.set(
                    "ltm:metadata",
                    json.dumps(self.metadata).encode("utf-8")
                )
                if len(self.metadata) > 0:
                    texts = [m["preference"] for m in self.metadata]
                    self.matrix = self.vectorizer.fit_transform(texts)
                    self.client.set("ltm:vectorizer", pickle.dumps(self.vectorizer))
                    self.client.set("ltm:matrix", pickle.dumps(self.matrix))
            except Exception as e:
                print(f"DEBUG: LTM Redis save error: {e}")
        else:
            import os
            index_path = settings.faiss_index_path
            os.makedirs(index_path, exist_ok=True)
            with open(os.path.join(index_path, "metadata.json"), "w") as f:
                json.dump(self.metadata, f)
            if len(self.metadata) > 0:
                texts = [m["preference"] for m in self.metadata]
                self.matrix = self.vectorizer.fit_transform(texts)
                with open(os.path.join(index_path, "ltm_vectorizer.pkl"), "wb") as f:
                    pickle.dump(self.vectorizer, f)
                with open(os.path.join(index_path, "ltm_matrix.pkl"), "wb") as f:
                    pickle.dump(self.matrix, f)

    def store_preference(self, user_id: str, preference: str):
        self.metadata.append({
            "user_id": user_id,
            "preference": preference,
            "timestamp": datetime.now().isoformat()
        })
        self._save()

    def get_preferences(self, user_id: str, query: str, top_k: int = 5) -> list:
        user_prefs = [m for m in self.metadata if m["user_id"] == user_id]
        if not user_prefs:
            return []
        return [p["preference"] for p in user_prefs[-top_k:]]

long_term_memory = LongTermMemory()