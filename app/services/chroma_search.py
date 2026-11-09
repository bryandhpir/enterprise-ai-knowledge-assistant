
from app.services.embedding_service import embed_texts
from app.services.vector_store import get_collection


def search_chroma(query: str, top_k: int = 3):

    if not query.strip():
        raise ValueError("Query must not be empty")

    if top_k <= 0:
        raise ValueError("top_k must be positive")

    collection = get_collection()

    if collection.count() == 0:
        return []

    # Only embed the user's question
    query_vector = embed_texts([query])[0]

    # Search stored document vectors
    results = collection.query(
        query_embeddings=[query_vector.tolist()],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"]
    )

    formatted_results = []

    for document, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        formatted_results.append({
            "source": metadata["source"],
            "chunk_index": metadata["chunk_index"],
            "text": document,
            "score": round(1 - distance, 4)
        })

    return formatted_results
