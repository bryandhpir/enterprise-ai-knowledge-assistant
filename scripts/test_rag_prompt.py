
from app.services.chroma_search import search_chroma
from app.services.rag_context import build_context
from app.services.rag_prompt import build_rag_prompt


def main():
    question = "Làm thế nào để kết nối VPN vào mạng nội bộ công ty?"

    # Step 1: Retrieval
    chunks = search_chroma(
        query=question,
        top_k=3,
        collection_name="it_knowledge_base_v2"
    )

    # Step 2: Context Construction
    context = build_context(chunks)

    # Step 3: Prompt Construction
    prompt = build_rag_prompt(
        question=question,
        context=context
    )

    print("===== RAG PROMPT =====")
    print(prompt)
    print("======================")
    print("Prompt length:", len(prompt))


if __name__ == "__main__":
    main()
