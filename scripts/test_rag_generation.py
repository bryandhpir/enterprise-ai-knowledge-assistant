
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from app.services.chroma_search import search_chroma
from app.services.rag_context import build_context
from app.services.rag_prompt import build_rag_prompt


BASE_DIR = Path(__file__).resolve().parents[1]

load_dotenv(BASE_DIR / ".env")


def main():
    # Step 1: User Question
    question = "Làm thế nào để kết nối VPN vào mạng nội bộ công ty?"

    # Step 2: Retrieval
    chunks = search_chroma(
        query=question,
        top_k=3,
        collection_name="it_knowledge_base_v2"
    )

    if not chunks:
        print("No relevant documents retrieved.")
        return

    # Step 3: Context Construction
    context = build_context(chunks)

    if not context:
        print("No usable context found.")
        return

    # Step 4: Prompt Construction
    prompt = build_rag_prompt(
        question=question,
        context=context
    )

    # Step 5: Gemini API
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

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

    # Step 6: Display results
    print("\n===== USER QUESTION =====")
    print(question)

    print("\n===== RAG ANSWER =====")
    print(answer)

    print("\n===== RETRIEVED SOURCES =====")

    for index, chunk in enumerate(chunks, start=1):
        print(
            f"[S{index}] {chunk['source']} "
            f"(chunk {chunk['chunk_index']}, "
            f"score={chunk['score']})"
        )

    print("\n===== PIPELINE INFO =====")
    print("Model:", model_name)
    print("Retrieved chunks:", len(chunks))
    print("Prompt length:", len(prompt), "characters")


if __name__ == "__main__":
    main()
