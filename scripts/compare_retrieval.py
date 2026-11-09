
import json
from pathlib import Path

from app.services.chroma_search import search_chroma


BASE_DIR = Path(__file__).resolve().parents[1]

DATASET_PATH = (
    BASE_DIR / "evals" / "holdout_questions.json"
)


def get_first_relevant_rank(results, expected):
    expected_sources = set(expected)

    for rank, result in enumerate(results, start=1):
        if result["source"] in expected_sources:
            return rank

    return None


def main():
    questions = json.loads(
        DATASET_PATH.read_text(encoding="utf-8")
    )

    for item in questions:
        query = item["query"]
        expected = item["relevant_sources"]

        v1_results = search_chroma(
            query=query,
            top_k=8,
            collection_name="it_knowledge_base"
        )

        v2_results = search_chroma(
            query=query,
            top_k=8,
            collection_name="it_knowledge_base_v2"
        )

        v1_rank = get_first_relevant_rank(
            v1_results, expected
        )

        v2_rank = get_first_relevant_rank(
            v2_results, expected
        )

        print("\n" + "=" * 60)
        print("QUESTION:", query)
        print("EXPECTED:", expected)
        print("V1 RANK:", v1_rank)
        print("V2 RANK:", v2_rank)

        if v1_rank is None or v2_rank is None:
            print("Comparison: BOTH OUTSIDE TOP 8")

        elif v1_rank is None:
            print("Comparison: V2 BETTER")

        elif v2_rank is None:
            print("Comparison: V1 BETTER")

        elif v2_rank < v1_rank:
            print("Comparison: V2 BETTER")

        elif v2_rank > v1_rank:
            print("Comparison: V1 BETTER")

        else:
            print("Comparison: SAME RANK")


        if v2_results:
            print("\nV2 TOP 1 SOURCE:")
            print(v2_results[0]["source"])

            print("\nV2 TOP 1 CONTENT:")
            print(v2_results[0]["text"][:500])


if __name__ == "__main__":
    main()
