
import argparse
import json

from pathlib import Path
from statistics import mean

from app.services.chroma_search import search_chroma
from evals.metrics import retrieval_metrics


BASE_DIR = Path(__file__).resolve().parents[1]

K_VALUES = [1, 3, 5, 8]


def main(
    collection_name: str = "it_knowledge_base",
    dataset_path: str = "evals/questions.json"
):
    # 1. Resolve dataset path
    path = Path(dataset_path)

    if not path.is_absolute():
        path = BASE_DIR / path

    # 2. Load evaluation questions
    questions = json.loads(
        path.read_text(encoding="utf-8")
    )

    if not questions:
        raise ValueError("Evaluation dataset is empty")

    print("Collection:", collection_name)
    print("Dataset:", path.name)
    print("Total questions:", len(questions))

    # 3. Initialize metric storage
    summary = {
        k: {
            "hit": [],
            "recall": [],
            "rr": []
        }
        for k in K_VALUES
    }

    # 4. Evaluate each question
    for item in questions:
        query = item["query"]
        expected = item["relevant_sources"]

        results = search_chroma(
            query=query,
            top_k=max(K_VALUES),
            collection_name=collection_name
        )

        # Calculate metrics for each K
        for k in K_VALUES:
            metrics = retrieval_metrics(
                results,
                expected,
                k
            )

            for metric, value in metrics.items():
                summary[k][metric].append(value)

        # Find the first relevant result
        first_rank = next(
            (
                rank
                for rank, result in enumerate(
                    results, start=1
                )
                if result["source"] in expected
            ),
            None
        )

        print(f"\nQuestion {item['id']}: {query}")
        print("Expected:", expected)
        print("First relevant rank:", first_rank)

        for rank, result in enumerate(
            results[:3], start=1
        ):
            print(
                f"  {rank}. {result['source']} "
                f"| Score: {result['score']:.4f}"
            )

    # 5. Print evaluation summary
    print("\n" + "=" * 45)
    print("RETRIEVAL EVALUATION SUMMARY")
    print("=" * 45)

    print("Collection:", collection_name)
    print("Dataset:", path.name)
    print("Total questions:", len(questions))

    for k in K_VALUES:
        hit = mean(summary[k]["hit"])
        recall = mean(summary[k]["recall"])
        mrr = mean(summary[k]["rr"])

        print(f"\nK = {k}")
        print(f"Hit@{k}:    {hit:.4f}")
        print(f"Recall@{k}: {recall:.4f}")
        print(f"MRR@{k}:    {mrr:.4f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Evaluate RAG retrieval performance"
    )

    parser.add_argument(
        "--collection",
        default="it_knowledge_base",
        help="ChromaDB collection name"
    )

    parser.add_argument(
        "--dataset",
        default="evals/questions.json",
        help="Path to evaluation dataset"
    )

    args = parser.parse_args()

    main(
        collection_name=args.collection,
        dataset_path=args.dataset
    )
