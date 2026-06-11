import os
import json
import pickle
import numpy as np
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class LongTermMemory:
    def __init__(self, index_path: str = "data/faiss_index"):
        self.index_path = index_path
        self.metadata_file = os.path.join(index_path, "metadata.json")
        self.vectorizer_file = os.path.join(index_path, "ltm_vectorizer.pkl")
        self.matrix_file = os.path.join(index_path, "ltm_matrix.pkl")
        self.metadata = []
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.matrix = None
        self._load()

    def _load(self):
        os.makedirs(self.index_path, exist_ok=True)
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, "r") as f:
                self.metadata = json.load(f)
            if os.path.exists(self.vectorizer_file) and len(self.metadata) > 0:
                with open(self.vectorizer_file, "rb") as f:
                    self.vectorizer = pickle.load(f)
                with open(self.matrix_file, "rb") as f:
                    self.matrix = pickle.load(f)

    def _save(self):
        with open(self.metadata_file, "w") as f:
            json.dump(self.metadata, f)
        if len(self.metadata) > 0:
            texts = [m["preference"] for m in self.metadata]
            self.matrix = self.vectorizer.fit_transform(texts)
            with open(self.vectorizer_file, "wb") as f:
                pickle.dump(self.vectorizer, f)
            with open(self.matrix_file, "wb") as f:
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