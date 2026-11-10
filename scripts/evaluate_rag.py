"""Evaluate RAG outputs; keep preview reports separate from full reports."""

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from app.services.rag_service import answer_question
from app.services.vector_store import get_collection
from evals.rag_metrics import evaluate_case, summarize_results

BASE_DIR = Path(__file__).resolve().parents[1]
DATASET = BASE_DIR / "evals" / "rag_eval_questions.json"
REPORT_DIR = BASE_DIR / "evals" / "reports"


def get_evidence(sources, collection):
    """Match returned source IDs to indexed chunks for later manual review."""
    evidence = {}
    for source in sources:
        records = collection.get(
            where={"source": source["source"]},
            include=["documents", "metadatas"],
        )
        documents = records.get("documents") or []
        metadatas = records.get("metadatas") or []
        for text, metadata in zip(documents, metadatas):
            if metadata and metadata.get("chunk_index") == source["chunk_index"]:
                evidence[source["id"]] = {
                    "source": source["source"],
                    "chunk_index": source["chunk_index"],
                    "text": text,
                }
                break
    return evidence


def format_rate(value):
    return "N/A" if value is None else f"{value:.1%}"


def display_status(value):
    if value is None:
        return "N/A"
    return "Pass" if value else "Fail"


def main():
    parser = argparse.ArgumentParser(description="Evaluate the RAG pipeline")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--top-k", type=int, default=3)
    args = parser.parse_args()

    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be positive")
    if not 1 <= args.top_k <= 20:
        parser.error("--top-k must be between 1 and 20")
    if not DATASET.is_file():
        parser.error(f"Evaluation dataset not found: {DATASET}")

    try:
        cases = json.loads(DATASET.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        parser.error(f"Invalid JSON in {DATASET}: {exc}")
    if not isinstance(cases, list) or not cases:
        parser.error("Evaluation dataset must be a non-empty JSON array")

    total_cases = len(cases)
    if args.limit is not None:
        cases = cases[:args.limit]

    collection = get_collection("it_knowledge_base_v2")
    rows = []
    for index, case in enumerate(cases, start=1):
        print(f"[{index}/{len(cases)}] {case['id']}")
        result = answer_question(question=case["query"], top_k=args.top_k)
        row = evaluate_case(case, result)
        row["evidence"] = get_evidence(result["sources"], collection)
        rows.append(row)

    summary = summarize_results(rows)
    preview = args.limit is not None and len(cases) < total_cases
    suffix = f"_preview_{len(cases)}" if preview else ""
    json_path = REPORT_DIR / f"rag_eval{suffix}.json"
    md_path = REPORT_DIR / f"rag_eval{suffix}.md"

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "collection": "it_knowledge_base_v2",
        "top_k": args.top_k,
        "min_similarity": os.getenv("RAG_MIN_SIMILARITY", ""),
        "preview": preview,
        "summary": summary,
        "results": rows,
    }
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    json_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    title = "RAG Evaluation Preview" if preview else "RAG Evaluation Report"
    lines = [
        f"# {title}",
        "",
        f"Generated (UTC): {report['generated_at']}",
        f"Collection: `{report['collection']}`",
        f"Top-K: {args.top_k}",
        f"Questions evaluated: {len(rows)} of {total_cases}",
        f"Minimum similarity: {report['min_similarity'] or 'disabled'}",
        "",
        "## Automated Metrics",
        "",
    ]
    for key in (
        "source_hit_rate", "citation_id_valid_rate", "unanswerable_refusal_rate"
    ):
        lines.append(f"- {key}: {format_rate(summary[key])}")

    lines.extend([
        "",
        "## Per-question Results",
        "",
        "| ID | Source Hit | Citation IDs | Correct Refusal |",
        "| --- | --- | --- | --- |",
    ])
    for row in rows:
        lines.append(
            f"| {row['id']} | {display_status(row['source_hit'])} "
            f"| {display_status(row['citation_valid'])} "
            f"| {display_status(row['refusal_correct'])} |"
        )

    lines.extend([
        "",
        "## Manual Review",
        "",
        f"Compare generated answers with source passages stored in `{json_path.name}`.",
        "",
        "| ID | Grounded | Complete | Citation supported | Notes |",
        "| --- | --- | --- | --- | --- |",
    ])
    for row in rows:
        lines.append(f"| {row['id']} | Not assessed | Not assessed | Not assessed | |")

    lines.extend([
        "",
        "## Limitations",
        "",
        "- Source Hit uses source-level relevance, not passage-level correctness.",
        "- Valid citation IDs do not prove claim-to-source support.",
        "- Groundedness and completeness require human review.",
        "- The evaluation set is small and some questions were used in prior analysis.",
        "- Generation can vary between runs.",
    ])
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("\n===== SUMMARY =====")
    print(json.dumps(summary, indent=2))
    print("\nReports:")
    print(json_path)
    print(md_path)


if __name__ == "__main__":
    main()
