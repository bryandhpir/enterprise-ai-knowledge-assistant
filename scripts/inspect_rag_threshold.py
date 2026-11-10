
import json
from pathlib import Path

from app.services.chroma_search import search_chroma


BASE_DIR = Path(__file__).resolve().parents[1]

development = json.loads(
    (BASE_DIR / "evals/questions.json").read_text(
        encoding="utf-8"
    )
)

out_of_scope = [
    "Làm thế nào để nấu phở bò?",
    "Giá vàng hôm nay bao nhiêu?",
    "Hãy viết bài thơ về mèo.",
    "Cách đặt phòng khách sạn?"
]


def inspect(question, expected_sources=None):
    results = search_chroma(
        query=question,
        top_k=3,
        collection_name="it_knowledge_base_v2"
    )

    best_score = max(
        (item["score"] for item in results),
        default=None
    )

    relevant_score = None

    if expected_sources:
        relevant_score = max(
            (
                item["score"]
                for item in results
                if item["source"] in expected_sources
            ),
            default=None
        )

    print(
        f"Top score: {best_score} | "
        f"Relevant score: {relevant_score} | "
        f"{question}"
    )


print("===== IN-SCOPE =====")

for item in development:
    inspect(
        item["query"],
        item["relevant_sources"]
    )

print("\n===== OUT-OF-SCOPE =====")

for question in out_of_scope:
    inspect(question)
