
import json
from pathlib import Path

from app.services.chroma_search import search_chroma

BASE_DIR = Path(__file__).resolve().parents[1]

DATASET_PATH = (
    BASE_DIR / "evals" / "questions.json"
)


def main():
    questions = json.loads(
        DATASET_PATH.read_text(encoding="utf-8")
    )

    failed_questions = []

    for item in questions:

        results = search_chroma(
            item["query"],
            top_k=8
        )

        expected = set(item["relevant_sources"])

        first_rank = None

        for rank, result in enumerate(results, start=1):
            if result["source"] in expected:
                first_rank = rank
                break

        # Analyze cases where relevant content
        # is not found in the top 3
        if first_rank is None or first_rank > 3:

            failed_questions.append({
                "question": item["query"],
                "expected": list(expected),
                "first_rank": first_rank,
                "results": results[:5]
            })

    print("\nRETRIEVAL FAILURE ANALYSIS")
    print("=" * 50)

    print("Total failed questions:", len(failed_questions))

    for item in failed_questions:

        print("\nQuestion:", item["question"])
        print("Expected:", item["expected"])
        print("First relevant rank:", item["first_rank"])

        print("\nTop 5 retrieved chunks:")

        for rank, result in enumerate(
            item["results"], start=1
        ):
            print(
                f"{rank}. {result['source']} "
                f"| Chunk: {result['chunk_index']} "
                f"| Score: {result['score']:.4f}"
            )

        print("-" * 50)


if __name__ == "__main__":
    main()
