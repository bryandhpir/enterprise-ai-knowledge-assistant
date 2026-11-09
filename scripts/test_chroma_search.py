
from app.services.chroma_search import search_chroma

questions = [
    "Tôi muốn truy cập hệ thống công ty khi làm việc tại nhà",
    "Làm thế nào để kết nối VPN vào mạng nội bộ công ty?",
    "Nhân viên làm việc từ xa cần kết nối như thế nào?"
]

for question in questions:
    print(f"\nQUESTION: {question}")
    print("-" * 50)

    results = search_chroma(question, top_k=8)

    for rank, result in enumerate(results, start=1):
        print(
            f"{rank}. {result['source']} "
            f"| Chunk: {result['chunk_index']} "
            f"| Score: {result['score']:.4f}"
        )
