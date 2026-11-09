
import json
from pathlib import Path

from app.services.chroma_search import search_chroma

BASE_DIR = Path(__file__).resolve().parents[1]

DATASET_PATH = BASE_DIR / "evals" / "questions.json"


def main():
    questions = json.loads(
        DATASET_PATH.read_text(encoding="utf-8")
    )

    for item in questions:
        results = search_chroma(
            query=item["query"],
            top_k=1,
            collection_name="it_knowledge_base_v2"
        )

        print("\n" + "=" * 60)
        print("QUESTION:", item["query"])
        print("EXPECTED:", item["relevant_sources"])

        if not results:
            print("NO RESULTS")
            continue

        result = results[0]

        print("SOURCE:", result["source"])
        print("SCORE:", result["score"])
        print("CONTENT:")
        print(result["text"])
        print("=" * 60)


if __name__ == "__main__":
    main()
