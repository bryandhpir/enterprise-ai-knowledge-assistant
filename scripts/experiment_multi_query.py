"""Compare baseline semantic retrieval with LLM-based multi-query retrieval.

Run from the repository root with:
    python -m scripts.experiment_multi_query

The experiment does not alter ChromaDB or the running RAG service.
"""

import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from app.services.chroma_search import search_chroma


ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "evals" / "rag_eval_questions.json"
COLLECTION = "it_knowledge_base_v2"
load_dotenv(ROOT / ".env")


def generate_variants(question: str, client, model_name: str) -> list[str]:
    """Request two meaning-preserving rewrites; never assume they are correct."""
    prompt = (
        "You help search Vietnamese enterprise IT documentation. "
        "Rewrite the user's question into TWO alternative Vietnamese search "
        "queries that preserve its original intent. Use different wording "
        "and common IT terminology only when relevant. Do not invent "
        "facts, answer the question, or add unrelated topics. "
        'Return ONLY JSON with this structure: {"queries": ["...", "..."]}.\n'
        "Original question: "
        + json.dumps(question, ensure_ascii=False)
    )
    response = client.interactions.create(model=model_name, input=prompt)
    raw = (response.output_text or "").strip()
    if raw.startswith("```"):
        lines = raw.splitlines()
        raw = "\n".join(lines[1:-1]).strip()
    data = json.loads(raw)
    values = data.get("queries", [])
    if not isinstance(values, list):
        raise ValueError("Expected a JSON list of queries")

    variants = []
    for value in values:
        if not isinstance(value, str):
            continue
        value = value.strip()
        if value and value != question and value not in variants:
            variants.append(value)
        if len(variants) == 2:
            break
    return variants


def reciprocal_rank_fusion(queries: list[str], candidates: int = 8) -> list[dict]:
    """Fuse results by source/chunk identity, not by similarity score."""
    merged = {}
    for query_index, query in enumerate(queries):
        weight = 2.0 if query_index == 0 else 1.0
        results = search_chroma(query=query, top_k=candidates, collection_name=COLLECTION)
        for rank, result in enumerate(results, start=1):
            key = (result["source"], result["chunk_index"])
            if key not in merged:
                merged[key] = {
                    "source": result["source"],
                    "chunk_index": result["chunk_index"],
                    "rrf_score": 0.0,
                }
            merged[key]["rrf_score"] += weight / (60 + rank)
    return sorted(
        merged.values(),
        key=lambda result: (-result["rrf_score"], result["source"], result["chunk_index"]),
    )


def first_relevant_rank(results: list[dict], expected: list[str]) -> int | None:
    expected_set = set(expected)
    return next(
        (index for index, result in enumerate(results, 1)
         if result["source"] in expected_set),
        None,
    )


def hit_at(rank: int | None, k: int) -> float:
    return float(rank is not None and rank <= k)


def reciprocal_rank(rank: int | None, k: int) -> float:
    return 1 / rank if rank is not None and rank <= k else 0.0


def main() -> None:
    parser = argparse.ArgumentParser(description="Multi-query retrieval experiment")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--candidates", type=int, default=8)
    args = parser.parse_args()
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be >= 1")
    if args.top_k < 1 or args.candidates < args.top_k:
        parser.error("Require 1 <= top-k <= candidates")

    cases = json.loads(DATASET.read_text(encoding="utf-8-sig"))
    cases = [item for item in cases if item["answerable"]]
    if args.limit is not None:
        cases = cases[:args.limit]
    if not cases:
        parser.error("No answerable evaluation cases")

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        parser.error("GEMINI_API_KEY is missing; set it in .env")
    model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    client = genai.Client(api_key=api_key)

    baseline_ranks = []
    multi_ranks = []
    for item in cases:
        question = item["query"]
        expected = item["relevant_sources"]
        variants = generate_variants(question, client, model_name)
        queries = [question] + variants

        baseline_results = search_chroma(
            query=question, top_k=args.candidates, collection_name=COLLECTION
        )
        multi_results = reciprocal_rank_fusion(queries, candidates=args.candidates)
        baseline_rank = first_relevant_rank(baseline_results, expected)
        multi_rank = first_relevant_rank(multi_results, expected)
        baseline_ranks.append(baseline_rank)
        multi_ranks.append(multi_rank)

        print("\n" + "=" * 66)
        print(f"ID: {item['id']}")
        print(f"ORIGINAL: {question}")
        for index, variant in enumerate(variants, 1):
            print(f"VARIANT {index}: {variant}")
        print(f"EXPECTED: {expected}")
        print(f"BASELINE FIRST RANK: {baseline_rank}")
        print(f"MULTI-QUERY FIRST RANK: {multi_rank}")
        print("MULTI-QUERY TOP RESULTS:")
        for result in multi_results[:args.top_k]:
            print(f"  {result['source']} | Chunk {result['chunk_index']} "
                  f"| RRF {result['rrf_score']:.5f}")

    n = len(cases)
    print("\n" + "=" * 66)
    print(f"EVALUATED ANSWERABLE QUESTIONS: {n}")
    for label, ranks in (("BASELINE", baseline_ranks), ("MULTI-QUERY", multi_ranks)):
        hit = sum(hit_at(rank, args.top_k) for rank in ranks) / n
        mrr = sum(reciprocal_rank(rank, args.candidates) for rank in ranks) / n
        print(f"{label}: Hit@{args.top_k}={hit:.4f} | "
              f"MRR@{args.candidates}={mrr:.4f}")
    print("NOTE: This is a development experiment, not an independent holdout test.")
    print("NOTE: RRF scores are not cosine similarity scores.")
    print("NOTE: Generated query intent and unanswerable-question behavior require review.")


if __name__ == "__main__":
    main()
