import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

index_path = "data/faiss_index"
rag_files = ["rag_chunks.json", "rag_index.faiss"]
for f in rag_files:
    path = os.path.join(index_path, f)
    if os.path.exists(path):
        os.remove(path)
        print(f"Deleted old {f}")

from app.rag.indexer import build_index

if __name__ == "__main__":
    print("Building RAG index from travel websites...")
    build_index()
    print("\nRAG index built successfully!")