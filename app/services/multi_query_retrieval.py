"""Optional multi-query retrieval with weighted RRF and safe fallback.

The original question is always preserved. LLM-generated variants are treated as
untrusted search suggestions, never as instructions or a replacement for the user
question. RRF ranks chunks; ``score`` remains original-query cosine similarity.
"""

import json
import logging
import os
import re
import unicodedata

from app.services.chroma_search import search_chroma
from app.services.embedding_service import embed_texts

LOGGER = logging.getLogger(__name__)
COLLECTION = "it_knowledge_base_v2"
RRF_K = 60


def _fold(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text.casefold())
    without_accents = "".join(
        char for char in decomposed if unicodedata.category(char) != "Mn"
    ).replace("đ", "d")
    return " ".join(without_accents.split())


def is_sensitive_disclosure_request(question: str) -> bool:
    """Conservative, incomplete check for third-party credential disclosure.

    This protects known test cases; it is NOT an access-control or security
    classification system and must not be marketed as one.
    """
    text = _fold(question)
    credentials = (
        "mat khau", "password", "ma otp", "otp", "api key",
        "access token", "private key", "ma xac thuc",
    )
    third_party = (
        "cua giam doc", "cua sep", "cua dong nghiep", "cua nguoi khac",
        "cua quan ly", "cua nhan vien khac", "of my manager",
        "someone else's", "someone elses",
    )
    return any(word in text for word in credentials) and any(
        phrase in text for phrase in third_party
    )


def _valid_variant(original: str, variant: str) -> bool:
    """Reject obvious topic/role additions; semantic equivalence is not proven."""
    candidate = variant.strip()
    if not candidate or candidate == original or len(candidate) > 350:
        return False
    old, new = _fold(original), _fold(candidate)
    if old == new:
        return False

    # These qualifiers can change the purpose of a business IT question.
    for qualifier in ("luat", "phap luat", "viet nam", "giam doc"):
        if qualifier in new and qualifier not in old:
            return False
    for role in ("giam doc", "dong nghiep", "nguoi khac"):
        if role in old and role not in new:
            return False
    return True


def generate_variants(question: str) -> list[str]:
    """Return up to two validated suggestions; may raise on model/API errors."""
    from google import genai

    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError("GEMINI_API_KEY is required for query expansion")

    prompt = (
        "Rewrite this Vietnamese enterprise IT-support search query in TWO "
        "different ways with exactly the same intent. Do not answer it. "
        "Do not change the requester, target person, permissions, or task. "
        "Do not reinterpret credential disclosure as password recovery. "
        "Do not add countries, laws, legal requirements, or other constraints "
        "not explicitly present in the original. Use technical synonyms only "
        "when they preserve the meaning. Return ONLY valid JSON: "
        '{"queries": ["...", "..."]}. Original: '
        + json.dumps(question, ensure_ascii=False)
    )
    client = genai.Client(api_key=key)
    response = client.interactions.create(
        model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"),
        input=prompt,
    )
    raw = (response.output_text or "").strip()
    if raw.startswith("```"):
        raw = "\n".join(raw.splitlines()[1:-1]).strip()
    values = json.loads(raw).get("queries", [])
    if not isinstance(values, list):
        raise ValueError("Query expansion did not return a JSON list")

    variants = []
    for value in values:
        if isinstance(value, str) and _valid_variant(question, value):
            value = value.strip()
            if value not in variants:
                variants.append(value)
        if len(variants) == 2:
            break
    return variants


def _identity(chunk: dict) -> tuple[str, int]:
    return chunk["source"], chunk["chunk_index"]


def weighted_rrf(result_lists: list[list[dict]], weights: list[float]) -> list[dict]:
    """Merge passages by source and chunk index, not by cosine similarity."""
    if len(result_lists) != len(weights):
        raise ValueError("Each result list must have a weight")

    merged: dict[tuple[str, int], dict] = {}
    for results, weight in zip(result_lists, weights):
        for rank, chunk in enumerate(results, start=1):
            key = _identity(chunk)
            if key not in merged:
                merged[key] = {**chunk, "rrf_score": 0.0}
            merged[key]["rrf_score"] += weight / (RRF_K + rank)

    return sorted(
        merged.values(),
        key=lambda item: (-item["rrf_score"], item["source"], item["chunk_index"]),
    )


def _attach_original_query_scores(
    question: str, selected: list[dict], baseline: list[dict]
) -> list[dict]:
    """Populate real original-query similarities, never RRF, in `score`.

    Re-embeds only variant-only candidates; baseline scores already came from
    a cosine-distance Chroma collection. Text embedding is a simple, portable
    alternative to depending on internal Chroma record ID layouts.
    """
    original_scores = {_identity(item): item["score"] for item in baseline}
    unseen = [item for item in selected if _identity(item) not in original_scores]
    if unseen:
        vectors = embed_texts([question, *[item["text"] for item in unseen]])
        question_vec = vectors[0]
        for item, doc_vec in zip(unseen, vectors[1:]):
            original_scores[_identity(item)] = round(
                float(sum(float(a) * float(b) for a, b in zip(question_vec, doc_vec))),
                4,
            )
    return [{**item, "score": original_scores[_identity(item)]} for item in selected]


def retrieve_multi_query(question: str, top_k: int = 3) -> list[dict]:
    """Retrieve top-K with weighted RRF; degrade to baseline on expansion failure."""
    if not question.strip():
        raise ValueError("Question must not be empty")
    if top_k < 1:
        raise ValueError("top_k must be positive")

    # Do not rewrite disclosure requests into benign helpdesk questions.
    if is_sensitive_disclosure_request(question):
        return []

    candidates = max(8, top_k)
    baseline = search_chroma(
        query=question, top_k=candidates, collection_name=COLLECTION
    )

    try:
        variants = generate_variants(question)
    except Exception as exc:
        LOGGER.warning("Query expansion failed (%s); using baseline", type(exc).__name__)
        return baseline[:top_k]

    if not variants:
        return baseline[:top_k]

    result_lists = [baseline]
    try:
        for variant in variants:
            result_lists.append(search_chroma(
                query=variant, top_k=candidates, collection_name=COLLECTION
            ))
        fused = weighted_rrf(result_lists, [2.0] + [1.0] * len(variants))
        return _attach_original_query_scores(question, fused[:top_k], baseline)
    except Exception as exc:
        LOGGER.warning("Multi-query retrieval failed (%s); using baseline", type(exc).__name__)
        return baseline[:top_k]
