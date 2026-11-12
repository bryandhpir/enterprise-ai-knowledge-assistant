"""Diagnose passage recall and lexical reranking without modifying the RAG app.

Uses the curated passage labels already available in evals/passage_eval_questions.json.
Does not call Gemini or mutate ChromaDB. Run inside the API container.
"""

import argparse
import json
from pathlib import Path
from statistics import mean

from app.services.chroma_search import search_chroma
from app.services.lexical_reranker import rerank_passages

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "evals" / "passage_eval_questions.json"
COLLECTION = "it_knowledge_base_v2"
WEIGHTS = (0.25, 0.40, 0.50, 0.65, 0.80)


def relevant_passages(case):
    return {
        (entry["source"], int(entry["chunk_index"]))
        for entry in case["relevant_passages"]
    }


def first_relevant_rank(results, expected):
    return next(
        (
            rank for rank, entry in enumerate(results, start=1)
            if (entry["source"], int(entry["chunk_index"])) in expected
        ),
        None,
    )


def describe_top(results, k=3):
    return ", ".join(
        f"{entry['source']}#{entry['chunk_index']}"
        for entry in results[:k]
    ) or "(empty)"


def main(candidate_count=48):
    if candidate_count < 3:
        raise ValueError("--candidates must be at least 3")
    cases = json.loads(DATASET.read_text(encoding="utf-8-sig"))
    reports = {weight: [] for weight in WEIGHTS}
    dense_reports = []

    print(f"Collection: {COLLECTION}")
    print(f"Dense candidates per question: {candidate_count}")
    print("Evaluation: curated passage labels (not an independent holdout)")

    for case in cases:
        expected = relevant_passages(case)
        candidates = search_chroma(
            query=case["query"],
            top_k=candidate_count,
            collection_name=COLLECTION,
        )
        dense_rank = first_relevant_rank(candidates, expected)
        dense_reports.append(dense_rank)
        print(f"\n{case['id']} | dense first relevant rank: {dense_rank}")
        print(f"  Dense top 3: {describe_top(candidates)}")

        for weight in WEIGHTS:
            reranked = rerank_passages(
                case["query"],
                candidates,
                top_k=len(candidates),
                lexical_weight=weight,
            )
            rank = first_relevant_rank(reranked, expected)
            reports[weight].append(rank)
            print(
                f"  lexical_weight={weight:.2f} | relevant rank={rank} "
                f"| top 3: {describe_top(reranked)}"
            )

    print("\n===== PASSAGE HIT@3 / MRR@3 (DEV DATA ONLY) =====")

    def display(label, ranks):
        hit = mean(rank is not None and rank <= 3 for rank in ranks)
        mrr = mean(1.0 / rank if rank is not None and rank <= 3 else 0.0 for rank in ranks)
        print(f"{label:>20}: Hit@3={hit:.4f} | MRR@3={mrr:.4f}")

    display("Dense baseline", dense_reports)
    for weight, ranks in reports.items():
        display(f"Lexical weight {weight:.2f}", ranks)

    # Earlier known failure H12 is source-level, so inspect it separately.
    rag_cases = json.loads(
        (ROOT / "evals" / "rag_eval_questions.json").read_text(encoding="utf-8-sig")
    )
    h12 = next((case for case in rag_cases if case["id"] == "H12"), None)
    if h12 is not None:
        pool = search_chroma(
            query=h12["query"],
            top_k=candidate_count,
            collection_name=COLLECTION,
        )

        def source_rank(results):
            return next(
                (rank for rank, item in enumerate(results, start=1)
                 if item["source"] in h12["relevant_sources"]),
                None,
            )

        print("\n===== KNOWN H12 SOURCE-LEVEL FAILURE (NOT PASSAGE METRIC) =====")
        print(f"Dense first VPN rank: {source_rank(pool)}")
        for weight in WEIGHTS:
            ranked = rerank_passages(
                h12["query"], pool,
                top_k=len(pool), lexical_weight=weight,
            )
            print(
                f"lexical_weight={weight:.2f} | VPN rank={source_rank(ranked)}"
                f" | top 3: {describe_top(ranked)}"
            )

    print("\nIMPORTANT: Tuning on this curated dataset can overfit.")
    print("Validate any selected configuration on new questions before integration.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=int, choices=(48, 80), default=48)
    args = parser.parse_args()
    main(candidate_count=args.candidates)
