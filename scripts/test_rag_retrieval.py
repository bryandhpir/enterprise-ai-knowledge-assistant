
from app.services.chroma_search import search_chroma


def main():
    question = "Làm thế nào để kết nối VPN vào mạng nội bộ công ty?"

    results = search_chroma(
        query=question,
        top_k=3,
        collection_name="it_knowledge_base_v2"
    )

    print("Question:", question)
    print("Retrieved chunks:", len(results))

    for index, result in enumerate(results, start=1):
        print(f"\n--- Chunk {index} ---")
        print("Source:", result["source"])
        print("Chunk index:", result["chunk_index"])
        print("Similarity score:", result["score"])
        print("Content:")
        print(result["text"])


if __name__ == "__main__":
    main()
