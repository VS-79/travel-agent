import os
import json
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class VectorStore:
    def __init__(self, index_path: str = "data/faiss_index"):
        self.index_path = index_path
        self.chunks_file = os.path.join(index_path, "rag_chunks.json")
        self.vectorizer_file = os.path.join(index_path, "vectorizer.pkl")
        self.matrix_file = os.path.join(index_path, "tfidf_matrix.pkl")
        self.chunks = []
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        self.matrix = None
        self._load()

    def _load(self):
        os.makedirs(self.index_path, exist_ok=True)
        if os.path.exists(self.chunks_file) and os.path.exists(self.vectorizer_file):
            with open(self.chunks_file, "r") as f:
                self.chunks = json.load(f)
            with open(self.vectorizer_file, "rb") as f:
                self.vectorizer = pickle.load(f)
            with open(self.matrix_file, "rb") as f:
                self.matrix = pickle.load(f)
            print(f"DEBUG: Loaded TF-IDF index with {len(self.chunks)} chunks")

    def _save(self):
        with open(self.chunks_file, "w") as f:
            json.dump(self.chunks, f)
        with open(self.vectorizer_file, "wb") as f:
            pickle.dump(self.vectorizer, f)
        with open(self.matrix_file, "wb") as f:
            pickle.dump(self.matrix, f)

    def add_documents(self, documents: list):
        self.chunks.extend(documents)
        texts = [d["text"] for d in self.chunks]
        self.matrix = self.vectorizer.fit_transform(texts)
        self._save()
        print(f"DEBUG: Added {len(documents)} chunks to TF-IDF index")

    def search(self, query: str, top_k: int = 3, city: str = None) -> list:
        if self.matrix is None or len(self.chunks) == 0:
            return []

        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.matrix).flatten()
        top_indices = np.argsort(scores)[::-1]

        results = []
        for idx in top_indices:
            if len(results) >= top_k:
                break
            chunk = self.chunks[idx]
            if city is None or city.lower() in chunk.get("city", "").lower():
                if scores[idx] > 0:
                    results.append(chunk)

        return results

vector_store = VectorStore()