
import numpy as np

from app.services.document_processor import (
    load_document_chunks
)
from app.services.embedding_service import embed_texts


def semantic_search(query: str, top_k: int = 3):

    if not query.strip():
        raise ValueError("Query must not be empty")

    if top_k <= 0:
        raise ValueError("top_k must be positive")

    chunks = load_document_chunks()

    if not chunks:
        return []

    # Extract document text
    texts = [chunk["text"] for chunk in chunks]

    # Create document embeddings
    document_vectors = embed_texts(texts)

    # Create query embedding
    query_vector = embed_texts([query])[0]

    # Calculate cosine similarity
    scores = np.dot(
        document_vectors,
        query_vector
    )

    # Sort by similarity, highest first
    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []

    for index in top_indices:
        chunk = chunks[int(index)]

        results.append({
            "source": chunk["source"],
            "chunk_index": chunk["chunk_index"],
            "text": chunk["text"],
            "score": round(float(scores[index]), 4)
        })

    return results
