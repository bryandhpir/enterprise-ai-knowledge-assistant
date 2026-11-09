
def retrieval_metrics(
    results: list[dict],
    relevant_sources: list[str],
    k: int
) -> dict:

    if k <= 0:
        raise ValueError("k must be positive")

    if not relevant_sources:
        raise ValueError("relevant_sources must not be empty")

    # Ground truth documents
    expected = set(relevant_sources)

    # Top-K retrieved chunks
    top_results = results[:k]

    retrieved_sources = [
        result["source"]
        for result in top_results
    ]

    # Recall@K (document level)
    found_sources = set(retrieved_sources) & expected
    recall = len(found_sources) / len(expected)

    # Rank of first relevant chunk
    first_rank = None

    for rank, source in enumerate(retrieved_sources, start=1):
        if source in expected:
            first_rank = rank
            break

    # Hit@K
    hit = 1.0 if first_rank is not None else 0.0

    # Reciprocal Rank@K
    reciprocal_rank = (
        1.0 / first_rank
        if first_rank is not None
        else 0.0
    )

    return {
        "hit": hit,
        "recall": recall,
        "rr": reciprocal_rank
    }
