
from app.services.rag_service import answer_question


def main():
    question = "Làm thế nào để kết nối VPN vào mạng nội bộ công ty?"

    result = answer_question(
        question=question,
        top_k=3
    )

    print("===== QUESTION =====")
    print(result["question"])

    print("\n===== ANSWER =====")
    print(result["answer"])

    print("\n===== SOURCES =====")
    for source in result["sources"]:
        print(source)

    print("\n===== MODEL =====")
    print(result["model"])


if __name__ == "__main__":
    main()
