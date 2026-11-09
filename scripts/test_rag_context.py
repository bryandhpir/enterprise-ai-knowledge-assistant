
from app.services.chroma_search import search_chroma
from app.services.rag_context import build_context


def main():
    question = "Làm thế nào để kết nối VPN vào mạng nội bộ công ty?"

    chunks = search_chroma(
        query=question,
        top_k=3,
        collection_name="it_knowledge_base_v2"
    )

    context = build_context(chunks)

    print("QUESTION:")
    print(question)

    print("\nRETRIEVED CHUNKS:", len(chunks))

    print("\nFORMATTED CONTEXT:")
    print(context if context else "(No context found)")


if __name__ == "__main__":
    main()
