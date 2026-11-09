
from pydantic import ValidationError

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ChatSource
)


def main():
    # Valid request
    request = ChatRequest(
        question="  Làm thế nào để kết nối VPN?  "
    )

    print("===== VALID REQUEST =====")
    print(request.model_dump())

    # Valid response
    response = ChatResponse(
        question=request.question,
        answer="Mở ứng dụng VPN do IT cung cấp. [S1]",
        sources=[
            ChatSource(
                id="S1",
                source="vpn_access.md",
                chunk_index=6,
                score=0.7898
            )
        ],
        model="gemini-3.5-flash-lite"
    )

    print("\n===== VALID RESPONSE =====")
    print(response.model_dump_json(indent=2))

    # Invalid request
    print("\n===== INVALID REQUEST =====")

    try:
        ChatRequest(question="   ", top_k=0)
    except ValidationError as error:
        print("Validation correctly rejected the request.")
        print("Number of errors:", len(error.errors()))


if __name__ == "__main__":
    main()
