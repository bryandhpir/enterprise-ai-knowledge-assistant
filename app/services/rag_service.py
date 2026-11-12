"""Retrieve evidence and generate a source-grounded RAG response."""

import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from app.services.chroma_search import search_chroma
from app.services.rag_context import build_context
from app.services.rag_prompt import build_rag_prompt
from app.services.rag_guardrails import (
    filter_chunks,
    citations_are_valid,
    NO_ANSWER,
    UNVERIFIED_ANSWER,
)

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


def answer_question(question: str, top_k: int = 3) -> dict:
    question = question.strip()
    if not question:
        raise ValueError("Question must not be empty")
    if top_k < 1:
        raise ValueError("top_k must be positive")

    mode = os.getenv("RAG_RETRIEVAL_MODE", "baseline").strip().lower()
    if mode == "baseline":
        chunks = search_chroma(
            query=question,
            top_k=top_k,
            collection_name="it_knowledge_base_v2",
        )
    elif mode == "multi_query":
        # Import lazily to keep the baseline path unchanged.
        from app.services.multi_query_retrieval import retrieve_multi_query
        chunks = retrieve_multi_query(question=question, top_k=top_k)
    elif mode == "rerank":
        from app.services.lexical_reranker import retrieve_reranked
        chunks = retrieve_reranked(question=question, top_k=top_k)
    else:
        raise ValueError(
            "RAG_RETRIEVAL_MODE must be 'baseline', 'multi_query', or 'rerank'"
        )

    # For both modes, score means cosine similarity to the ORIGINAL question.
    raw_threshold = os.getenv("RAG_MIN_SIMILARITY", "").strip()
    min_score = float(raw_threshold) if raw_threshold else None
    if min_score is not None and not 0 <= min_score <= 1:
        raise ValueError("RAG_MIN_SIMILARITY must be between 0 and 1")
    chunks = filter_chunks(chunks, min_score=min_score)

    if not chunks:
        return {
            "question": question,
            "answer": NO_ANSWER,
            "sources": [],
            "model": None,
        }

    # Optional evidence-only continuation; no retrieval ranks or scores change.
    # Limited to rerank mode and disabled unless explicitly enabled.
    if mode == "rerank" and os.getenv(
        "RAG_CONTEXT_NEIGHBORS", "false"
    ).strip().lower() in ("1", "true", "yes", "on"):
        from app.services.neighbor_context import append_next_chunk_context
        chunks = append_next_chunk_context(chunks)

    context = build_context(chunks)
    prompt = build_rag_prompt(question=question, context=context)
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing")

    client = genai.Client(api_key=api_key)
    response = client.interactions.create(model=model_name, input=prompt)
    answer = (response.output_text or "").strip()
    if not answer:
        raise RuntimeError("Gemini returned no text")

    sources = []
    for index, chunk in enumerate(chunks, start=1):
        entry = {
            "id": f"S{index}",
            "source": chunk["source"],
            "chunk_index": chunk["chunk_index"],
            "score": chunk["score"],
        }
        if chunk.get("context_chunk_indices"):
            # Explicitly disclose the evidence span behind this citation ID.
            entry["context_chunk_indices"] = chunk["context_chunk_indices"]
        sources.append(entry)

    if NO_ANSWER in answer:
        answer = NO_ANSWER
    elif not citations_are_valid(answer, sources):
        answer = UNVERIFIED_ANSWER

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "model": model_name,
    }
