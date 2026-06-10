import os
import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, index_path: str = "data/faiss_index"):
        self.index_path = index_path
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dimension = 384
        self.chunks_file = os.path.join(index_path, "rag_chunks.json")
        self.rag_index_file = os.path.join(index_path, "rag_index.faiss")
        self.chunks = []
        self.index = faiss.IndexFlatL2(self.dimension)
        self._load()

    def _load(self):
        os.makedirs(self.index_path, exist_ok=True)
        if os.path.exists(self.rag_index_file) and os.path.exists(self.chunks_file):
            self.index = faiss.read_index(self.rag_index_file)
            with open(self.chunks_file, "r") as f:
                self.chunks = json.load(f)
            print(f"DEBUG: Loaded RAG index with {len(self.chunks)} chunks")

    def _save(self):
        faiss.write_index(self.index, self.rag_index_file)
        with open(self.chunks_file, "w") as f:
            json.dump(self.chunks, f)

    def add_documents(self, documents: list):
        """Add a list of {text, source, city} dicts to the index."""
        texts = [d["text"] for d in documents]
        embeddings = self.model.encode(texts)
        self.index.add(np.array(embeddings, dtype=np.float32))
        self.chunks.extend(documents)
        self._save()
        print(f"DEBUG: Added {len(documents)} chunks to RAG index")

    def search(self, query: str, top_k: int = 3, city: str = None) -> list:
        """Search for relevant chunks."""
        if self.index.ntotal == 0:
            return []

        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(
            np.array(query_embedding, dtype=np.float32), top_k * 2
        )

        results = []
        for idx in indices[0]:
            if idx != -1 and idx < len(self.chunks):
                chunk = self.chunks[idx]
                if city is None or city.lower() in chunk.get("city", "").lower():
                    results.append(chunk)
                if len(results) >= top_k:
                    break

        return results

vector_store = VectorStore()