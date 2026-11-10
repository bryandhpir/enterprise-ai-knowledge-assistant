
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

    # 1. Retrieval
    chunks = search_chroma(
        query=question,
        top_k=top_k,
        collection_name="it_knowledge_base_v2"
    )

    # 2. Optional similarity threshold
    raw_threshold = os.getenv(
        "RAG_MIN_SIMILARITY", ""
    ).strip()

    min_score = (
        float(raw_threshold)
        if raw_threshold else None
    )

    if min_score is not None and not 0 <= min_score <= 1:
        raise ValueError(
            "RAG_MIN_SIMILARITY must be between 0 and 1"
        )

    chunks = filter_chunks(
        chunks,
        min_score=min_score
    )

    # 3. No-answer fallback
    if not chunks:
        return {
            "question": question,
            "answer": NO_ANSWER,
            "sources": [],
            "model": None
        }

    # 4. Context + Prompt
    context = build_context(chunks)

    prompt = build_rag_prompt(
        question=question,
        context=context
    )

    # 5. Gemini Generation
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.5-flash-lite"
    )

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing")

    client = genai.Client(api_key=api_key)

    response = client.interactions.create(
        model=model_name,
        input=prompt
    )

    answer = (response.output_text or "").strip()

    if not answer:
        raise RuntimeError("Gemini returned no text")

    # 6. Source metadata
    sources = [
        {
            "id": f"S{index}",
            "source": chunk["source"],
            "chunk_index": chunk["chunk_index"],
            "score": chunk["score"]
        }
        for index, chunk in enumerate(chunks, start=1)
    ]

    # 7. Citation validation
    if NO_ANSWER in answer:
        answer = NO_ANSWER

    elif not citations_are_valid(answer, sources):
        answer = UNVERIFIED_ANSWER

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "model": model_name
    }
