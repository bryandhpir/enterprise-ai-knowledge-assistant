"""Optional two-stage retrieval with lightweight lexical passage reranking.

Stage 1: fetch a wider semantic candidate set from the *existing* V2 collection.
Stage 2: score those passages using a BM25-style lexical signal combined
with normalized original-query cosine similarity, then select Top-K.

This is NOT a cross-encoder, and it does not introduce a second AI model.
It cannot rescue a relevant passage missing from the stage-1 candidate set.
Only ``score`` represents cosine similarity; ``rerank_score`` is a unitless
ranking signal. Retrieval experiments must use passage-level labels.
"""

from collections import Counter
import os
import math
import re
import unicodedata

from app.services.chroma_search import search_chroma

COLLECTION = "it_knowledge_base_v2"
DEFAULT_CANDIDATES = 80
DEFAULT_LEXICAL_WEIGHT = 0.65
MAX_CANDIDATES = 200

# Conservative stopword list; retain domain-bearing words such as VPN, IT,
# security, employee, account, and device. No third-party NLP dependency.
STOPWORDS = frozenset({
    "toi", "cua", "cho", "voi", "va", "hoac", "la", "co", "khong",
    "nhung", "nay", "do", "de", "khi", "thi", "the", "nao", "lam",
    "gi", "can", "duoc", "mot", "cach", "tren", "trong", "neu",
    "sau", "tu", "o", "tai", "boi", "cac", "bao", "nhieu",
    "nhu", "roi", "van", "da", "vi", "sao", "nen", "theo",
})


def _tokens(text: str) -> list[str]:
    """Whitespace/Unicode-aware Vietnamese lexical tokens; not full word segmentation."""
    folded = unicodedata.normalize("NFD", text.casefold().replace("đ", "d"))
    folded = "".join(c for c in folded if unicodedata.category(c) != "Mn")
    return [
        term for term in re.findall(r"[a-z0-9]+", folded)
        if len(term) > 1 and term not in STOPWORDS
    ]


def _passage_key(chunk: dict) -> tuple[str, int]:
    return (chunk["source"], int(chunk["chunk_index"]))


def rerank_passages(
    question: str,
    candidates: list[dict],
    top_k: int = 3,
    *,
    lexical_weight: float = 0.65,
) -> list[dict]:
    """Rerank semantic candidates using BM25 + original cosine similarity.

    Original candidate dictionaries remain unchanged. Empty-lexical queries
    keep semantic ranking. Passage IDs are (source, chunk_index), matching V2.
    """
    if not question.strip():
        raise ValueError("Question must not be empty")
    if top_k < 1:
        raise ValueError("top_k must be positive")
    if not 0 <= lexical_weight <= 1:
        raise ValueError("lexical_weight must be in [0, 1]")
    if not candidates:
        return []

    # Defensive deduplication, preserving semantic-search order.
    unique = []
    seen = set()
    for item in candidates:
        key = _passage_key(item)
        if key not in seen:
            seen.add(key)
            unique.append(item)

    query_terms = _tokens(question)
    if not query_terms:
        return [dict(item) for item in unique[:top_k]]

    documents = [_tokens(item["text"]) for item in unique]
    term_counts = [Counter(doc) for doc in documents]
    n_docs = len(unique)
    avg_length = sum(len(doc) for doc in documents) / n_docs or 1.0

    doc_frequency = Counter()
    for tf in term_counts:
        doc_frequency.update(tf.keys())

    lexical = []
    for doc, tf in zip(documents, term_counts):
        total = 0.0
        for term in set(query_terms):
            frequency = tf[term]
            if frequency == 0:
                continue
            idf = math.log(1 + (n_docs - doc_frequency[term] + 0.5) /
                           (doc_frequency[term] + 0.5))
            denom = frequency + 1.5 * (0.25 + 0.75 * len(doc) / avg_length)
            total += idf * frequency * 2.5 / denom
        lexical.append(total)

    dense = [float(item["score"]) for item in unique]

    def normalize(values: list[float]) -> list[float]:
        low, high = min(values), max(values)
        if high == low:
            return [1.0] * len(values) if high > 0 else [0.0] * len(values)
        return [(value - low) / (high - low) for value in values]

    lexical_norm = normalize(lexical)
    dense_norm = normalize(dense)
    # If none of the query terms appear, preserve the semantic results.
    effective_lexical_weight = lexical_weight if max(lexical) > 0 else 0.0

    scored = []
    for index, item in enumerate(unique):
        score = (effective_lexical_weight * lexical_norm[index] +
                 (1.0 - effective_lexical_weight) * dense_norm[index])
        scored.append({**item, "rerank_score": round(score, 6)})

    scored.sort(key=lambda item: (-item["rerank_score"], -item["score"],
                                  item["source"], item["chunk_index"]))
    return scored[:top_k]


def retrieve_reranked(question: str, top_k: int = 3) -> list[dict]:
    """Retrieve a larger candidate pool, then select Top-K lexical-reranked passages."""
    if not question.strip():
        raise ValueError("Question must not be empty")
    if top_k < 1:
        raise ValueError("top_k must be positive")

    # Independently configurable; defaults match the evaluated 80/0.65 setup.
    # A larger candidate pool may increase retrieval latency.
    raw_count = os.getenv("RAG_RERANK_CANDIDATES") or str(DEFAULT_CANDIDATES)
    raw_weight = os.getenv("RAG_RERANK_LEXICAL_WEIGHT") or str(DEFAULT_LEXICAL_WEIGHT)

    try:
        candidate_count = int(raw_count)
    except ValueError as exc:
        raise ValueError("RAG_RERANK_CANDIDATES must be an integer") from exc
    if not top_k <= candidate_count <= MAX_CANDIDATES:
        raise ValueError(
            f"RAG_RERANK_CANDIDATES must be between top_k ({top_k}) "
            f"and {MAX_CANDIDATES}"
        )

    try:
        lexical_weight = float(raw_weight)
    except ValueError as exc:
        raise ValueError("RAG_RERANK_LEXICAL_WEIGHT must be numeric") from exc
    if not 0 <= lexical_weight <= 1:
        raise ValueError("RAG_RERANK_LEXICAL_WEIGHT must be between 0 and 1")

    candidates = search_chroma(
        query=question,
        top_k=candidate_count,
        collection_name=COLLECTION,
    )
    return rerank_passages(
        question, candidates, top_k=top_k, lexical_weight=lexical_weight
    )
