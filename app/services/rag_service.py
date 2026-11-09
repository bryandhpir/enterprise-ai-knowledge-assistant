
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from app.services.chroma_search import search_chroma
from app.services.rag_context import build_context
from app.services.rag_prompt import build_rag_prompt


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


def answer_question(question: str, top_k: int = 3) -> dict:
    # 1. Validate question
    question = question.strip()

    if not question:
        raise ValueError("Question must not be empty")

    if top_k < 1:
        raise ValueError("top_k must be positive")

    # 2. Retrieval from ChromaDB V2
    chunks = search_chroma(
        query=question,
        top_k=top_k,
        collection_name="it_knowledge_base_v2"
    )

    # 3. Remove empty chunks
    chunks = [
        chunk for chunk in chunks
        if chunk["text"].strip()
    ]

    if not chunks:
        return {
            "question": question,
            "answer": "Không có tài liệu khả dụng để trả lời.",
            "sources": [],
            "model": None
        }

    # 4. Build context
    context = build_context(chunks)

    # 5. Build RAG prompt
    prompt = build_rag_prompt(question, context)

    # 6. Gemini Generation
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv(
        "GEMINI_MODEL", "gemini-3.5-flash-lite"
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

    # 7. Format retrieved sources
    sources = []

    for index, chunk in enumerate(chunks, start=1):
        sources.append({
            "id": f"S{index}",
            "source": chunk["source"],
            "chunk_index": chunk["chunk_index"],
            "score": chunk["score"]
        })

    # 8. Return structured result
    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "model": model_name
    }
