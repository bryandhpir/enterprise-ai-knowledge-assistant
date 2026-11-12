"""Review query expansion on out-of-scope questions without generating answers.

Run from the repository root:
    python -m scripts.audit_multi_query_safety

Requires scripts/experiment_multi_query.py to be present.
This is a retrieval / intent-drift inspection, NOT a refusal-rate evaluation.
"""

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from app.services.chroma_search import search_chroma
from scripts.experiment_multi_query import (
    generate_variants,
    reciprocal_rank_fusion,
)

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "evals" / "rag_eval_questions.json"
OUTPUT = ROOT / "evals" / "reports" / "multi_query_safety_audit.json"
COLLECTION = "it_knowledge_base_v2"


def brief_results(results: list[dict], limit: int = 3) -> list[dict]:
    """Keep source/rank metadata; do not treat RRF as cosine similarity."""
    return [
        {
            "rank": rank,
            "source": item["source"],
            "chunk_index": item["chunk_index"],
            "score": item.get("score"),
            "rrf_score": item.get("rrf_score"),
        }
        for rank, item in enumerate(results[:limit], start=1)
    ]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inspect Multi-Query intent drift on unanswerable questions"
    )
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be positive")

    load_dotenv(ROOT / ".env")
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        parser.error("GEMINI_API_KEY is missing")

    cases = json.loads(DATASET.read_text(encoding="utf-8-sig"))
    cases = [case for case in cases if not case["answerable"]]
    if args.limit is not None:
        cases = cases[: args.limit]
    if not cases:
        parser.error("No unanswerable cases to audit")

    model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    client = genai.Client(api_key=key)
    rows = []

    for case in cases:
        question = case["query"]
        variants = generate_variants(question, client, model_name)
        baseline = search_chroma(
            query=question, top_k=8, collection_name=COLLECTION
        )
        fused = reciprocal_rank_fusion(
            queries=[question, *variants], candidates=8
        )
        record = {
            "id": case["id"],
            "question": question,
            "variants": variants,
            "baseline_top3": brief_results(baseline),
            "multi_query_top3": brief_results(fused),
            "manual_intent_preserved": None,
            "manual_notes": "",
        }
        rows.append(record)

        print("\n" + "=" * 64)
        print(f"ID: {case['id']}")
        print(f"ORIGINAL: {question}")
        for i, variant in enumerate(variants, start=1):
            print(f"VARIANT {i}: {variant}")
        print("BASELINE SOURCES:", [r["source"] for r in record["baseline_top3"]])
        print("MULTI-QUERY SOURCES:", [r["source"] for r in record["multi_query_top3"]])
        print("REVIEW: Did the rewrites preserve the original intent?")

    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "model": model_name,
        "collection": COLLECTION,
        "purpose": "Manual intent-drift and retrieval inspection; not a refusal metric",
        "cases": rows,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSaved inspection report to: {OUTPUT}")
    print("NOTE: This script does not generate final answers or measure refusal quality.")


if __name__ == "__main__":
    main()
