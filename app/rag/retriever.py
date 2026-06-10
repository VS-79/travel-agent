from app.rag.vector_store import vector_store

def retrieve(query: str, city: str = None, top_k: int = 3) -> str:
    """Retrieve relevant travel knowledge for a query."""
    results = vector_store.search(query, top_k=top_k, city=city)

    if not results:
        return ""

    context = "## Relevant Travel Knowledge:\n\n"
    for i, chunk in enumerate(results, 1):
        context += f"**Source {i}** ({chunk.get('source', 'unknown')}):\n"
        context += f"{chunk['text']}\n\n"

    return context

def multi_hop_retrieve(query: str, city: str = None) -> str:
    """
    Multi-hop RAG: first retrieval finds initial context,
    second retrieval refines based on that context.
    """
    first_results = retrieve(query, city=city, top_k=2)

    if not first_results:
        return ""

    first_texts = " ".join([
        r["text"] for r in vector_store.search(query, city=city, top_k=2)
    ])
    refined_query = f"{query} {first_texts[:200]}"
    second_results = retrieve(refined_query, city=city, top_k=2)

    combined = first_results
    if second_results and second_results != first_results:
        combined += "\n## Additional Context:\n" + second_results

    return combined