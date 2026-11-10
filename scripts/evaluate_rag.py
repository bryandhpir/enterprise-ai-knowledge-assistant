
import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from app.services.rag_service import answer_question
from app.services.vector_store import get_collection
from evals.rag_metrics import (
    evaluate_case,
    summarize_results,
)


BASE_DIR = Path(__file__).resolve().parents[1]
DATASET = BASE_DIR / "evals" / "rag_eval_questions.json"
REPORT_DIR = BASE_DIR / "evals" / "reports"


def get_evidence(sources, collection):
    evidence = {}

    for source in sources:
        records = collection.get(
            where={"source": source["source"]},
            include=["documents", "metadatas"],
        )

        for text, metadata in zip(
            records["documents"],
            records["metadatas"],
        ):
            if metadata["chunk_index"] == source["chunk_index"]:
                evidence[source["id"]] = {
                    "source": source["source"],
                    "chunk_index": source["chunk_index"],
                    "text": text,
                }
                break

    return evidence


def format_rate(value):
    return "N/A" if value is None else f"{value:.1%}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--top-k", type=int, default=3)
    args = parser.parse_args()

    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be positive")

    if not 1 <= args.top_k <= 20:
        parser.error("--top-k must be between 1 and 20")

    cases = json.loads(
        DATASET.read_text(encoding="utf-8")
    )

    if args.limit is not None:
        cases = cases[:args.limit]

    collection = get_collection("it_knowledge_base_v2")
    rows = []

    for index, case in enumerate(cases, start=1):
        print(f"[{index}/{len(cases)}] {case['id']}")

        result = answer_question(
            question=case["query"],
            top_k=args.top_k,
        )

        row = evaluate_case(case, result)
        row["evidence"] = get_evidence(
            result["sources"], collection
        )
        rows.append(row)

    summary = summarize_results(rows)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "collection": "it_knowledge_base_v2",
        "top_k": args.top_k,
        "min_similarity": os.getenv(
            "RAG_MIN_SIMILARITY", ""
        ),
        "summary": summary,
        "results": rows,
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    json_path = REPORT_DIR / "rag_eval.json"
    json_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# Week 4 — RAG Evaluation Report",
        "",
        f"Generated (UTC): {report['generated_at']}",
        f"Collection: {report['collection']}",
        f"Top-K: {args.top_k}",
        f"Evaluated questions: {len(rows)}",
        "",
        "## Automated Metrics",
        "",
    ]

    for key in (
        "source_hit_rate",
        "citation_id_valid_rate",
        "unanswerable_refusal_rate",
    ):
        lines.append(
            f"- {key}: {format_rate(summary[key])}"
        )

    lines += [
        "",
        "## Per-question Results",
        "",
        "| ID | Source Hit | Citation IDs | Correct Refusal |",
        "| --- | --- | --- | --- |",
    ]

    def show(value):
        if value is None:
            return "N/A"
        return "Pass" if value else "Fail"

    for row in rows:
        lines.append(
            f"| {row['id']} "
            f"| {show(row['source_hit'])} "
            f"| {show(row['citation_valid'])} "
            f"| {show(row['refusal_correct'])} |"
        )

    lines += [
        "",
        "## Manual Review",
        "",
        "Review each answer against its exact retrieved chunks.",
        "Use the evidence stored in week4_rag_eval.json.",
        "",
        "| ID | Grounded 0/1 | Complete 0/1 | Citation supported 0/1 | Notes |",
        "| --- | --- | --- | --- | --- |",
    ]

    for row in rows:
        lines.append(
            f"| {row['id']} | TBD | TBD | TBD | |"
        )

    lines += [
        "",
        "## Limitations",
        "",
        "- Source Hit measures source-level retrieval only.",
        "- Citation ID validation does not prove claim support.",
        "- Groundedness and completeness require manual review.",
        "- Generation can vary between runs.",
        "- The five historical holdout questions have been used in prior analysis.",
    ]

    md_path = REPORT_DIR / "rag_eval.md"
    md_path.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    print("\n===== SUMMARY =====")
    print(json.dumps(summary, indent=2))
    print("\nReports:")
    print(json_path)
    print(md_path)


if __name__ == "__main__":
    main()
